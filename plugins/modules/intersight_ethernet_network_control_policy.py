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
module: intersight_ethernet_network_control_policy
short_description: Fabric Ethernet Network Control Policy configuration for Cisco Intersight
description:
  - Fabric Ethernet Network Control Policy configuration for Cisco Intersight.
  - Used to configure Fabric Ethernet Network Control Policy on Cisco Intersight managed devices.
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
      - The name assigned to the LAN Connectivity policy.
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
  cdp_enabled:
    description:
      -  Enables the CDP on an interface.
    default: False
    type: bool
  forge_mac:
    description:
      -  Determines if the MAC forging is allowed or denied on an interface.
      -  allow - Allows mac forging on an interface.
      -  deny - Denies mac forging on an interface.
    choices: ['allow' , 'deny']
    default: allow
    type: str
  lldp_settings:
    description:
      -  Determines the LLDP setting on an interface on the switch.
    type: list
    elements: dict
    suboptions:
      receive_enabled:
        description:
          - Determines if the LLDP frames can be received by an interface on the switch.
        type: bool
        default: True
      transmit_enabled:
        description:
          - Determines if the LLDP frames can be transmitted by an interface on the switch.
        type: bool
        default: False
  mac_registration_mode:
    description:
      -  Determines the MAC addresses that have to be registered with the switch.
      -  nativeVlanOnly - Register only the MAC addresses learnt on the native VLAN.
      -  allVlans - Register all the MAC addresses learnt on all the allowed VLANs.
    choices: ['nativeVlanOnly' , 'allVlans']
    default: nativeVlanOnly
    type: str
  uplink_fail_action:
    description:
      -  Determines the state of the virtual interface (vethernet / vfc) on the switch when a suitable uplink is not pinned.
      -  linkDown - The vethernet will go down in case a suitable uplink is not pinned.
      -  warning - The vethernet will remain up even if a suitable uplink is not pinned.
    choices: ['linkDown' , 'warning']
    default: linkDown
    type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Fabric Ethernet Network Control Policy
  cisco.intersight.intersight_ethernet_network_control_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-ENCP
    description: Fabric Ethernet Network Control Policy for COS
    tags:
      - Key: Site
        Value: RCDN
    cdp_enabled: true


- name: Delete Fabric Ethernet Network Control Policy
  cisco.intersight.intersight_ethernet_qos_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-ENCP
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
        "ObjectType": "fabric.EthNetworkControlPolicy",
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


def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = params[prop_key]


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
    lldp_settings_spec = {
        "receive_enabled" : {"type": "bool", "default": True},
        "transmit_enabled" : {"type": "bool", "default": False}
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        cdp_enabled={
            "type": "bool",
            "default": False
        },
        forge_mac={
            "type": "str",
            "choices": [
                'allow',
                'deny'
            ],
            "default": "allow"
        },
        lldp_settings={
            "type": "list",
            "elements": "dict",
            "options": lldp_settings_spec
        },
        mac_registration_mode={
            "type": "str",
            "choices": [
                'nativeVlanOnly',
                'allVlans'
            ],
            "default": "nativeVlanOnly"
        },
        uplink_fail_action={
            "type": "str",
            "choices": [
                'linkDown',
                'warning'
            ],
            "default": "linkDown"
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
    resource_path = '/fabric/EthNetworkControlPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('CdpEnabled', 'cdp_enabled', intersight.module.params, intersight.api_body)
    check_and_add_prop('ForgeMac', 'forge_mac', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('LldpSettings', 'lldp_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop('MacRegistrationMode', 'mac_registration_mode', intersight.module.params, intersight.api_body)
    check_and_add_prop('UplinkFailAction', 'uplink_fail_action', intersight.module.params, intersight.api_body)
    check_and_add_prop('NetworkPolicy', 'network_policy', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
