#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: intersight_server_profile_derive
short_description: Derive Server Profiles from Templates in Cisco Intersight
description:
  - Derive new Server Profiles from a Server Profile Template using the Intersight MoCloner API.
  - Sync existing derived profiles back to their template when the template has changed using the MoMerger API.
  - Idempotent - will not re-derive if the profile already exists, and will not sync if the profile is already in sync.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  organization:
    description:
      - The name of the Organization this resource is assigned to.
    type: str
    default: default
  template_name:
    description:
      - Name of the Server Profile Template to derive from.
      - The template must exist in the specified organization.
    type: str
    required: true
  profile_names:
    description:
      - List of Server Profile names to derive from the template.
      - Each name must be unique within the organization.
    type: list
    elements: str
    required: true
  state:
    description:
      - If C(present), will derive profiles that do not exist and sync profiles that are out of sync with the template.
      - If C(absent), will delete derived profiles.
    type: str
    choices: [present, absent]
    default: present
  force_sync:
    description:
      - When C(true), always sync existing derived profiles to the template, even if the profile appears to be in sync.
      - When C(false), only sync profiles whose ConfigContext shows they are out of sync with the template.
    type: bool
    default: false
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Derive a single server profile from a template
  cisco.intersight.intersight_server_profile_derive:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: default
    template_name: My-Standard-Template
    profile_names:
      - SP-Derived-1

- name: Derive multiple server profiles from a template
  cisco.intersight.intersight_server_profile_derive:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: default
    template_name: My-Standard-Template
    profile_names:
      - SP-Derived-1
      - SP-Derived-2
      - SP-Derived-3

- name: Force sync derived profiles back to template
  cisco.intersight.intersight_server_profile_derive:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    template_name: My-Standard-Template
    profile_names:
      - SP-Derived-1
    force_sync: true

- name: Delete derived server profiles
  cisco.intersight.intersight_server_profile_derive:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    template_name: My-Standard-Template
    profile_names:
      - SP-Derived-1
    state: absent
'''

RETURN = r'''
api_response:
  description: Summary of derive/sync operations performed.
  returned: always
  type: dict
  sample:
    "api_response": {
        "derived": ["SP-Derived-1", "SP-Derived-2"],
        "synced": ["SP-Derived-3"],
        "skipped": [],
        "deleted": []
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def get_profile_by_name(intersight, profile_name):
    """Look up a server profile by name."""
    options = {
        'http_method': 'get',
        'resource_path': '/server/Profiles',
        'query_params': {
            '$filter': "Name eq '" + profile_name + "'",
        },
    }
    response = intersight.call_api(**options)
    if response.get('Results'):
        return response['Results'][0]
    return None


def get_template_moid(intersight, template_name, organization_moid):
    """Look up a server profile template by name and org."""
    options = {
        'http_method': 'get',
        'resource_path': '/server/ProfileTemplates',
        'query_params': {
            '$filter': "Name eq '" + template_name + "' and Organization.Moid eq '" + organization_moid + "'",
        },
    }
    response = intersight.call_api(**options)
    if response.get('Results'):
        return response['Results'][0]['Moid']
    return None


def derive_profile(intersight, template_moid, profile_name, organization_moid):
    """Derive a new server profile from a template using MoCloner."""
    options = {
        'http_method': 'post',
        'resource_path': '/bulk/MoCloners',
        'body': {
            'Sources': [
                {
                    'ClassId': 'mo.MoRef',
                    'ObjectType': 'server.ProfileTemplate',
                    'Moid': template_moid,
                }
            ],
            'Targets': [
                {
                    'Name': profile_name,
                    'ObjectType': 'server.Profile',
                    'ClassId': 'server.Profile',
                    'Organization': {
                        'Moid': organization_moid,
                    },
                }
            ],
        },
    }
    return intersight.call_api(**options)


def sync_profile(intersight, template_moid, profile_moid):
    """Sync a derived profile back to its template using MoMerger."""
    options = {
        'http_method': 'post',
        'resource_path': '/bulk/MoMergers',
        'body': {
            'Sources': [
                {
                    'ObjectType': 'server.ProfileTemplate',
                    'Moid': template_moid,
                }
            ],
            'Targets': [
                {
                    'ObjectType': 'server.Profile',
                    'Moid': profile_moid,
                }
            ],
            'MergeAction': 'Replace',
        },
    }
    return intersight.call_api(**options)


def delete_profile(intersight, profile_moid):
    """Delete a server profile by Moid."""
    options = {
        'http_method': 'delete',
        'resource_path': '/server/Profiles',
        'moid': profile_moid,
    }
    return intersight.call_api(**options)


def profile_needs_sync(profile, force_sync):
    """Check if a derived profile needs syncing."""
    if force_sync:
        return True
    config_context = profile.get('ConfigContext', {})
    config_state = config_context.get('ConfigState', '')
    return config_state in ('Pending-changes', 'Out-of-sync', 'Inconsistent')


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        organization=dict(type='str', default='default'),
        template_name=dict(type='str', required=True),
        profile_names=dict(type='list', elements='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        force_sync=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    organization_name = module.params['organization']
    template_name = module.params['template_name']
    profile_names = module.params['profile_names']
    state = module.params['state']
    force_sync = module.params['force_sync']

    organization_moid = intersight.get_moid_by_name(
        resource_path='/organization/Organizations',
        resource_name=organization_name,
    )
    if not organization_moid:
        module.fail_json(msg="Organization '%s' not found." % organization_name)

    result_summary = {
        'derived': [],
        'synced': [],
        'skipped': [],
        'deleted': [],
    }

    template_moid = None
    if state == 'present':
        template_moid = get_template_moid(intersight, template_name, organization_moid)
        if not template_moid:
            module.fail_json(msg="Server Profile Template '%s' not found in organization '%s'." % (template_name, organization_name))

    for profile_name in profile_names:
        existing_profile = get_profile_by_name(intersight, profile_name)

        if state == 'absent':
            if existing_profile:
                if not module.check_mode:
                    delete_profile(intersight, existing_profile['Moid'])
                result_summary['deleted'].append(profile_name)
                intersight.result['changed'] = True
            else:
                result_summary['skipped'].append(profile_name)
            continue

        if existing_profile:
            if profile_needs_sync(existing_profile, force_sync):
                if not module.check_mode:
                    sync_profile(intersight, template_moid, existing_profile['Moid'])
                result_summary['synced'].append(profile_name)
                intersight.result['changed'] = True
            else:
                result_summary['skipped'].append(profile_name)
        else:
            if not module.check_mode:
                derive_profile(intersight, template_moid, profile_name, organization_moid)
            result_summary['derived'].append(profile_name)
            intersight.result['changed'] = True

    intersight.result['api_response'] = result_summary
    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
