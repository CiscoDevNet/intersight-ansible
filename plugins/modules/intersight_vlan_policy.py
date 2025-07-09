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
module: intersight_vlan_policy
short_description: VLAN Policy configuration for Cisco Intersight
description:
  - Manages VLAN Policy configuration on Cisco Intersight.
  - A policy to configure VLAN settings for network interfaces on Cisco Intersight managed servers.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/fabric/EthNetworkPolicy/get/).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    type: str
    choices: [present, absent]
    default: present
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles, Policies, and Pools that are created within a Custom Organization are applicable only to devices in the same Organization.
    type: str
    default: default
  name:
    description:
      - The name assigned to the VLAN Policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description for the VLAN Policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  vlans:
    description:
      - List of VLANs to be created and attached to the VLAN policy.
    type: list
    elements: dict
    suboptions:
      prefix:
        description:
          - Prefix for the VLAN name.
        type: str
        required: true
      vlan_id:
        description:
          - VLAN ID number.
        type: int
        required: true
      auto_allow_on_uplinks:
        description:
          - Whether to automatically allow this VLAN on uplinks.
        type: bool
        default: true
      enable_sharing:
        description:
          - Whether to enable VLAN sharing.
        type: bool
        default: false
      multicast_policy_name:
        description:
          - Name of the multicast policy to associate with this VLAN.
          - Required when enable_sharing is false.
        type: str
      sharing_type:
        description:
          - Type of VLAN sharing when enable_sharing is true.
        type: str
        choices: ['Primary', 'Isolated', 'Community']
      primary_vlan_id:
        description:
          - Primary VLAN ID when sharing_type is Isolated or Community.
        type: int
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a VLAN Policy with VLANs
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "test-vlan-policy"
    description: "Test VLAN policy"
    tags:
      - Key: "Site"
        Value: "DataCenter-A"
    vlans:
      - prefix: "production"
        vlan_id: 100
        auto_allow_on_uplinks: true
        enable_sharing: false
        multicast_policy_name: "my-multicast-policy"
      - prefix: "development"
        vlan_id: 200
        auto_allow_on_uplinks: false
        enable_sharing: false
        multicast_policy_name: "my-multicast-policy"
    state: present

- name: Create a VLAN Policy with VLAN sharing
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "shared-vlan-policy"
    vlans:
      - prefix: "primary"
        vlan_id: 79
        enable_sharing: true
        sharing_type: "Primary"
      - prefix: "isolated"
        vlan_id: 90
        enable_sharing: true
        sharing_type: "Isolated"
        primary_vlan_id: 79
    state: present

- name: Create a VLAN Policy with minimal configuration
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "minimal-vlan-policy"
    state: present

- name: Delete a VLAN Policy
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "test-vlan-policy"
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "test_vlan_policy",
        "ObjectType": "fabric.EthNetworkPolicy",
        "Tags": [
            {
                "Key": "Site",
                "Value": "DataCenter-A"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
#from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec
import sys
sys.path.insert(1, '/home/rgershbu/Ansible-Content-Repos/intersight-ansible/')
from plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        vlans=dict(type='list', elements='dict', options=dict(
            prefix=dict(type='str', required=True),
            vlan_id=dict(type='int', required=True),
            auto_allow_on_uplinks=dict(type='bool', default=True),
            enable_sharing=dict(type='bool', default=False),
            multicast_policy_name=dict(type='str'),
            sharing_type=dict(type='str', choices=['Primary', 'Isolated', 'Community']),
            primary_vlan_id=dict(type='int')
        ))
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    
    # Resource path used to configure policy
    resource_path = '/fabric/EthNetworkPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name']
    }
    if intersight.module.params['state'] == 'present':
        if intersight.module.params['description']:
            intersight.api_body['Description'] = intersight.module.params['description']
        
        if intersight.module.params['tags']:
            intersight.api_body['Tags'] = intersight.module.params['tags']

    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)
    if intersight.module.params['state'] == 'present':
        vlan_policy_moid = intersight.result['api_response']['Moid']

    # Process VLANs if provided
    if intersight.module.params['state'] == 'present' and intersight.module.params['vlans']:
        # Cache for multicast policy MOIDs to avoid redundant API calls
        multicast_policy_cache = {}
        
        for vlan_config in intersight.module.params['vlans']:
            # Validate VLAN configuration
            prefix = vlan_config['prefix']
            vlan_id = vlan_config['vlan_id']
            auto_allow_on_uplinks = vlan_config.get('auto_allow_on_uplinks')
            enable_sharing = vlan_config.get('enable_sharing')
            
            # Generate VLAN name: prefix_vlan_id
            vlan_name = f"{prefix}_{vlan_id}"
            
            # Build base VLAN API body
            vlan_attach_api_body = {
                'Name': vlan_name,
                'VlanId': vlan_id,
                'AutoAllowOnUplinks': auto_allow_on_uplinks,
                'IsNative': False,
                'EthNetworkPolicy': vlan_policy_moid
            }
            
            # Handle sharing configuration
            if enable_sharing:
                sharing_type = vlan_config.get('sharing_type')
                vlan_attach_api_body['SharingType'] = sharing_type
                
                # If Isolated or Community, primary_vlan_id is required
                if sharing_type in ['Isolated', 'Community']:
                    if 'primary_vlan_id' not in vlan_config:
                        module.fail_json(msg=f"primary_vlan_id is required when sharing_type is {sharing_type}")
                    vlan_attach_api_body['PrimaryVlanId'] = vlan_config['primary_vlan_id']
                else:
                    vlan_attach_api_body['PrimaryVlanId'] = 0
            else:
                # No sharing, use multicast policy
                vlan_attach_api_body['SharingType'] = 'None'
                vlan_attach_api_body['PrimaryVlanId'] = 0
                
                # Get multicast policy name from vlan config
                multicast_policy_name = vlan_config.get('multicast_policy_name')
                if not multicast_policy_name:
                    module.fail_json(msg="multicast_policy_name is required when enable_sharing is false")
                
                # Check if multicast policy MOID is already cached
                if multicast_policy_name in multicast_policy_cache:
                    multicast_policy_moid = multicast_policy_cache[multicast_policy_name]
                    print(f"Using cached multicast policy MOID for '{multicast_policy_name}': {multicast_policy_moid}")
                else:
                    # Fetch multicast policy MOID and cache it
                    multicast_policy_moid = intersight.get_moid_by_value(resource_path='/fabric/MulticastPolicies', resource_value=multicast_policy_name)
                    multicast_policy_cache[multicast_policy_name] = multicast_policy_moid
                    print(f"Fetched and cached multicast policy MOID for '{multicast_policy_name}': {multicast_policy_moid}")
                
                vlan_attach_api_body['MulticastPolicy'] = multicast_policy_moid
            # Create the VLAN
            resource_path = '/fabric/Vlans'
            intersight.api_body = vlan_attach_api_body
            intersight.configure_vlans(resource_path=resource_path, vlan_name=vlan_name)
            print(f"Created VLAN: {vlan_name} with ID: {vlan_id}")


    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main() 