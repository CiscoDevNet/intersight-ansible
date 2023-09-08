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
module: intersight_ethernet_network_policy
short_description: Ethernet Network Policy configuration for Cisco Intersight
description:
  - Ethernet Network Policy configuration for Cisco Intersight.
  - Used to configure Ethernet Network Policy on Cisco Intersight managed devices.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    choices: [present, absent]
    default: present
    type: str
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    default: default
    type: str
  name:
    description:
      - The name assigned to the Ethernet Network policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
    type: str
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements : dict
  description:
    description:
      - The user-defined description of the Boot Order policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
  vlan_settings:
    description:
      -  VLAN configuration for the virtual interface.
    type: list
    elements: dict
    suboptions:
      default_vlan:
        description:
          - Native VLAN ID of the virtual interface or the corresponding vethernet on the peer Fabric Interconnect to which the virtual interface is connected.
          - Setting the ID to 0 will not associate any native VLAN to the traffic on the virtual interface.
        type: int
        default: 0
      mode:
        description:
          - Option to determine if the port can carry single VLAN (Access) or multiple VLANs (Trunk) traffic.
          - ACCESS - An access port carries traffic only for a single VLAN on the interface.
          - TRUNK - A trunk port can have two or more VLANs configured on the interface. It can carry traffic for several VLANs simultaneously.
        type: str
        choices: ['ACCESS', 'TRUNK']
        default: ACCESS
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Ethernet Network Policy
  cisco.intersight.intersight_ethernet_network_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-ENWP
    description: Ethernet Network Policy for COS
    tags:
      - Key: Site
        Value: RCDN
    vlan_settings:
      - default_vlan: 693
        mode: ACCESS


- name: Delete Ethernet Network Policy
  cisco.intersight.intersight_ethernet_network_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-ENWP
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-ENWP",
        "ObjectType": "vnic.EthNetworkPolicy",
        "Tags": [
            {
                "Key": "Site",
                "Value": "RCDN"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def check_and_add_prop_dict(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = {}
        if params[prop_key] :
            for item in params[prop_key]:
                for key in item.keys():
                    api_body[prop][to_camel_case(key)] = item[key]


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    vlan_settings_spec = {
        "default_vlan" : {"type": "int", "default": 0},
        "mode": {"type": "str", "default": "ACCESS", "choices": ['ACCESS', 'TRUNK']},
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        vlan_settings={
            "type": "list",
            "elements": "dict",
            "options": vlan_settings_spec
        },
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    #
    # Argument spec above, resource path, and API body should be the only code changed in each policy module
    #
    # Resource path used to configure policy
    resource_path = '/vnic/EthNetworkPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop_dict('VlanSettings', 'vlan_settings', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
