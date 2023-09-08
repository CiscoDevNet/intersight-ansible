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
module: intersight_ethernet_qos_policy
short_description: Ethernet Qos policy configuration for Cisco Intersight
description:
  - Ethernet Qos policy configuration for Cisco Intersight.
  - Used to configure Ethernet Qos Policy on Cisco Intersight managed devices.
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
      - The name assigned to the Ethernent Qos policy.
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
  burst:
    description:
      -  The burst traffic, in bytes, allowed on the vNIC.
    default: 10240
    type: int
  cos:
    description:
      -  Class of Service to be associated to the traffic on the virtual interface.
    default: 0
    type: int
  mtu:
    description:
      -  The Maximum Transmission Unit (MTU) or packet size that the virtual interface accepts.
    default: 1500
    type: int
  priority:
    description:
      -  The priority matching the System QoS specified in the fabric profile.
      -  Best Effort - QoS priority for Best-effort traffic.
      -  FC - QoS priority for FC traffic.
      -  Platinum - QoS priority for Platinum traffic.
      -  Gold - QoS priority for Gold traffic.
      -  Silver - QoS priority for Silver traffic.
      -  Bronze - QoS priority for Bronze traffic.
    choices: ['Best Effort' , 'FC' , 'Platinum' , 'Gold' , 'Silver' , 'Bronze']
    default: Best Effort
    type: str
  rate_limit:
    description:
      -  The value in Mbps (0-10G/40G/100G depending on Adapter Model) to use for limiting the data rate on the virtual interface.
    default: 0
    type: int
  trust_host_cos:
    description:
      -  Enables usage of the Class of Service provided by the operating system.
    default: False
    type: bool
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Ethernet QoS Policy
  cisco.intersight.intersight_ethernet_qos_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-EQOS
    description: Ethernet Qos policy for COS
    tags:
      - Key: Site
        Value: RCDN
    mtu: 1500

- name: Delete Ethernet Qos Policy
  cisco.intersight.intersight_ethernet_qos_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-EQOS
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-LCP",
        "ObjectType": "vnic.EthQosPolicy",
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


def check_and_add_prop(prop, propKey, params, api_body):
    if propKey in params.keys():
        api_body[prop] = params[propKey]


def main():
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        burst={
            "type": "int",
            "default": 10240
        },
        cos={
            "type": "int",
            "default": 0
        },
        mtu={
            "type": "int",
            "default": 1500
        },
        priority={
            "type": "str",
            "choices": [
                'Best Effort',
                'FC',
                'Platinum',
                'Gold',
                'Silver',
                'Bronze'
            ],
            "default": "Best Effort"
        },
        rate_limit={
            "type": "int",
            "default": 0
        },
        trust_host_cos={
            "type": "bool",
            "default": False
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
    resource_path = '/vnic/EthQosPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('Burst', 'burst', intersight.module.params, intersight.api_body)
    check_and_add_prop('Cos', 'cos', intersight.module.params, intersight.api_body)
    check_and_add_prop('Mtu', 'mtu', intersight.module.params, intersight.api_body)
    check_and_add_prop('Priority', 'priority', intersight.module.params, intersight.api_body)
    check_and_add_prop('RateLimit', 'rate_limit', intersight.module.params, intersight.api_body)
    check_and_add_prop('TrustHostCos', 'trust_host_cos', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
