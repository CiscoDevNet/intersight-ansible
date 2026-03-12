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
module: intersight_resource_group_info
short_description: Gather information about Resource Groups in Cisco Intersight
description:
  - Gather information about Resource Groups in L(Cisco Intersight,https://intersight.com).
  - Information can be filtered by O(name).
  - If no filters are passed, all Resource Groups will be returned.
  - Resource Groups are account-level resources and are not scoped to an organization.
extends_documentation_fragment: intersight
options:
  name:
    description:
      - The name of the Resource Group to gather information from.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Fetch a specific Resource Group by name
  cisco.intersight.intersight_resource_group_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "all-resources-group"

- name: Fetch all Resource Groups
  cisco.intersight.intersight_resource_group_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": [
    {
        "Name": "all-resources-group",
        "ObjectType": "resource.Group",
        "Qualifier": "Allow-All",
        "Selectors": []
    },
    {
        "Name": "selected-devices-group",
        "ObjectType": "resource.Group",
        "Qualifier": "Allow-Selectors",
        "Selectors": [
            {
                "Selector": "/api/v1/asset/DeviceRegistrations?$filter=Moid in ('6758c0cc6f726138013e7077')"
            }
        ]
    }
  ]
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        name=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/resource/Groups'

    query_params = intersight.set_query_params()

    intersight.get_resource(
        resource_path=resource_path,
        query_params=query_params,
        return_list=True,
    )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
