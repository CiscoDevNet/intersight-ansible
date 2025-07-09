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
short_description: Manage VLAN Policies and VLANs for Cisco Intersight
description:
  - Create, update, and delete VLAN Policies on Cisco Intersight.
  - Manage individual VLANs within VLAN policies.
  - Supports both regular VLANs and Private VLANs (Primary, Isolated, Community) configurations.
  - VLAN policies define network segmentation and can be attached to LAN Connectivity policies and Server Profiles.
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
      - Policies created within a Custom Organization are applicable only to devices in the same Organization.
      - Use 'default' for the default organization.
    type: str
    default: default
  name:
    description:
      - The name assigned to the VLAN Policy.
      - Must be unique within the organization.
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
      - Each VLAN will be named as C(prefix_vlan_id) (e.g., prod_100).
      - Leave empty to create a policy without VLANs for manual configuration later.
    type: list
    elements: dict
    suboptions:
      prefix:
        description:
          - Prefix for the VLAN name.
          - Combined with vlan_id to create the full VLAN name (prefix_vlan_id).
        type: str
        required: true
      vlan_id:
        description:
          - Enter a valid VLAN ID or ID range between 2 and 4093. You can enter a range of IDs using a hyphen,
            and you can enter multiple IDs or ID ranges separated by commas.
          - Examples of valid VLAN IDs or ID ranges are 50, 200, 2000-2100.
            You cannot use VLANs from 4043-4047, 4094, and 4095 because these IDs are reserved for system use.
          - You can create a maximum of 3000 VLANs at a time.
          - VLAN ID number (1-4094).
          - Must be unique within the fabric interconnect domain.
        type: int
        required: true
      is_native:
        description:
          - Whether this VLAN is the native VLAN for the fabric interconnect domain.
        type: bool
        default: false
      auto_allow_on_uplinks:
        description:
          - Whether to automatically allow this VLAN on uplinks.
        type: bool
        default: true
      enable_sharing:
        description:
          - When selected, enables Private VLAN sharing options.
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
          - The Primary VLAN ID of the VLAN, if the sharing type of the VLAN is Isolated or Community.
        type: int
      state:
        description:
          - Whether to create/update or delete the VLAN.
        type: str
        choices: ['present', 'absent']
        default: present
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a VLAN Policy with multiple VLANs
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "datacenter-vlan-policy"
    description: "VLAN policy for datacenter infrastructure"
    tags:
      - Key: "Environment"
        Value: "Production"
      - Key: "Site"
        Value: "DataCenter-A"
    vlans:
      - prefix: "prod"
        vlan_id: 100
        auto_allow_on_uplinks: true
        enable_sharing: false
        multicast_policy_name: "default-multicast-policy"
      - prefix: "dev"
        vlan_id: 200
        auto_allow_on_uplinks: false
        enable_sharing: false
        multicast_policy_name: "default-multicast-policy"
      - prefix: "mgmt"
        vlan_id: 300
        auto_allow_on_uplinks: true
        enable_sharing: false
        multicast_policy_name: "default-multicast-policy"
        is_native: true
    state: present

- name: Create a VLAN Policy with VLAN sharing (Private VLANs)
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "private-vlan-policy"
    description: "Policy with private VLAN configuration"
    vlans:
      - prefix: "primary"
        vlan_id: 79
        enable_sharing: true
        sharing_type: "Primary"
        auto_allow_on_uplinks: true
      - prefix: "isolated"
        vlan_id: 90
        enable_sharing: true
        sharing_type: "Isolated"
        primary_vlan_id: 79
        auto_allow_on_uplinks: true
      - prefix: "community"
        vlan_id: 91
        enable_sharing: true
        sharing_type: "Community"
        primary_vlan_id: 79
        auto_allow_on_uplinks: true
    state: present

- name: Create a VLAN Policy with mixed configurations
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "Engineering"
    name: "mixed-vlan-policy"
    description: "Mixed configuration with shared and non-shared VLANs"
    vlans:
      - prefix: "web"
        vlan_id: 10
        auto_allow_on_uplinks: true
        enable_sharing: false
        multicast_policy_name: "web-multicast-policy"
      - prefix: "db"
        vlan_id: 20
        auto_allow_on_uplinks: false
        enable_sharing: false
        state: absent
        multicast_policy_name: "db-multicast-policy"
      - prefix: "dmz_primary"
        vlan_id: 50
        enable_sharing: true
        sharing_type: "Primary"
        auto_allow_on_uplinks: true
        state: present
      - prefix: "dmz_isolated"
        vlan_id: 51
        enable_sharing: true
        sharing_type: "Isolated"
        primary_vlan_id: 50
        auto_allow_on_uplinks: true
    state: present

- name: Create a VLAN Policy with minimal configuration (policy only)
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "empty-vlan-policy"
    description: "Empty policy for manual VLAN configuration"
    state: present

- name: Update an existing VLAN Policy
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "datacenter-vlan-policy"
    description: "Updated description for datacenter infrastructure"
    tags:
      - Key: "Environment"
        Value: "Production"
      - Key: "Site"
        Value: "DataCenter-A"
      - Key: "Updated"
        Value: "2024-01-01"
    state: present

- name: Delete a VLAN Policy
  cisco.intersight.intersight_vlan_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "datacenter-vlan-policy"
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
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def save_changed_state_and_reset(intersight, changed_states):
    """
    Save the current changed state to the list and reset it for the next operation.
    Args:
        intersight: IntersightModule instance
        changed_states: List of changed states
    """
    changed_states.append(intersight.result['changed'])
    intersight.result['changed'] = False


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
            primary_vlan_id=dict(type='int'),
            is_native=dict(type='bool', default=False),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        ))
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    # Initialize structured response
    final_response = {
        'vlan_policy': {},
        'vlans': []
    }
    intersight.result['api_response'] = final_response
    intersight.result['trace_id'] = ''

    # Initialize list to track changed states from each API call
    changed_states = []

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

    intersight.configure_policy_or_profile(resource_path=resource_path)

    # Store the VLAN policy response
    final_response['vlan_policy'] = intersight.result['api_response']

    # Save the changed state and reset for next operation
    save_changed_state_and_reset(intersight, changed_states)

    vlan_policy_moid = None
    if intersight.module.params['state'] == 'present' and final_response['vlan_policy']:
        vlan_policy_moid = final_response['vlan_policy']['Moid']

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
            is_native = vlan_config.get('is_native')

            # Generate VLAN name: prefix_vlan_id
            vlan_name = f"{prefix}_{vlan_id}"

            # Build base VLAN API body
            vlan_attach_api_body = {
                'Name': vlan_name,
                'VlanId': vlan_id,
                'AutoAllowOnUplinks': auto_allow_on_uplinks,
                'IsNative': is_native,
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
                else:
                    # Fetch multicast policy MOID and cache it
                    multicast_policy_moid = intersight.get_moid_by_name(resource_path='/fabric/MulticastPolicies', resource_name=multicast_policy_name)
                    multicast_policy_cache[multicast_policy_name] = multicast_policy_moid

                vlan_attach_api_body['MulticastPolicy'] = multicast_policy_moid

            # Create the VLAN
            resource_path = '/fabric/Vlans'
            intersight.api_body = vlan_attach_api_body
            intersight.configure_secondary_resource(resource_path=resource_path, resource_name=vlan_name, state=vlan_config['state'])

            # Store the VLAN response
            final_response['vlans'].append(intersight.result['api_response'])

            # Save the changed state and reset for next operation
            save_changed_state_and_reset(intersight, changed_states)

    # Set the final structured response
    intersight.result['api_response'] = final_response

    # Set final changed state based on whether any operation resulted in a change
    intersight.result['changed'] = any(changed_states)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
