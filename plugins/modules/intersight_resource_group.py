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
module: intersight_resource_group
short_description: Resource Group configuration for Cisco Intersight
description:
  - Manages Resource Group configuration on Cisco Intersight.
  - Resource Groups define a set of resources that can be used for access control and organization assignment.
  - Supports both C(all) and C(selectors) qualifier types.
  - Resource Groups are account-level resources and are not scoped to an organization.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/resource/Group/model/).
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
      - The name assigned to the Resource Group.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description for the Resource Group.
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  qualifier:
    description:
      - Qualifier defines how resources are added to the Resource Group.
      - C(all) includes all resources (represents Allow-All in the API).
      - C(selectors) uses selector queries to filter specific resources (represents Allow-Selectors in the API).
    type: str
    choices: [all, selectors]
    default: all
  selectors:
    description:
      - List of selector query strings used to filter resources for the Resource Group.
      - Required when O(qualifier) is C(selectors).
      - "Each selector is an API path with a filter query."
      - "Example: C(/api/v1/asset/DeviceRegistrations?$filter=Moid in ('moid_value'))"
      - "Example: C(/api/v1/compute/Blades?$filter=Serial in ('serial_value') and ManagementMode eq 'Intersight')"
    type: list
    elements: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create Resource Group with all qualifier
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "all-resources-group"
    description: "Resource group that includes all resources"
    qualifier: "all"
    state: present

- name: Create Resource Group with selectors for specific devices
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "selected-devices-group"
    description: "Resource group for specific devices"
    qualifier: "selectors"
    selectors:
      - "/api/v1/asset/DeviceRegistrations?$filter=Moid in ('507f1f77bcf86cd799439011')"
    state: present

- name: Create multiple Resource Groups for UCS domains
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "{{ item.name }}"
    description: "{{ item.description }}"
    qualifier: "selectors"
    selectors:
      - "{{ item.selector }}"
    state: present
  loop:
    - name: "ucs-lab-domain-1"
      description: "Lab UCS domain 1"
      selector: "/api/v1/asset/DeviceRegistrations?$filter=Moid in ('507f1f77bcf86cd799439011')"
    - name: "ucs-lab-domain-2"
      description: "Lab UCS domain 2"
      selector: "/api/v1/asset/DeviceRegistrations?$filter=Moid in ('507f1f77bcf86cd799439022')"
    - name: "ucs-lab-domain-3"
      description: "Lab UCS domain 3"
      selector: "/api/v1/asset/DeviceRegistrations?$filter=Moid in ('507f1f77bcf86cd799439033')"

- name: Create Resource Group with selectors for compute blades
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "blade-servers-group"
    qualifier: "selectors"
    selectors:
      - "/api/v1/compute/Blades?$filter=Serial in ('FCH26387CE1') and ManagementMode eq 'Intersight'"
    state: present

- name: Update Resource Group from all to selectors
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "all-resources-group"
    description: "Now scoped to specific devices"
    qualifier: "selectors"
    selectors:
      - "/api/v1/asset/DeviceRegistrations?$filter=Moid in ('507f1f77bcf86cd799439011')"
    state: present

- name: Delete Resource Group
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "all-resources-group"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "all-resources-group",
        "ObjectType": "resource.Group",
        "Description": "Resource group that includes all resources",
        "Qualifier": "Allow-All",
        "Selectors": []
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec

QUALIFIER_MAP = {
    'all': 'Allow-All',
    'selectors': 'Allow-Selectors',
}


def build_api_body(intersight):
    """Build the API body for Resource Group configuration."""
    params = intersight.module.params
    if params['state'] == 'present':
        intersight.api_body = {
            'Name': params['name'],
            'Qualifier': QUALIFIER_MAP[params['qualifier']],
        }

        if params['qualifier'] == 'selectors' and params.get('selectors'):
            intersight.api_body['Selectors'] = [
                {'Selector': s} for s in params['selectors']
            ]

        intersight.set_tags_and_description()


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        qualifier=dict(type='str', choices=['all', 'selectors'], default='all'),
        selectors=dict(type='list', elements='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ['qualifier', 'selectors', ['selectors']],
        ],
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    build_api_body(intersight)

    resource_path = '/resource/Groups'

    intersight.configure_secondary_resource(
        resource_path=resource_path,
        resource_name=module.params['name'],
        state=module.params['state'],
    )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
