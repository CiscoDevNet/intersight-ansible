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
module: intersight_snmp_policy_info
short_description: Gather information about SNMP Policies in Cisco Intersight
description:
  - Gather information about SNMP Policies in L(Cisco Intersight,https://intersight.com).
  - Information can be filtered by O(organization) and O(name).
  - If no filters are passed, all SNMP Policies will be returned.
extends_documentation_fragment: intersight
options:
  organization:
    description:
      - The name of the organization the SNMP Policy belongs to.
    type: str
  name:
    description:
      - The name of the SNMP Policy to gather information from.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Fetch a specific SNMP Policy by name
  cisco.intersight.intersight_snmp_policy_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "mixed-snmp-policy"

- name: Fetch all SNMP Policies in a specific Organization
  cisco.intersight.intersight_snmp_policy_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"

- name: Fetch all SNMP Policies
  cisco.intersight.intersight_snmp_policy_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": [
    {
        "Name": "mixed-snmp-policy",
        "ObjectType": "snmp.Policy",
        "Enabled": true,
        "V2Enabled": true,
        "V3Enabled": true,
        "SnmpPort": 161,
        "SysContact": "admin@example.com",
        "SysLocation": "Data Center A",
        "CommunityAccess": "Full",
        "AccessCommunityString": "public",
        "TrapCommunity": "trapcomm",
        "EngineId": "custom-engine-id",
        "SnmpUsers": [
            {
                "Name": "admin",
                "SecurityLevel": "AuthPriv",
                "AuthType": "SHA",
                "IsAuthPasswordSet": true,
                "PrivacyType": "AES",
                "IsPrivacyPasswordSet": true
            }
        ],
        "SnmpTraps": [
            {
                "Enabled": true,
                "Version": "V2",
                "Community": "trapcomm",
                "Type": "Trap",
                "Destination": "192.168.1.100",
                "Port": 162
            }
        ],
        "Tags": [
            {
                "Key": "Environment",
                "Value": "Production"
            }
        ]
    },
    {
        "Name": "v3-only-snmp-policy",
        "ObjectType": "snmp.Policy",
        "Enabled": true,
        "V3Enabled": true,
        "SnmpPort": 161,
        "SysContact": "admin@example.com",
        "SysLocation": "Data Center B",
        "CommunityAccess": "Disabled",
        "EngineId": "v3-engine-id",
        "SnmpUsers": [
            {
                "Name": "v3user",
                "SecurityLevel": "AuthPriv",
                "AuthType": "SHA",
                "IsAuthPasswordSet": true,
                "PrivacyType": "AES",
                "IsPrivacyPasswordSet": true
            }
        ],
        "SnmpTraps": [],
        "Tags": []
    }
  ]
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        organization=dict(type='str'),
        name=dict(type='str')
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Resource path used to fetch info
    resource_path = '/snmp/Policies'

    query_params = intersight.set_query_params()

    intersight.get_resource(
        resource_path=resource_path,
        query_params=query_params,
        return_list=True
    )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
