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
module: intersight_domain_info
short_description: Gather information about UCS Domain Profiles in Cisco Intersight
description:
  - Gather information about UCS Domain Profiles (SwitchClusterProfiles) in L(Cisco Intersight,https://intersight.com).
  - Returns enriched data including SwitchProfiles (A and B), their assigned Fabric Interconnects, and attached PolicyBuckets.
  - Information can be filtered by O(name) and O(organization).
  - If no filters are passed, all UCS Domain Profiles will be returned.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/fabric/SwitchClusterProfiles/get/).
extends_documentation_fragment: intersight
options:
  name:
    description:
      - The name of the UCS Domain Profile to gather information from.
    type: str
  organization:
    description:
      - The name of the Organization to filter UCS Domain Profiles by.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Fetch a specific UCS Domain Profile by name
  cisco.intersight.intersight_domain_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "Domain-01"

- name: Fetch all UCS Domain Profiles in an organization
  cisco.intersight.intersight_domain_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"

- name: Fetch all UCS Domain Profiles
  cisco.intersight.intersight_domain_info:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
'''

RETURN = r'''
api_response:
  description:
    - List of UCS Domain Profiles with enriched SwitchProfile details.
    - Each profile includes a C(SwitchProfiles) list containing the SwitchProfile data
      for Fabric Interconnect A and B, including their C(AssignedSwitch) and C(PolicyBucket).
  returned: always
  type: list
  elements: dict
  sample:
    - Name: "Domain-01"
      ObjectType: "fabric.SwitchClusterProfile"
      SwitchProfiles:
        - Name: "Domain-01-A"
          SwitchId: "A"
          AssignedSwitch:
            Moid: "abc123"
            ObjectType: "network.Element"
          PolicyBucket:
            - Moid: "pol123"
              ObjectType: "fabric.SystemQosPolicy"
        - Name: "Domain-01-B"
          SwitchId: "B"
          AssignedSwitch: null
          PolicyBucket: []
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import (
    IntersightModule,
    intersight_argument_spec,
)


def enrich_with_switch_profiles(intersight, clusters):
    """Fetch SwitchProfiles for each cluster and attach them to the response."""
    for cluster in clusters:
        cluster_moid = cluster.get('Moid')
        if not cluster_moid:
            cluster['SwitchProfiles'] = []
            continue

        intersight.get_resource(
            resource_path='/fabric/SwitchProfiles',
            query_params={
                '$filter': f"SwitchClusterProfile.Moid eq '{cluster_moid}'",
                '$select': 'Name,Moid,SwitchId,AssignedSwitch,PolicyBucket,ConfigContext',
            },
            return_list=True,
        )

        profiles = intersight.result['api_response']
        if not isinstance(profiles, list):
            profiles = [profiles] if profiles else []

        cluster['SwitchProfiles'] = profiles

    return clusters


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        name=dict(type='str'),
        organization=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    query_params = intersight.set_query_params()

    intersight.get_resource(
        resource_path='/fabric/SwitchClusterProfiles',
        query_params=query_params,
        return_list=True,
    )

    clusters = intersight.result['api_response']
    if not isinstance(clusters, list):
        clusters = [clusters] if clusters else []

    enriched = enrich_with_switch_profiles(intersight, clusters)

    intersight.result['api_response'] = enriched
    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
