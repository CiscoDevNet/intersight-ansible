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
module: intersight_organization_info
short_description: Gather information about Organizations in Cisco Intersight
description:
  - Gather information about Organizations in L(Cisco Intersight,https://intersight.com).
  - Information can be filtered by O(name).
  - If no filters are passed, all Organizations will be returned.
  - Organizations are account-level resources and are not scoped to another organization.
extends_documentation_fragment: intersight
options:
  name:
    description:
      - The name of the Organization to gather information from.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Fetch a specific Organization by name
  cisco.intersight.intersight_organization_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "my-organization"

- name: Fetch all Organizations
  cisco.intersight.intersight_organization_info:
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
        "Name": "my-organization",
        "ObjectType": "organization.Organization",
        "Description": "My organization"
    },
    {
        "Name": "another-org",
        "ObjectType": "organization.Organization",
        "Description": "Another organization"
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

    resource_path = '/organization/Organizations'

    query_params = intersight.set_query_params()

    intersight.get_resource(
        resource_path=resource_path,
        query_params=query_params,
        return_list=True,
    )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
