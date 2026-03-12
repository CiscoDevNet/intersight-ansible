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
module: intersight_organization
short_description: Organization configuration for Cisco Intersight
description:
  - Manages Organization configuration on Cisco Intersight.
  - Organizations are account-level resources used to organize and manage Intersight resources.
  - Supports assigning Resource Groups to define resource scope.
  - Supports sharing resources with other Organizations via sharing rules.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/organization/Organization/model/).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    type: str
    choices: [present, absent]
    default: present
  name:
    description:
      - The name assigned to the Organization.
    type: str
    required: true
  description:
    description:
      - The user-defined description for the Organization.
    type: str
    aliases: [descr]
  share_resources:
    description:
      - Enable this option to share resources with other Organizations.
      - When C(true), use O(shared_orgs) to specify which Organizations to share with.
      - Mutually exclusive with O(resource_groups).
    type: bool
    default: false
  resource_groups:
    description:
      - List of Resource Group names to assign to the Organization.
      - Resource Group names are resolved to their Moids automatically.
      - Mutually exclusive with O(share_resources) and O(shared_orgs).
    type: list
    elements: str
  shared_orgs:
    description:
      - List of Organization names to share resources with.
      - Only valid when O(share_resources) is C(true).
      - Organization names are resolved to their Moids automatically.
    type: list
    elements: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create Organization with Resource Groups
  cisco.intersight.intersight_organization:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "my-organization"
    description: "My organization"
    resource_groups:
      - "my-resource-group"
    state: present

- name: Create Organization with shared resources
  cisco.intersight.intersight_organization:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "shared-org"
    description: "Organization sharing resources"
    share_resources: true
    shared_orgs:
      - "other-org-1"
      - "other-org-2"
    state: present

- name: Create Organization without Resource Groups
  cisco.intersight.intersight_organization:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "simple-org"
    description: "Simple organization"
    state: present

- name: Delete Organization
  cisco.intersight.intersight_organization:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "my-organization"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "my-organization",
        "ObjectType": "organization.Organization",
        "Description": "My organization"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def build_api_body(intersight):
    """Build the API body for Organization configuration."""
    params = intersight.module.params
    if params['state'] == 'present':
        intersight.api_body = {
            'Name': params['name'],
        }

        if not params['share_resources']:
            if params.get('resource_groups'):
                rg_refs = []
                for rg_name in params['resource_groups']:
                    moid = intersight.get_moid_by_name('/resource/Groups', rg_name)
                    if moid is None:
                        intersight.module.fail_json(msg=f"Resource Group '{rg_name}' not found")
                    rg_refs.append({'ObjectType': 'resource.Group', 'Moid': moid})
                intersight.api_body['ResourceGroups'] = rg_refs
            else:
                intersight.api_body['ResourceGroups'] = []
        else:
            # Shared mode: clear any previously assigned ResourceGroups
            intersight.api_body['ResourceGroups'] = []

        if params.get('description') is not None:
            intersight.api_body['Description'] = params['description']


def get_sharing_rules(intersight, org_moid):
    """Get current sharing rules for an organization."""
    intersight.get_resource(
        resource_path='/iam/SharingRules',
        query_params={
            '$filter': f"SharedResource.Moid eq '{org_moid}'",
        },
        return_list=True,
    )
    return intersight.result['api_response'] if isinstance(intersight.result['api_response'], list) else []


def configure_sharing_rules(intersight, org_moid):
    """Configure sharing rules for an organization."""
    params = intersight.module.params
    shared_org_names = params.get('shared_orgs') or []

    # Get current sharing rules
    current_rules = get_sharing_rules(intersight, org_moid)

    # Build map of current shared org Moids to rule Moids
    current_shared = {}
    for rule in current_rules:
        shared_with_moid = rule.get('SharedWithResource', {}).get('Moid')
        if shared_with_moid:
            current_shared[shared_with_moid] = rule['Moid']

    # Resolve desired shared org names to Moids
    desired_shared = {}
    for org_name in shared_org_names:
        moid = intersight.get_moid_by_name('/organization/Organizations', org_name)
        if moid is None:
            intersight.module.fail_json(msg=f"Organization '{org_name}' not found")
        desired_shared[moid] = org_name

    # Compute diff
    current_moids = set(current_shared.keys())
    desired_moids = set(desired_shared.keys())
    to_add = desired_moids - current_moids
    to_remove = current_moids - desired_moids

    # Delete removed sharing rules
    if to_remove:
        delete_data = [{'moid': current_shared[moid]} for moid in to_remove]
        intersight.configure_bulk_resources(
            resource_path='/iam/SharingRules',
            resources_data=delete_data,
            http_method='delete',
        )

    # Create new sharing rules
    if to_add:
        create_data = [
            {
                'body': {
                    'SharedResource': {
                        'ObjectType': 'organization.Organization',
                        'Moid': org_moid,
                    },
                    'SharedWithResource': {
                        'ObjectType': 'organization.Organization',
                        'Moid': shared_moid,
                    },
                }
            }
            for shared_moid in to_add
        ]
        intersight.configure_bulk_resources(
            resource_path='/iam/SharingRules',
            resources_data=create_data,
            http_method='post',
        )


def cleanup_sharing_rules(intersight, org_moid):
    """Remove all sharing rules for an organization."""
    current_rules = get_sharing_rules(intersight, org_moid)
    if current_rules:
        delete_data = [{'moid': rule['Moid']} for rule in current_rules]
        intersight.configure_bulk_resources(
            resource_path='/iam/SharingRules',
            resources_data=delete_data,
            http_method='delete',
        )


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        share_resources=dict(type='bool', default=False),
        resource_groups=dict(type='list', elements='str'),
        shared_orgs=dict(type='list', elements='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ['share_resources', True, ['shared_orgs']],
        ],
    )

    if module.params['share_resources'] and module.params.get('resource_groups'):
        module.fail_json(msg="parameters are mutually exclusive: share_resources=true and resource_groups")

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    build_api_body(intersight)

    resource_path = '/organization/Organizations'

    # Clean up sharing rules BEFORE modifying the organization.
    # The Intersight API rejects ResourceGroup changes on orgs that still
    # have active sharing rules, so removal must happen first.
    if not module.check_mode:
        intersight.get_resource(
            resource_path=resource_path,
            query_params={'$filter': f"Name eq '{module.params['name']}'"},
        )
        existing_moid = intersight.result['api_response'].get('Moid')
        if existing_moid and module.params['state'] == 'absent' or not module.params['share_resources']:
            cleanup_sharing_rules(intersight, existing_moid)

    intersight.configure_secondary_resource(
        resource_path=resource_path,
        resource_name=module.params['name'],
        state=module.params['state'],
    )

    org_response = intersight.result['api_response']
    org_moid = org_response.get('Moid')

    if module.params['state'] == 'present' and org_moid:
        if module.params['share_resources']:
            configure_sharing_rules(intersight, org_moid)

    intersight.result['api_response'] = org_response
    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
