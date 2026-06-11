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
module: intersight_confidential_compute_info
short_description: Gather information about Confidential Compute Policies
description:
  - Gathers information about Confidential Compute Policies on Cisco Intersight.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  organization:
    description:
      - The name of the Organization this resource is assigned to.
    type: str
    default: default
  name:
    description:
      - The name assigned to the Confidential Compute Policy.
    type: str
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Get Confidential Compute Policy Info
  cisco.intersight.intersight_confidential_compute_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "cc-policy"
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: list
  sample:
    [
      {
        "Name": "cc-policy",
        "ObjectType": "confidentialcompute.Policy",
        "SevEnabled": true
      }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        organization=dict(type='str', default='default'),
        name=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/confidentialcompute/Policies'
    query_params = intersight.set_query_params()

    intersight.get_resource(resource_path=resource_path, query_params=query_params, return_list=True)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
