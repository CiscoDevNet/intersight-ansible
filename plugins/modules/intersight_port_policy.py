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
module: intersight_port_policy
short_description: Manage Port Policies for Cisco Intersight
description:
  - Create, update, and delete Port Policies on Cisco Intersight.
  - Manage port configurations including breakout ports, server roles, uplink port channels, and LAN pin groups.
  - Supports various device models with model-specific port configurations.
  - Port policies define the configuration of unified ports on fabric interconnects.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/fabric/PortPolicies/get/).
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
      - The name assigned to the Port Policy.
      - Must be unique within the organization.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description for the Port Policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  device_model:
    description:
      - The device model for which the Port Policy is intended.
      - Different models support different port configurations and capabilities.
    type: str
    choices: ['UCS-FI-6454', 'UCS-FI-64108', 'UCS-FI-6536', 'UCS-FI-6664', 'UCSX-S9108-100G']
    required: true
  fc_port_mode:
    description:
      - Configure Fibre Channel port mode for a range of ports.
      - This converts Ethernet ports to Fibre Channel ports.
      - Only one FC port mode configuration is allowed per policy.
    type: dict
    suboptions:
      port_id_start:
        description:
          - Starting port ID for FC mode configuration.
          - Must be 1 for FC port ranges.
        type: int
        default: 1
      port_id_end:
        description:
          - Ending port ID for FC mode configuration.
          - Valid values are 4, 8, 12, or 16.
        type: int
        choices: [4, 8, 12, 16]
        required: true
      state:
        description:
          - Whether to enable or disable FC port mode.
        type: str
        choices: ['present', 'absent']
        default: present
  breakout_ports:
    description:
      - List of breakout port configurations.
      - Breakout ports allow splitting a high-speed port into multiple lower-speed ports.
    type: list
    elements: dict
    suboptions:
      port_id_start:
        description:
          - Starting port ID for the breakout configuration.
        type: int
        required: true
      port_id_end:
        description:
          - Ending port ID for the breakout configuration.
        type: int
        required: true
      custom_mode:
        description:
          - Breakout mode for the ports.
        type: str
        choices: ['BreakoutEthernet10G', 'BreakoutEthernet25G']
        required: true
      state:
        description:
          - Whether to create/update or delete the breakout port configuration.
        type: str
        choices: ['present', 'absent']
        default: present
  server_ports:
    description:
      - List of server port configurations.
      - Server ports connect to server adapters.
    type: list
    elements: dict
    suboptions:
      port_id:
        description:
          - Port ID to configure as server port.
          - Can be a regular port (e.g., 49) or aggregate port (e.g., "49/2").
          - Aggregate ports use breakout port syntax where "49/2" means sub-port 2 of port 49.
        type: str
        required: true
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Cl74']
        default: 'Auto'
      auto_negotiation_disabled:
        description:
          - Disable auto-negotiation on the port.
        type: bool
        default: false
      user_label:
        description:
          - User-defined label for the port.
        type: str
      preferred_device_type:
        description:
          - Preferred device type when manual chassis/server numbering is enabled.
        type: str
        choices: ['Chassis', 'RackServer']
      preferred_device_id:
        description:
          - Preferred device ID when manual chassis/server numbering is enabled.
          - Required when preferred_device_type is specified.
        type: int
      state:
        description:
          - Whether to create/update or delete the server port configuration.
        type: str
        choices: ['present', 'absent']
        default: present
  ethernet_uplink_port_channels:
    description:
      - List of Ethernet uplink port channel configurations.
      - Port channels aggregate multiple Ethernet ports into a single logical link.
    type: list
    elements: dict
    suboptions:
      pc_id:
        description:
          - Port Channel Identifier.
        type: int
        required: true
      admin_speed:
        description:
          - Administrative speed of the port channel.
        type: str
        choices: ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps']
        default: 'Auto'
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Off']
        default: 'Auto'
      user_label:
        description:
          - User-defined label for the port channel.
        type: str
      ports:
        description:
          - List of Ethernet ports to include in the port channel.
        type: list
        elements: dict
        required: true
        suboptions:
          port_id:
            description:
              - Port ID to include in the port channel.
              - Can be a regular port (e.g., 36) or aggregate port (e.g., "49/2").
              - Aggregate ports use breakout port syntax where "49/2" means sub-port 2 of port 49.
            type: str
            required: true
          aggregate_port_id:
            description:
              - Aggregate port ID for breakout ports (legacy syntax).
              - Use the new "49/2" syntax in port_id instead.
            type: int
      eth_network_group_policy_names:
        description:
          - List of Ethernet Network Group Policy names to associate.
        type: list
        elements: str
      flow_control_policy_name:
        description:
          - Flow Control Policy name to associate.
        type: str
      link_aggregation_policy_name:
        description:
          - Link Aggregation Policy name to associate.
        type: str
      link_control_policy_name:
        description:
          - Link Control Policy name to associate.
        type: str
      state:
        description:
          - Whether to create/update or delete the port channel.
        type: str
        choices: ['present', 'absent']
        default: present
  fc_uplink_port_channels:
    description:
      - List of FC uplink port channel configurations.
      - Port channels aggregate multiple FC ports into a single logical link.
      - Only applicable when fc_port_mode is configured.
    type: list
    elements: dict
    suboptions:
      pc_id:
        description:
          - Port Channel Identifier.
        type: int
        required: true
      admin_speed:
        description:
          - Administrative speed of the FC port channel.
        type: str
        choices: ['8Gbps', '16Gbps', '32Gbps']
        default: '16Gbps'
      vsan_id:
        description:
          - VSAN ID for the FC port channel.
        type: int
        default: 1
      user_label:
        description:
          - User-defined label for the port channel.
        type: str
      ports:
        description:
          - List of FC ports to include in the port channel.
          - Ports must be within the FC port mode range.
        type: list
        elements: dict
        required: true
        suboptions:
          port_id:
            description:
              - FC port ID to include in the port channel.
            type: int
            required: true
      state:
        description:
          - Whether to create/update or delete the port channel.
        type: str
        choices: ['present', 'absent']
        default: present
  fcoe_uplink_port_channels:
    description:
      - List of FCoE uplink port channel configurations.
      - Port channels provide Fibre Channel over Ethernet connectivity.
    type: list
    elements: dict
    suboptions:
      pc_id:
        description:
          - Port Channel Identifier.
        type: int
        required: true
      admin_speed:
        description:
          - Administrative speed of the port channel.
        type: str
        choices: ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps']
        default: 'Auto'
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Off']
        default: 'Auto'
      user_label:
        description:
          - User-defined label for the port channel.
        type: str
      ports:
        description:
          - List of Ethernet ports to include in the port channel.
        type: list
        elements: dict
        required: true
        suboptions:
          port_id:
            description:
              - Port ID to include in the port channel.
              - Can be a regular port (e.g., 36) or aggregate port (e.g., "49/2").
              - Aggregate ports use breakout port syntax where "49/2" means sub-port 2 of port 49.
            type: str
            required: true
      link_aggregation_policy_name:
        description:
          - Link Aggregation Policy name to associate.
        type: str
      link_control_policy_name:
        description:
          - Link Control Policy name to associate.
        type: str
      state:
        description:
          - Whether to create/update or delete the port channel.
        type: str
        choices: ['present', 'absent']
        default: present
  appliance_port_channels:
    description:
      - List of appliance port channel configurations.
      - Port channels for direct-attached storage connectivity.
    type: list
    elements: dict
    suboptions:
      pc_id:
        description:
          - Port Channel Identifier.
        type: int
        required: true
      admin_speed:
        description:
          - Administrative speed of the port channel.
        type: str
        choices: ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps']
        default: 'Auto'
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Off']
        default: 'Auto'
      priority:
        description:
          - QoS priority for the appliance port channel.
        type: str
        choices: ['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze']
        default: 'Best Effort'
      mode:
        description:
          - Port mode for the appliance port channel.
        type: str
        choices: ['trunk', 'access']
        default: 'trunk'
      user_label:
        description:
          - User-defined label for the port channel.
        type: str
      ports:
        description:
          - List of Ethernet ports to include in the port channel.
        type: list
        elements: dict
        required: true
        suboptions:
          port_id:
            description:
              - Port ID to include in the port channel.
              - Can be a regular port (e.g., 36) or aggregate port (e.g., "49/2").
              - Aggregate ports use breakout port syntax where "49/2" means sub-port 2 of port 49.
            type: str
            required: true
      eth_network_group_policy_name:
        description:
          - Ethernet Network Group Policy name (required).
        type: str
        required: true
      eth_network_control_policy_name:
        description:
          - Ethernet Network Control Policy name (required).
        type: str
        required: true
      link_aggregation_policy_name:
        description:
          - Link Aggregation Policy name to associate.
        type: str
      state:
        description:
          - Whether to create/update or delete the port channel.
        type: str
        choices: ['present', 'absent']
        default: present
  lan_pin_groups:
    description:
      - List of LAN pin group configurations.
      - Pin groups control traffic distribution across uplinks.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Name of the LAN pin group.
        type: str
        required: true
      target_interface_role_type:
        description:
          - Type of target interface role.
        type: str
        choices: ['UplinkPcRole', 'UplinkRole']
        required: true
      target_interface_name:
        description:
          - Name or identifier of the target interface.
          - For UplinkPcRole, this should be the pc_id of an uplink port channel.
          - For UplinkRole, this should be the port identifier.
        type: str
        required: true
      state:
        description:
          - Whether to create/update or delete the LAN pin group.
        type: str
        choices: ['present', 'absent']
        default: present
  fc_uplink_ports:
    description:
      - List of FC Uplink port configurations.
      - FC Uplink ports are used for Fibre Channel connectivity to storage networks.
      - Only applicable when fc_port_mode is configured.
    type: list
    elements: dict
    suboptions:
      port_id:
        description:
          - Port ID to configure as FC Uplink.
          - Must be within the FC port mode range.
          - Can be a regular port (e.g., 1) or aggregate port (e.g., "49/1").
        type: str
        required: true
      admin_speed:
        description:
          - Administrative speed of the FC port.
        type: str
        choices: ['Auto', '8Gbps', '16Gbps', '32Gbps']
        default: 'Auto'
      vsan_id:
        description:
          - VSAN ID for the FC Uplink port.
        type: int
        required: true
      user_label:
        description:
          - User-defined label for the port.
        type: str
      state:
        description:
          - Whether to create/update or delete the FC Uplink port.
        type: str
        choices: ['present', 'absent']
        default: present
  fc_storage_ports:
    description:
      - List of FC Storage port configurations.
      - FC Storage ports are used for direct storage connectivity.
      - Only applicable when fc_port_mode is configured.
    type: list
    elements: dict
    suboptions:
      port_id:
        description:
          - Port ID to configure as FC Storage.
          - Must be within the FC port mode range.
          - Can be a regular port (e.g., 2) or aggregate port (e.g., "49/2").
        type: str
        required: true
      admin_speed:
        description:
          - Administrative speed of the FC port.
        type: str
        choices: ['Auto', '8Gbps', '16Gbps', '32Gbps']
        default: 'Auto'
      vsan_id:
        description:
          - VSAN ID for the FC Storage port.
        type: int
        required: true
      user_label:
        description:
          - User-defined label for the port.
        type: str
      state:
        description:
          - Whether to create/update or delete the FC Storage port.
        type: str
        choices: ['present', 'absent']
        default: present
  appliance_ports:
    description:
      - List of Appliance port configurations.
      - Appliance ports are used for direct-attached storage connectivity.
    type: list
    elements: dict
    suboptions:
      port_id:
        description:
          - Port ID to configure as Appliance port.
          - Can be a regular port (e.g., 13) or aggregate port (e.g., "49/1").
        type: str
        required: true
      admin_speed:
        description:
          - Administrative speed of the port.
          - 1Gbps only allowed for ports 45-48.
          - 40Gbps and 100Gbps only allowed for ports 49-54.
        type: str
        choices: ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps']
        default: 'Auto'
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Off']
        default: 'Auto'
      priority:
        description:
          - QoS priority for the appliance port.
        type: str
        choices: ['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze']
        default: 'Best Effort'
      mode:
        description:
          - Port mode for the appliance port.
        type: str
        choices: ['trunk', 'access']
        default: 'trunk'
      eth_network_group_policy_name:
        description:
          - Ethernet Network Group Policy name (required).
        type: str
        required: true
      eth_network_control_policy_name:
        description:
          - Ethernet Network Control Policy name (required).
        type: str
        required: true
      user_label:
        description:
          - User-defined label for the port.
        type: str
      state:
        description:
          - Whether to create/update or delete the appliance port.
        type: str
        choices: ['present', 'absent']
        default: present
  ethernet_uplink_ports:
    description:
      - List of Ethernet Uplink port configurations.
      - Ethernet Uplink ports connect to upstream network switches.
    type: list
    elements: dict
    suboptions:
      port_id:
        description:
          - Port ID to configure as Ethernet Uplink.
          - Can be a regular port (e.g., 14) or aggregate port (e.g., "49/1").
        type: str
        required: true
      admin_speed:
        description:
          - Administrative speed of the port.
          - Speed restrictions apply based on port numbers.
        type: str
        choices: ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps']
        default: 'Auto'
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Off']
        default: 'Auto'
      eth_network_group_policy_name:
        description:
          - List of Ethernet Network Group Policy names.
        type: list
        elements: str
      flow_control_policy_name:
        description:
          - Flow Control Policy name.
        type: str
      link_control_policy_name:
        description:
          - Link Control Policy name.
        type: str
      mac_sec_policy_name:
        description:
          - MAC Security Policy name.
        type: str
      user_label:
        description:
          - User-defined label for the port.
        type: str
      state:
        description:
          - Whether to create/update or delete the Ethernet Uplink port.
        type: str
        choices: ['present', 'absent']
        default: present
  fcoe_uplink_ports:
    description:
      - List of FCoE Uplink port configurations.
      - FCoE Uplink ports provide Fibre Channel over Ethernet connectivity.
    type: list
    elements: dict
    suboptions:
      port_id:
        description:
          - Port ID to configure as FCoE Uplink.
          - Can be a regular port (e.g., 15) or aggregate port (e.g., "49/1").
        type: str
        required: true
      admin_speed:
        description:
          - Administrative speed of the port.
        type: str
        choices: ['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps']
        default: 'Auto'
      fec:
        description:
          - Forward Error Correction (FEC) mode.
        type: str
        choices: ['Auto', 'Off']
        default: 'Auto'
      link_control_policy_name:
        description:
          - Link Control Policy name.
        type: str
      user_label:
        description:
          - User-defined label for the port.
        type: str
      state:
        description:
          - Whether to create/update or delete the FCoE Uplink port.
        type: str
        choices: ['present', 'absent']
        default: present
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a Port Policy with breakout ports and server ports
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "port-policy-example"
    description: "Example port policy with various configurations"
    device_model: "UCS-FI-6454"
    tags:
      - Key: "Environment"
        Value: "Production"
    breakout_ports:
      - port_id_start: 49
        port_id_end: 49
        custom_mode: "BreakoutEthernet25G"
        state: present
    server_ports:
      - port_id: 1
        fec: "Auto"
        auto_negotiation_disabled: false
        user_label: "Server Port 1"
        state: present
      - port_id: "49/2"
        fec: "Auto"
        auto_negotiation_disabled: false
        user_label: "Server Port Aggregate"
        state: present
    state: present

- name: Create a Port Policy with Ethernet uplink port channel
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "port-policy-with-pc"
    description: "Port policy with port channel configurations"
    device_model: "UCS-FI-6454"
    ethernet_uplink_port_channels:
      - pc_id: 123
        admin_speed: "25Gbps"
        fec: "Auto"
        user_label: "Uplink PC 123"
        ports:
          - port_id: 36
          - port_id: 37
          - port_id: "49/1"
          - port_id: "49/2"
        eth_network_group_policy_names:
          - "default-network-group"
        flow_control_policy_name: "default-flow-control"
        link_aggregation_policy_name: "default-link-aggregation"
        link_control_policy_name: "default-link-control"
        state: present
    state: present

- name: Create a Port Policy with FC uplink port channel
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "fc-port-channel-policy"
    device_model: "UCS-FI-6454"
    fc_port_mode:
      port_id_end: 8
      state: present
    fc_uplink_port_channels:
      - pc_id: 13
        admin_speed: "16Gbps"
        vsan_id: 1
        ports:
          - port_id: 1
          - port_id: 2
          - port_id: 3
          - port_id: 4
        state: present
    state: present

- name: Create a Port Policy with appliance port channel
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "appliance-pc-policy"
    device_model: "UCS-FI-6454"
    appliance_port_channels:
      - pc_id: 21
        admin_speed: "Auto"
        fec: "Auto"
        priority: "Best Effort"
        mode: "trunk"
        user_label: "Storage PC"
        ports:
          - port_id: 11
          - port_id: 12
        eth_network_group_policy_name: "storage-network-group"
        eth_network_control_policy_name: "storage-network-control"
        link_aggregation_policy_name: "default-link-aggregation"
        state: present
    state: present

- name: Create a Port Policy with LAN pin groups
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "port-policy-with-pin-groups"
    description: "Port policy with LAN pin group configuration"
    device_model: "UCS-FI-6454"
    ethernet_uplink_port_channels:
      - pc_id: 1
        admin_speed: "Auto"
        ports:
          - port_id: 53
          - port_id: 54
        state: present
    lan_pin_groups:
      - name: "pin-group-1"
        target_interface_role_type: "UplinkPcRole"
        target_interface_name: "1"
        state: present
    state: present

- name: Update Port Policy - manage resource states
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "port-policy-update"
    device_model: "UCS-FI-6454"
    server_ports:
      - port_id: 3
        user_label: "New Server Port"
        state: present
      - port_id: 4
        state: absent
    state: present

- name: Create a Port Policy with Fibre Channel ports 1-16
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "fc-port-policy"
    device_model: "UCS-FI-6454"
    fc_port_mode:
      port_id_end: 16
      state: present
    fc_uplink_ports:
      - port_id: 1
        admin_speed: "8Gbps"
        vsan_id: 2
        user_label: "FC Uplink 1"
        state: present
      - port_id: "49/1"
        admin_speed: "16Gbps"
        vsan_id: 3
        user_label: "FC Uplink Aggregate"
        state: present
    fc_storage_ports:
      - port_id: 2
        admin_speed: "8Gbps"
        vsan_id: 5
        user_label: "FC Storage 2"
        state: present
    state: present

- name: Create a Port Policy with Appliance and Ethernet Uplink ports
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "mixed-port-policy"
    device_model: "UCS-FI-6454"
    appliance_ports:
      - port_id: 13
        admin_speed: "10Gbps"
        fec: "Auto"
        priority: "Best Effort"
        mode: "trunk"
        eth_network_group_policy_name: "default-network-group"
        eth_network_control_policy_name: "default-network-control"
        user_label: "Storage Appliance"
        state: present
    ethernet_uplink_ports:
      - port_id: 14
        admin_speed: "Auto"
        fec: "Auto"
        eth_network_group_policy_name:
          - "default-network-group"
        flow_control_policy_name: "default-flow-control"
        link_control_policy_name: "default-link-control"
        state: present
    fcoe_uplink_ports:
      - port_id: 15
        admin_speed: "Auto"
        fec: "Auto"
        link_control_policy_name: "default-link-control"
        user_label: "FCoE Uplink"
        state: present
    state: present

- name: Delete a Port Policy
  cisco.intersight.intersight_port_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "port-policy-to-delete"
    device_model: "UCS-FI-6454"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "port-policy-example",
        "DeviceModel": "UCS-FI-6454",
        "ObjectType": "fabric.PortPolicy",
        "Tags": [
            {
                "Key": "Environment",
                "Value": "Production"
            }
        ],
        "BreakoutPorts": [
            {
                "SlotId": 1,
                "PortIdStart": 49,
                "PortIdEnd": 49,
                "CustomMode": "BreakoutEthernet25G"
            }
        ],
        "ServerPorts": [
            {
                "SlotId": 1,
                "PortId": 1,
                "Fec": "Auto",
                "UserLabel": "Server Port 1"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
#from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec
import sys
sys.path.insert(1, '/home/rgershbu/Ansible-Content-Repos/intersight-ansible/')
from plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def parse_port_id(port_input):
    """
    Parse port ID input to determine if it's a regular or aggregate port.
    
    Args:
        port_input: Port specification (int like 49 or string like "49/2")
        
    Returns:
        Dictionary with:
        - is_aggregate: Boolean indicating if it's an aggregate port
        - port_id: The port ID (2 for aggregate "49/2", 49 for regular 49)
        - aggregate_port_id: The aggregate port ID (49 for "49/2", None for regular)
        - display_name: Human readable name ("port49/2" or "port49")
    """
    if isinstance(port_input, str) and '/' in port_input:
        # Aggregate port syntax: "49/2"
        try:
            aggregate_port_str, port_str = port_input.split('/')
            aggregate_port_id = int(aggregate_port_str)
            port_id = int(port_str)
            
            # Validate aggregate port sub-port range (1-4)
            if not (1 <= port_id <= 4):
                raise ValueError(f"Aggregate port sub-port must be between 1-4, got {port_id}")
            
            return {
                'is_aggregate': True,
                'port_id': port_id,
                'aggregate_port_id': aggregate_port_id,
                'display_name': f"port{aggregate_port_id}/{port_id}"
            }
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid aggregate port format '{port_input}'. Expected format: '49/2'") from e
    else:
        # Regular port: just a number
        try:
            port_id = int(port_input)
            return {
                'is_aggregate': False,
                'port_id': port_id,
                'aggregate_port_id': None,
                'display_name': f"port{port_id}"
            }
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid port format '{port_input}'. Expected integer or 'X/Y' format") from e


def validate_breakout_port_config(module, breakout_config):
    """
    Validate breakout port configuration.
    
    Args:
        module: AnsibleModule instance
        breakout_config: Dictionary containing breakout port configuration
    """
    port_id_start = breakout_config.get('port_id_start')
    port_id_end = breakout_config.get('port_id_end')
    
    if port_id_start and port_id_end:
        if port_id_start > port_id_end:
            module.fail_json(msg=f"port_id_start ({port_id_start}) cannot be greater than port_id_end ({port_id_end})")


def validate_uplink_port_channel_config(module, pc_config):
    """
    Validate uplink port channel configuration.
    
    Args:
        module: AnsibleModule instance
        pc_config: Dictionary containing port channel configuration
    """
    ports = pc_config.get('ports', [])
    
    if not ports:
        module.fail_json(msg=f"At least one port must be specified for port channel {pc_config.get('pc_id')}")
    
    port_ids = [p['port_id'] for p in ports]
    if len(port_ids) != len(set(port_ids)):
        module.fail_json(msg=f"Duplicate ports found in port channel {pc_config.get('pc_id')}")


def validate_port_id_uniqueness(module):
    """
    Validate that port IDs don't overlap across different port types.
    Handles both regular ports and aggregate ports properly.
    
    Args:
        module: AnsibleModule instance
    """
    # Separate lists for regular ports and aggregate ports
    regular_ports = []  # Regular port IDs (e.g., 49)
    aggregate_ports = []  # Aggregate port strings (e.g., "port49/2")
    aggregate_base_ports = set()  # Base ports used for aggregation (e.g., 49)
    
    # Add FC port mode range
    fc_port_mode = module.params.get('fc_port_mode')
    if fc_port_mode and fc_port_mode.get('state', 'present') == 'present':
        port_start = fc_port_mode.get('port_id_start', 1)
        port_end = fc_port_mode['port_id_end']
        regular_ports.extend(range(port_start, port_end + 1))
    
    def add_port_to_lists(port_input):
        """Helper to add port to appropriate list based on type."""
        try:
            port_info = parse_port_id(port_input)
            if port_info['is_aggregate']:
                aggregate_ports.append(port_info['display_name'])
                # Track the base port used for aggregation
                aggregate_base_ports.add(port_info['aggregate_port_id'])
            else:
                regular_ports.append(port_info['port_id'])
        except ValueError as e:
            module.fail_json(msg=f"Invalid port specification: {e}")
    
    # Add all port role configurations
    port_role_configs = [
        ('server_ports', module.params.get('server_ports', [])),
        ('fc_uplink_ports', module.params.get('fc_uplink_ports', [])),
        ('fc_storage_ports', module.params.get('fc_storage_ports', [])),
        ('appliance_ports', module.params.get('appliance_ports', [])),
        ('ethernet_uplink_ports', module.params.get('ethernet_uplink_ports', [])),
        ('fcoe_uplink_ports', module.params.get('fcoe_uplink_ports', []))
    ]
    
    for _, port_configs in port_role_configs:
        for port_config in port_configs:
            if port_config.get('state', 'present') == 'present':
                add_port_to_lists(port_config['port_id'])
    
    # Add port channel member ports (can be regular or aggregate)
    # TODO: Note to myself, please don't remove it or take it into account for now - I will need to handle port channel for aggregation in specific hardware.
    def add_port_channel_ports(port_channels):
        """Helper function to add port channel ports to appropriate lists."""
        for pc_config in port_channels:
            if pc_config.get('state', 'present') == 'present':
                ports = pc_config.get('ports', [])
                for port in ports:
                    port_id = port['port_id']
                    aggregate_port_id = port.get('aggregate_port_id')
                    
                    if aggregate_port_id:
                        # Legacy syntax: aggregate_port_id specified separately
                        aggregate_ports.append(f"port{aggregate_port_id}/{port_id}")
                        # Track the base port used for aggregation
                        aggregate_base_ports.add(aggregate_port_id)
                    else:
                        # New syntax: port_id can be "49/2" format or regular
                        add_port_to_lists(port_id)
    
    # Add all port channel types
    add_port_channel_ports(module.params.get('ethernet_uplink_port_channels', []))
    add_port_channel_ports(module.params.get('fc_uplink_port_channels', []))
    add_port_channel_ports(module.params.get('fcoe_uplink_port_channels', []))
    add_port_channel_ports(module.params.get('appliance_port_channels', []))
    
    # Add breakout port ranges (these create the base ports for aggregation)
    breakout_ports = module.params.get('breakout_ports', [])
    for breakout_config in breakout_ports:
        if breakout_config.get('state', 'present') == 'present':
            port_start = breakout_config['port_id_start']
            port_end = breakout_config['port_id_end']
            # Breakout ports become aggregate base ports, not regular ports
            aggregate_base_ports.update(range(port_start, port_end + 1))
    
    def find_duplicates(port_list):
        """Helper function to find duplicates in a list."""
        if len(port_list) == len(set(port_list)):
            return []
        
        duplicates = []
        unique_items = set(port_list)
        for item in unique_items:
            if port_list.count(item) > 1:
                duplicates.append(item)
        return duplicates
    
    # Check for duplicates in both port lists
    regular_duplicates = find_duplicates(regular_ports)
    aggregate_duplicates = find_duplicates(aggregate_ports)
    
    # Check for conflicts between regular ports and aggregate base ports
    regular_ports_set = set(regular_ports)
    base_regular_conflicts = regular_ports_set.intersection(aggregate_base_ports)
    
    # Report conflicts
    conflicts = []
    if regular_duplicates:
        regular_conflict_str = ', '.join(map(str, sorted(regular_duplicates)))
        conflicts.append(f"Regular ports: {regular_conflict_str}")
    
    if aggregate_duplicates:
        aggregate_conflict_str = ', '.join(sorted(aggregate_duplicates))
        conflicts.append(f"Aggregate ports: {aggregate_conflict_str}")
    
    if base_regular_conflicts:
        base_conflict_str = ', '.join(map(str, sorted(base_regular_conflicts)))
        conflicts.append(f"Ports used as both regular and aggregate base: {base_conflict_str}")
    
    if conflicts:
        conflict_message = "Port ID conflicts detected. The following ports are assigned multiple roles:\n" + '\n'.join(conflicts)
        module.fail_json(msg=conflict_message)


def validate_fc_port_constraints(module):
    """
    Validate FC port constraints.
    
    Args:
        module: AnsibleModule instance
    """
    fc_port_mode = module.params.get('fc_port_mode')
    fc_uplink_ports = module.params.get('fc_uplink_ports', [])
    fc_storage_ports = module.params.get('fc_storage_ports', [])
    
    # If FC ports are configured, FC mode must be enabled
    if (fc_uplink_ports or fc_storage_ports) and (not fc_port_mode or fc_port_mode.get('state') != 'present'):
        module.fail_json(msg="fc_port_mode must be configured with state 'present' when FC uplink or storage ports are specified")
    
    # If FC mode is configured, validate FC port IDs are within range
    if fc_port_mode and fc_port_mode.get('state', 'present') == 'present':
        port_start = fc_port_mode.get('port_id_start', 1)
        port_end = fc_port_mode['port_id_end']
        
        def validate_fc_port_range(fc_configs, port_type):
            """Helper function to validate FC ports are within FC port mode range."""
            for fc_config in fc_configs:
                if fc_config.get('state', 'present') == 'present':
                    try:
                        port_info = parse_port_id(fc_config['port_id'])
                        # For aggregate ports, check the base port; for regular ports, check the port itself
                        check_port = port_info['aggregate_port_id'] if port_info['is_aggregate'] else port_info['port_id']
                        if check_port < port_start or check_port > port_end:
                            module.fail_json(
                                msg=f"{port_type} port {fc_config['port_id']} is outside the FC port mode range ({port_start}-{port_end})"
                            )
                    except ValueError as e:
                        module.fail_json(msg=f"Invalid {port_type} port specification: {e}")
        
        # Validate both FC port types
        validate_fc_port_range(fc_uplink_ports, "FC Uplink")
        validate_fc_port_range(fc_storage_ports, "FC Storage")


def validate_server_port_constraints(module):
    """
    Validate server port specific constraints.
    
    Args:
        module: AnsibleModule instance
    """
    server_ports = module.params.get('server_ports', [])
    
    for server_config in server_ports:
        if server_config.get('state', 'present') == 'present':
            preferred_device_type = server_config.get('preferred_device_type')
            preferred_device_id = server_config.get('preferred_device_id')
            
            # If preferred_device_type is specified, preferred_device_id is required
            if preferred_device_type and not preferred_device_id:
                module.fail_json(
                    msg=f"preferred_device_id is required when preferred_device_type is specified for server port {server_config['port_id']}"
                )
            
            # If preferred_device_id is specified, preferred_device_type is required
            if preferred_device_id and not preferred_device_type:
                module.fail_json(
                    msg=f"preferred_device_type is required when preferred_device_id is specified for server port {server_config['port_id']}"
                )


def validate_appliance_port_constraints(module):
    """
    Validate appliance port specific constraints.
    
    Args:
        module: AnsibleModule instance
    """
    appliance_ports = module.params.get('appliance_ports', [])
    
    for appliance_config in appliance_ports:
        if appliance_config.get('state', 'present') == 'present':
            try:
                port_info = parse_port_id(appliance_config['port_id'])
                # For aggregate ports, check the base port; for regular ports, check the port itself
                check_port = port_info['aggregate_port_id'] if port_info['is_aggregate'] else port_info['port_id']
                admin_speed = appliance_config.get('admin_speed', 'Auto')
                
                # Validate speed restrictions based on port numbers
                if admin_speed == '1Gbps' and not (45 <= check_port <= 48):
                    module.fail_json(
                        msg=f"1Gbps speed is only allowed for ports 45-48, but port {appliance_config['port_id']} was specified"
                    )
                
                if admin_speed in ['40Gbps', '100Gbps'] and not (49 <= check_port <= 54):
                    module.fail_json(
                        msg=f"{admin_speed} speed is only allowed for ports 49-54, but port {appliance_config['port_id']} was specified"
                    )
            except ValueError as e:
                module.fail_json(msg=f"Invalid Appliance port specification: {e}")


def validate_input(module):
    """
    Validate module input parameters.
    
    Args:
        module: AnsibleModule instance
    """
    # Validate port ID uniqueness across all port types
    validate_port_id_uniqueness(module)
    
    # Validate FC port constraints
    validate_fc_port_constraints(module)
    
    # Validate server port constraints
    validate_server_port_constraints(module)
    
    # Validate appliance port constraints
    validate_appliance_port_constraints(module)
    
    # Validate breakout port configurations
    breakout_ports = module.params.get('breakout_ports', [])
    for breakout_config in breakout_ports:
        if breakout_config.get('state', 'present') == 'present':
            validate_breakout_port_config(module, breakout_config)
    
    # Validate uplink port channel configurations
    uplink_port_channels = module.params.get('uplink_port_channels', [])
    for pc_config in uplink_port_channels:
        if pc_config.get('state', 'present') == 'present':
            validate_uplink_port_channel_config(module, pc_config)


def resolve_policy_moid(intersight, policy_cache, resource_path, policy_name, policy_type):
    """
    Resolve policy name to MOID with caching.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        resource_path: API resource path for the policy
        policy_name: Name of the policy to resolve
        policy_type: Type of policy for error messages
        
    Returns:
        MOID of the policy or None if not found
    """
    cache_key = f"{resource_path}:{policy_name}"
    
    if cache_key in policy_cache:
        return policy_cache[cache_key]
    
    moid = intersight.get_moid_by_name(
        resource_path=resource_path,
        resource_name=policy_name
    )
    
    if not moid:
        intersight.module.fail_json(msg=f"{policy_type} '{policy_name}' not found")
    
    policy_cache[cache_key] = moid
    return moid


def configure_generic_ports(intersight, policy_cache, port_policy_moid, port_configs, 
                           build_func, resource_path, requires_policy_cache=True):
    """
    Generic function to configure individual ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        port_policy_moid: MOID of the port policy
        port_configs: List of port configurations
        build_func: Function to build the API body
        resource_path: API resource path
        requires_policy_cache: Whether the build function requires policy cache
    """
    for port_config in port_configs:
        port_state = port_config.get('state', 'present')
        
        if port_state == 'present':
            # Build API body using the provided build function
            if requires_policy_cache:
                intersight.api_body = build_func(intersight, policy_cache, port_config, port_policy_moid)
            else:
                intersight.api_body = build_func(port_config, port_policy_moid)
            
            # Generate resource name using port_id
            port_info = parse_port_id(port_config['port_id'])
            resource_name = f"slot1_{port_info['display_name']}"
        else:
            # For deletion, we only need the resource name
            port_info = parse_port_id(port_config['port_id'])
            resource_name = f"slot1_{port_info['display_name']}"
        
        # Configure the port
        intersight.configure_secondary_resource(
            resource_path=resource_path,
            resource_name=resource_name,
            state=port_state
        )


def resolve_optional_policies(intersight, policy_cache, config, api_body, policy_mappings):
    """
    Generic helper to resolve optional policy MOIDs and add them to API body.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary to cache policy MOIDs
        config: Configuration dictionary containing policy names
        api_body: API body dictionary to update
        policy_mappings: Dictionary mapping config keys to (api_field, resource_path, display_name)
    """
    for config_key, (api_field, resource_path, display_name) in policy_mappings.items():
        if config.get(config_key):
            api_body[api_field] = resolve_policy_moid(
                intersight, policy_cache,
                resource_path,
                config[config_key],
                display_name
            )


def build_breakout_port_api_body(breakout_config, port_policy_moid):
    """
    Build API body for breakout port configuration.
    
    Args:
        breakout_config: Dictionary containing breakout port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    return {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortIdStart': breakout_config['port_id_start'],
        'PortIdEnd': breakout_config['port_id_end'],
        'CustomMode': breakout_config['custom_mode']
    }


def build_server_port_api_body(server_config, port_policy_moid):
    """
    Build API body for server port configuration.
    
    Args:
        server_config: Dictionary containing server port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    # Parse port ID to handle aggregate ports
    port_info = parse_port_id(server_config['port_id'])
    
    api_body = {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortId': port_info['port_id'],
        'Fec': server_config.get('fec', 'Auto'),
        'AutoNegotiationDisabled': server_config.get('auto_negotiation_disabled', False)
    }
    
    # Add aggregate port ID if this is an aggregate port
    if port_info['is_aggregate']:
        api_body['AggregatePortId'] = port_info['aggregate_port_id']
    
    if server_config.get('user_label'):
        api_body['UserLabel'] = server_config['user_label']
    
    # Add preferred device configuration if specified
    if server_config.get('preferred_device_type'):
        api_body['PreferredDeviceType'] = server_config['preferred_device_type']
        if server_config.get('preferred_device_id'):
            api_body['PreferredDeviceId'] = server_config['preferred_device_id']
    
    return api_body


def build_port_channel_ports_list(ports):
    """
    Build the Ports list for port channel API body.
    
    Args:
        ports: List of port configurations with port_id
        
    Returns:
        List of formatted port dictionaries
    """
    port_list = []
    for port in ports:
        port_input = port['port_id']
        
        port_info = parse_port_id(port_input)
        port_entry = {
            'PortId': port_info['port_id'],
            'SlotId': 1,
            'id': port_info['display_name']
        }
        
        if port_info['is_aggregate']:
            port_entry['AggregatePortId'] = port_info['aggregate_port_id']
        
        port_list.append(port_entry)
    
    return port_list


def build_ethernet_uplink_pc_api_body(intersight, policy_cache, pc_config, port_policy_moid):
    """
    Build API body for Ethernet uplink port channel configuration.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        pc_config: Dictionary containing port channel configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    api_body = {
        'PortPolicy': port_policy_moid,
        'PcId': pc_config['pc_id'],
        'AdminSpeed': pc_config.get('admin_speed', 'Auto'),
        'Fec': pc_config.get('fec', 'Auto'),
        'Ports': build_port_channel_ports_list(pc_config.get('ports', []))
    }
    
    if pc_config.get('user_label'):
        api_body['UserLabel'] = pc_config['user_label']
    
    # Resolve Ethernet Network Group Policy MOIDs
    if pc_config.get('eth_network_group_policy_names'):
        eth_network_group_moids = []
        for policy_name in pc_config['eth_network_group_policy_names']:
            moid = resolve_policy_moid(
                intersight, policy_cache,
                '/fabric/EthNetworkGroupPolicies',
                policy_name,
                'Ethernet Network Group Policy'
            )
            eth_network_group_moids.append(moid)
        api_body['EthNetworkGroupPolicy'] = eth_network_group_moids
    
    # Resolve optional policies using generic helper
    policy_mappings = {
        'flow_control_policy_name': ('FlowControlPolicy', '/fabric/FlowControlPolicies', 'Flow Control Policy'),
        'link_aggregation_policy_name': ('LinkAggregationPolicy', '/fabric/LinkAggregationPolicies', 'Link Aggregation Policy'),
        'link_control_policy_name': ('LinkControlPolicy', '/fabric/LinkControlPolicies', 'Link Control Policy')
    }
    
    resolve_optional_policies(intersight, policy_cache, pc_config, api_body, policy_mappings)
    
    return api_body


def build_fc_uplink_pc_api_body(pc_config, port_policy_moid):
    """
    Build API body for FC uplink port channel configuration.
    
    Args:
        pc_config: Dictionary containing port channel configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    api_body = {
        'PortPolicy': port_policy_moid,
        'PcId': pc_config['pc_id'],
        'AdminSpeed': pc_config.get('admin_speed', '16Gbps'),
        'VsanId': pc_config.get('vsan_id', 1),
        'Ports': build_port_channel_ports_list(pc_config.get('ports', []))
    }
    
    if pc_config.get('user_label'):
        api_body['UserLabel'] = pc_config['user_label']
    
    return api_body


def build_fcoe_uplink_pc_api_body(intersight, policy_cache, pc_config, port_policy_moid):
    """
    Build API body for FCoE uplink port channel configuration.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        pc_config: Dictionary containing port channel configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    api_body = {
        'PortPolicy': port_policy_moid,
        'PcId': pc_config['pc_id'],
        'AdminSpeed': pc_config.get('admin_speed', 'Auto'),
        'Fec': pc_config.get('fec', 'Auto'),
        'Ports': build_port_channel_ports_list(pc_config.get('ports', []))
    }
    
    if pc_config.get('user_label'):
        api_body['UserLabel'] = pc_config['user_label']
    
    # Resolve optional policies using generic helper
    policy_mappings = {
        'link_aggregation_policy_name': ('LinkAggregationPolicy', '/fabric/LinkAggregationPolicies', 'Link Aggregation Policy'),
        'link_control_policy_name': ('LinkControlPolicy', '/fabric/LinkControlPolicies', 'Link Control Policy')
    }
    
    resolve_optional_policies(intersight, policy_cache, pc_config, api_body, policy_mappings)
    
    return api_body


def build_appliance_pc_api_body(intersight, policy_cache, pc_config, port_policy_moid):
    """
    Build API body for appliance port channel configuration.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        pc_config: Dictionary containing port channel configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    api_body = {
        'PortPolicy': port_policy_moid,
        'PcId': pc_config['pc_id'],
        'AdminSpeed': pc_config.get('admin_speed', 'Auto'),
        'Fec': pc_config.get('fec', 'Auto'),
        'Priority': pc_config.get('priority', 'Best Effort'),
        'Mode': pc_config.get('mode', 'trunk'),
        'Ports': build_port_channel_ports_list(pc_config.get('ports', []))
    }
    
    if pc_config.get('user_label'):
        api_body['UserLabel'] = pc_config['user_label']
    
    # Resolve policies using generic helper
    policy_mappings = {
        'eth_network_group_policy_name': ('EthNetworkGroupPolicy', '/fabric/EthNetworkGroupPolicies', 'Ethernet Network Group Policy'),
        'eth_network_control_policy_name': ('EthNetworkControlPolicy', '/fabric/EthNetworkControlPolicies', 'Ethernet Network Control Policy'),
        'link_aggregation_policy_name': ('LinkAggregationPolicy', '/fabric/LinkAggregationPolicies', 'Link Aggregation Policy')
    }
    
    resolve_optional_policies(intersight, policy_cache, pc_config, api_body, policy_mappings)
    
    return api_body


def build_lan_pin_group_api_body(intersight, pin_group_config, port_policy_moid, uplink_pc_moids):
    """
    Build API body for LAN pin group configuration.
    
    Args:
        intersight: IntersightModule instance
        pin_group_config: Dictionary containing pin group configuration
        port_policy_moid: MOID of the port policy
        uplink_pc_moids: Dictionary mapping pc_id to MOID
        
    Returns:
        Dictionary containing the API body
    """
    api_body = {
        'PortPolicy': port_policy_moid,
        'Name': pin_group_config['name']
    }
    
    # Determine the target interface role
    target_type = pin_group_config['target_interface_role_type']
    target_name = pin_group_config['target_interface_name']
    
    if target_type == 'UplinkPcRole':
        # Look up the MOID for the uplink port channel
        pc_id = int(target_name)
        if pc_id not in uplink_pc_moids:
            intersight.module.fail_json(
                msg=f"Uplink port channel with pc_id {pc_id} not found for pin group '{pin_group_config['name']}'"
            )
        api_body['PinTargetInterfaceRole'] = {
            'ObjectType': 'fabric.UplinkPcRole',
            'Moid': uplink_pc_moids[pc_id]
        }
    else:
        # For UplinkRole, we'll need to implement this when we add uplink port support
        intersight.module.fail_json(
            msg=f"UplinkRole target type not yet implemented for pin group '{pin_group_config['name']}'"
        )
    
    return api_body


def build_fc_port_mode_api_body(fc_config, port_policy_moid):
    """
    Build API body for FC port mode configuration.
    
    Args:
        fc_config: Dictionary containing FC port mode configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    return {
        'PortPolicy': port_policy_moid,
        'PortIdStart': fc_config.get('port_id_start', 1),
        'PortIdEnd': fc_config['port_id_end'],
        'SlotId': 1
    }


def build_fc_uplink_port_api_body(fc_config, port_policy_moid):
    """
    Build API body for FC Uplink port configuration.
    
    Args:
        fc_config: Dictionary containing FC Uplink port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    # Parse port ID to handle aggregate ports
    port_info = parse_port_id(fc_config['port_id'])
    
    api_body = {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortId': port_info['port_id'],
        'AdminSpeed': fc_config.get('admin_speed', 'Auto'),
        'VsanId': fc_config['vsan_id']
    }
    
    # Add aggregate port ID if this is an aggregate port
    if port_info['is_aggregate']:
        api_body['AggregatePortId'] = port_info['aggregate_port_id']
    
    if fc_config.get('user_label'):
        api_body['UserLabel'] = fc_config['user_label']
    
    return api_body


def build_fc_storage_port_api_body(fc_config, port_policy_moid):
    """
    Build API body for FC Storage port configuration.
    
    Args:
        fc_config: Dictionary containing FC Storage port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    # Parse port ID to handle aggregate ports
    port_info = parse_port_id(fc_config['port_id'])
    
    api_body = {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortId': port_info['port_id'],
        'AdminSpeed': fc_config.get('admin_speed', 'Auto'),
        'VsanId': fc_config['vsan_id']
    }
    
    # Add aggregate port ID if this is an aggregate port
    if port_info['is_aggregate']:
        api_body['AggregatePortId'] = port_info['aggregate_port_id']
    
    if fc_config.get('user_label'):
        api_body['UserLabel'] = fc_config['user_label']
    
    return api_body


def build_appliance_port_api_body(intersight, policy_cache, appliance_config, port_policy_moid):
    """
    Build API body for Appliance port configuration.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        appliance_config: Dictionary containing Appliance port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    # Parse port ID to handle aggregate ports
    port_info = parse_port_id(appliance_config['port_id'])
    
    api_body = {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortId': port_info['port_id'],
        'AdminSpeed': appliance_config.get('admin_speed', 'Auto'),
        'Fec': appliance_config.get('fec', 'Auto'),
        'Priority': appliance_config.get('priority', 'Best Effort'),
        'Mode': appliance_config.get('mode', 'trunk')
    }
    
    # Add aggregate port ID if this is an aggregate port
    if port_info['is_aggregate']:
        api_body['AggregatePortId'] = port_info['aggregate_port_id']
    
    if appliance_config.get('user_label'):
        api_body['UserLabel'] = appliance_config['user_label']
    
    # Resolve policies using generic helper
    policy_mappings = {
        'eth_network_group_policy_name': ('EthNetworkGroupPolicy', '/fabric/EthNetworkGroupPolicies', 'Ethernet Network Group Policy'),
        'eth_network_control_policy_name': ('EthNetworkControlPolicy', '/fabric/EthNetworkControlPolicies', 'Ethernet Network Control Policy')
    }
    
    resolve_optional_policies(intersight, policy_cache, appliance_config, api_body, policy_mappings)
    
    return api_body


def build_ethernet_uplink_port_api_body(intersight, policy_cache, uplink_config, port_policy_moid):
    """
    Build API body for Ethernet Uplink port configuration.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        uplink_config: Dictionary containing Ethernet Uplink port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    # Parse port ID to handle aggregate ports
    port_info = parse_port_id(uplink_config['port_id'])
    
    api_body = {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortId': port_info['port_id'],
        'AdminSpeed': uplink_config.get('admin_speed', 'Auto'),
        'Fec': uplink_config.get('fec', 'Auto')
    }
    
    # Add aggregate port ID if this is an aggregate port
    if port_info['is_aggregate']:
        api_body['AggregatePortId'] = port_info['aggregate_port_id']
    
    if uplink_config.get('user_label'):
        api_body['UserLabel'] = uplink_config['user_label']
    
    # Resolve Ethernet Network Group Policy MOIDs
    if uplink_config.get('eth_network_group_policy_name'):
        eth_network_group_moids = []
        for policy_name in uplink_config['eth_network_group_policy_name']:
            moid = resolve_policy_moid(
                intersight, policy_cache,
                '/fabric/EthNetworkGroupPolicies',
                policy_name,
                'Ethernet Network Group Policy'
            )
            eth_network_group_moids.append(moid)
        api_body['EthNetworkGroupPolicy'] = eth_network_group_moids
    
    # Resolve single policies using generic helper
    policy_mappings = {
        'flow_control_policy_name': ('FlowControlPolicy', '/fabric/FlowControlPolicies', 'Flow Control Policy'),
        'link_control_policy_name': ('LinkControlPolicy', '/fabric/LinkControlPolicies', 'Link Control Policy'),
        'mac_sec_policy_name': ('MacSecPolicy', '/fabric/MacSecPolicies', 'MAC Security Policy')
    }
    
    resolve_optional_policies(intersight, policy_cache, uplink_config, api_body, policy_mappings)
    
    return api_body


def build_fcoe_uplink_port_api_body(intersight, policy_cache, fcoe_config, port_policy_moid):
    """
    Build API body for FCoE Uplink port configuration.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        fcoe_config: Dictionary containing FCoE Uplink port configuration
        port_policy_moid: MOID of the port policy
        
    Returns:
        Dictionary containing the API body
    """
    # Parse port ID to handle aggregate ports
    port_info = parse_port_id(fcoe_config['port_id'])
    
    api_body = {
        'PortPolicy': port_policy_moid,
        'SlotId': 1,
        'PortId': port_info['port_id'],
        'AdminSpeed': fcoe_config.get('admin_speed', 'Auto'),
        'Fec': fcoe_config.get('fec', 'Auto')
    }
    
    # Add aggregate port ID if this is an aggregate port
    if port_info['is_aggregate']:
        api_body['AggregatePortId'] = port_info['aggregate_port_id']
    
    if fcoe_config.get('user_label'):
        api_body['UserLabel'] = fcoe_config['user_label']
    
    # Resolve policies using generic helper
    policy_mappings = {
        'link_control_policy_name': ('LinkControlPolicy', '/fabric/LinkControlPolicies', 'Link Control Policy')
    }
    
    resolve_optional_policies(intersight, policy_cache, fcoe_config, api_body, policy_mappings)
    
    return api_body


def configure_breakout_ports(intersight, port_policy_moid, breakout_ports):
    """
    Configure breakout ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        port_policy_moid: MOID of the port policy
        breakout_ports: List of breakout port configurations
    """
    for breakout_config in breakout_ports:
        breakout_state = breakout_config.get('state', 'present')
        
        if breakout_state == 'present':
            # Build API body for breakout port
            intersight.api_body = build_breakout_port_api_body(breakout_config, port_policy_moid)
            
            # Create unique identifier for the breakout port (slot hardcoded to 1)
            resource_name = f"slot1_port{breakout_config['port_id_start']}-{breakout_config['port_id_end']}"
        else:
            # For deletion, we only need minimal information (slot hardcoded to 1)
            resource_name = f"slot1_port{breakout_config['port_id_start']}-{breakout_config['port_id_end']}"
        
        # Configure the breakout port
        intersight.configure_secondary_resource(
            resource_path='/fabric/PortModes',
            resource_name=resource_name,
            state=breakout_state
        )


def configure_server_ports(intersight, port_policy_moid, server_ports):
    """
    Configure server ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        port_policy_moid: MOID of the port policy
        server_ports: List of server port configurations
    """
    for server_config in server_ports:
        server_state = server_config.get('state', 'present')
        
        if server_state == 'present':
            # Build API body for server port
            intersight.api_body = build_server_port_api_body(server_config, port_policy_moid)
            
            # Create unique identifier for the server port (slot_id hardcoded to 1)
            port_info = parse_port_id(server_config['port_id'])
            resource_name = f"slot1_{port_info['display_name']}"
        else:
            # For deletion, we only need minimal information
            port_info = parse_port_id(server_config['port_id'])
            resource_name = f"slot1_{port_info['display_name']}"
        
        # Configure the server port
        intersight.configure_secondary_resource(
            resource_path='/fabric/ServerRoles',
            resource_name=resource_name,
            state=server_state
        )


def configure_generic_port_channels(intersight, policy_cache, port_policy_moid, port_channels, 
                                   build_func, resource_path, requires_policy_cache=True):
    """
    Generic function to configure port channels for the port policy.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        port_policy_moid: MOID of the port policy
        port_channels: List of port channel configurations
        build_func: Function to build the API body
        resource_path: API resource path
        requires_policy_cache: Whether the build function requires policy cache
        
    Returns:
        Dictionary mapping pc_id to MOID for created port channels
    """
    pc_moids = {}
    
    for pc_config in port_channels:
        pc_state = pc_config.get('state', 'present')
        pc_id = pc_config['pc_id']
        
        if pc_state == 'present':
            # Build API body using the provided build function
            if requires_policy_cache:
                intersight.api_body = build_func(intersight, policy_cache, pc_config, port_policy_moid)
            else:
                intersight.api_body = build_func(pc_config, port_policy_moid)
            
            # Create unique identifier for the port channel
            resource_name = f"pc{pc_id}"
        else:
            # For deletion, we only need minimal information
            resource_name = f"pc{pc_id}"
        
        # Configure the port channel
        intersight.configure_secondary_resource(
            resource_path=resource_path,
            resource_name=resource_name,
            state=pc_state
        )
        
        # Store the MOID if the port channel was created
        if pc_state == 'present' and intersight.result.get('api_response'):
            pc_moids[pc_id] = intersight.result['api_response'].get('Moid')
    
    return pc_moids


def configure_ethernet_uplink_port_channels(intersight, policy_cache, port_policy_moid, port_channels):
    """Configure Ethernet uplink port channels."""
    return configure_generic_port_channels(
        intersight, policy_cache, port_policy_moid, port_channels,
        build_ethernet_uplink_pc_api_body, '/fabric/UplinkPcRoles'
    )


def configure_fc_uplink_port_channels(intersight, port_policy_moid, port_channels):
    """Configure FC uplink port channels."""
    return configure_generic_port_channels(
        intersight, None, port_policy_moid, port_channels,
        build_fc_uplink_pc_api_body, '/fabric/FcUplinkPcRoles',
        requires_policy_cache=False
    )


def configure_fcoe_uplink_port_channels(intersight, policy_cache, port_policy_moid, port_channels):
    """Configure FCoE uplink port channels."""
    return configure_generic_port_channels(
        intersight, policy_cache, port_policy_moid, port_channels,
        build_fcoe_uplink_pc_api_body, '/fabric/FcoeUplinkPcRoles'
    )


def configure_appliance_port_channels(intersight, policy_cache, port_policy_moid, port_channels):
    """Configure appliance port channels."""
    return configure_generic_port_channels(
        intersight, policy_cache, port_policy_moid, port_channels,
        build_appliance_pc_api_body, '/fabric/AppliancePcRoles'
    )


def configure_lan_pin_groups(intersight, port_policy_moid, lan_pin_groups, uplink_pc_moids):
    """
    Configure LAN pin groups for the port policy.
    
    Args:
        intersight: IntersightModule instance
        port_policy_moid: MOID of the port policy
        lan_pin_groups: List of LAN pin group configurations
        uplink_pc_moids: Dictionary mapping pc_id to MOID
    """
    for pin_group_config in lan_pin_groups:
        pin_group_state = pin_group_config.get('state', 'present')
        
        if pin_group_state == 'present':
            # Build API body for LAN pin group
            intersight.api_body = build_lan_pin_group_api_body(
                intersight, pin_group_config, port_policy_moid, uplink_pc_moids
            )
            
            resource_name = pin_group_config['name']
        else:
            # For deletion, we only need the name
            resource_name = pin_group_config['name']
        
        # Configure the LAN pin group
        intersight.configure_secondary_resource(
            resource_path='/fabric/LanPinGroups',
            resource_name=resource_name,
            state=pin_group_state
        )


def configure_fc_port_mode(intersight, port_policy_moid, fc_port_mode):
    """
    Configure FC port mode for the port policy.
    
    Args:
        intersight: IntersightModule instance
        port_policy_moid: MOID of the port policy
        fc_port_mode: Dictionary containing FC port mode configuration
    """
    if not fc_port_mode:
        return
    
    fc_state = fc_port_mode.get('state', 'present')
    
    if fc_state == 'present':
        # Build API body for FC port mode
        intersight.api_body = build_fc_port_mode_api_body(fc_port_mode, port_policy_moid)
        
        # Create unique identifier for the FC port mode
        resource_name = f"fc_mode_1-{fc_port_mode['port_id_end']}"
    else:
        # For deletion, we only need minimal information
        resource_name = f"fc_mode_1-{fc_port_mode['port_id_end']}"
    
    # Configure the FC port mode
    intersight.configure_secondary_resource(
        resource_path='/fabric/PortModes',
        resource_name=resource_name,
        state=fc_state
    )


def configure_fc_uplink_ports(intersight, port_policy_moid, fc_uplink_ports):
    """
    Configure FC Uplink ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        port_policy_moid: MOID of the port policy
        fc_uplink_ports: List of FC Uplink port configurations
    """
    configure_generic_ports(
        intersight, None, port_policy_moid, fc_uplink_ports,
        build_fc_uplink_port_api_body, '/fabric/FcUplinkRoles',
        requires_policy_cache=False
    )


def configure_fc_storage_ports(intersight, port_policy_moid, fc_storage_ports):
    """
    Configure FC Storage ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        port_policy_moid: MOID of the port policy
        fc_storage_ports: List of FC Storage port configurations
    """
    configure_generic_ports(
        intersight, None, port_policy_moid, fc_storage_ports,
        build_fc_storage_port_api_body, '/fabric/FcStorageRoles',
        requires_policy_cache=False
    )


def configure_appliance_ports(intersight, policy_cache, port_policy_moid, appliance_ports):
    """
    Configure Appliance ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        port_policy_moid: MOID of the port policy
        appliance_ports: List of Appliance port configurations
    """
    configure_generic_ports(
        intersight, policy_cache, port_policy_moid, appliance_ports,
        build_appliance_port_api_body, '/fabric/ApplianceRoles',
        requires_policy_cache=True
    )


def configure_ethernet_uplink_ports(intersight, policy_cache, port_policy_moid, ethernet_uplink_ports):
    """
    Configure Ethernet Uplink ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        port_policy_moid: MOID of the port policy
        ethernet_uplink_ports: List of Ethernet Uplink port configurations
    """
    configure_generic_ports(
        intersight, policy_cache, port_policy_moid, ethernet_uplink_ports,
        build_ethernet_uplink_port_api_body, '/fabric/UplinkRoles',
        requires_policy_cache=True
    )


def configure_fcoe_uplink_ports(intersight, policy_cache, port_policy_moid, fcoe_uplink_ports):
    """
    Configure FCoE Uplink ports for the port policy.
    
    Args:
        intersight: IntersightModule instance
        policy_cache: Dictionary for caching policy MOIDs
        port_policy_moid: MOID of the port policy
        fcoe_uplink_ports: List of FCoE Uplink port configurations
    """
    configure_generic_ports(
        intersight, policy_cache, port_policy_moid, fcoe_uplink_ports,
        build_fcoe_uplink_port_api_body, '/fabric/FcoeUplinkRoles',
        requires_policy_cache=True
    )


def main():
    # Define FC port mode options
    fc_port_mode_options = dict(
        port_id_start=dict(type='int', default=1),
        port_id_end=dict(type='int', choices=[4, 8, 12, 16], required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define breakout port options
    breakout_port_options = dict(
        port_id_start=dict(type='int', required=True),
        port_id_end=dict(type='int', required=True),
        custom_mode=dict(type='str', choices=['BreakoutEthernet10G', 'BreakoutEthernet25G'], required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define server port options
    server_port_options = dict(
        port_id=dict(type='str', required=True),
        fec=dict(type='str', choices=['Auto', 'Cl74'], default='Auto'),
        auto_negotiation_disabled=dict(type='bool', default=False),
        user_label=dict(type='str'),
        preferred_device_type=dict(type='str', choices=['Chassis', 'RackServer']),
        preferred_device_id=dict(type='int'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define port options for port channels
    ethernet_port_options = dict(
        port_id=dict(type='str', required=True)
    )
    
    fc_port_options = dict(
        port_id=dict(type='str', required=True)
    )
    
    # Define Ethernet uplink port channel options
    ethernet_uplink_pc_options = dict(
        pc_id=dict(type='int', required=True),
        admin_speed=dict(type='str', choices=['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], default='Auto'),
        fec=dict(type='str', choices=['Auto', 'Off'], default='Auto'),
        user_label=dict(type='str'),
        ports=dict(type='list', elements='dict', options=ethernet_port_options, required=True),
        eth_network_group_policy_names=dict(type='list', elements='str'),
        flow_control_policy_name=dict(type='str'),
        link_aggregation_policy_name=dict(type='str'),
        link_control_policy_name=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define FC uplink port channel options
    fc_uplink_pc_options = dict(
        pc_id=dict(type='int', required=True),
        admin_speed=dict(type='str', choices=['8Gbps', '16Gbps', '32Gbps'], default='16Gbps'),
        vsan_id=dict(type='int', default=1),
        user_label=dict(type='str'),
        ports=dict(type='list', elements='dict', options=fc_port_options, required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define FCoE uplink port channel options
    fcoe_uplink_pc_options = dict(
        pc_id=dict(type='int', required=True),
        admin_speed=dict(type='str', choices=['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], default='Auto'),
        fec=dict(type='str', choices=['Auto', 'Off'], default='Auto'),
        user_label=dict(type='str'),
        ports=dict(type='list', elements='dict', options=ethernet_port_options, required=True),
        link_aggregation_policy_name=dict(type='str'),
        link_control_policy_name=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define Appliance port channel options
    appliance_pc_options = dict(
        pc_id=dict(type='int', required=True),
        admin_speed=dict(type='str', choices=['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], default='Auto'),
        fec=dict(type='str', choices=['Auto', 'Off'], default='Auto'),
        priority=dict(type='str', choices=['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze'], default='Best Effort'),
        mode=dict(type='str', choices=['trunk', 'access'], default='trunk'),
        user_label=dict(type='str'),
        ports=dict(type='list', elements='dict', options=ethernet_port_options, required=True),
        eth_network_group_policy_name=dict(type='str', required=True),
        eth_network_control_policy_name=dict(type='str', required=True),
        link_aggregation_policy_name=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define LAN pin group options
    lan_pin_group_options = dict(
        name=dict(type='str', required=True),
        target_interface_role_type=dict(type='str', choices=['UplinkPcRole', 'UplinkRole'], required=True),
        target_interface_name=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define FC Uplink port options
    fc_uplink_port_options = dict(
        port_id=dict(type='str', required=True),
        admin_speed=dict(type='str', choices=['Auto', '8Gbps', '16Gbps', '32Gbps'], default='Auto'),
        vsan_id=dict(type='int', required=True),
        user_label=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define FC Storage port options
    fc_storage_port_options = dict(
        port_id=dict(type='str', required=True),
        admin_speed=dict(type='str', choices=['Auto', '8Gbps', '16Gbps', '32Gbps'], default='Auto'),
        vsan_id=dict(type='int', required=True),
        user_label=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define Appliance port options
    appliance_port_options = dict(
        port_id=dict(type='str', required=True),
        admin_speed=dict(type='str', choices=['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], default='Auto'),
        fec=dict(type='str', choices=['Auto', 'Off'], default='Auto'),
        priority=dict(type='str', choices=['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze'], default='Best Effort'),
        mode=dict(type='str', choices=['trunk', 'access'], default='trunk'),
        eth_network_group_policy_name=dict(type='str', required=True),
        eth_network_control_policy_name=dict(type='str', required=True),
        user_label=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define Ethernet Uplink port options
    ethernet_uplink_port_options = dict(
        port_id=dict(type='str', required=True),
        admin_speed=dict(type='str', choices=['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], default='Auto'),
        fec=dict(type='str', choices=['Auto', 'Off'], default='Auto'),
        eth_network_group_policy_name=dict(type='list', elements='str'),
        flow_control_policy_name=dict(type='str'),
        link_control_policy_name=dict(type='str'),
        mac_sec_policy_name=dict(type='str'),
        user_label=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    # Define FCoE Uplink port options
    fcoe_uplink_port_options = dict(
        port_id=dict(type='str', required=True),
        admin_speed=dict(type='str', choices=['Auto', '1Gbps', '10Gbps', '25Gbps', '40Gbps', '100Gbps'], default='Auto'),
        fec=dict(type='str', choices=['Auto', 'Off'], default='Auto'),
        link_control_policy_name=dict(type='str'),
        user_label=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        device_model=dict(
            type='str',
            choices=['UCS-FI-6454', 'UCS-FI-64108', 'UCS-FI-6536', 'UCS-FI-6664', 'UCSX-S9108-100G'],
            required=True
        ),
        fc_port_mode=dict(type='dict', options=fc_port_mode_options),
        breakout_ports=dict(type='list', elements='dict', options=breakout_port_options),
        server_ports=dict(type='list', elements='dict', options=server_port_options),
        ethernet_uplink_port_channels=dict(type='list', elements='dict', options=ethernet_uplink_pc_options),
        fc_uplink_port_channels=dict(type='list', elements='dict', options=fc_uplink_pc_options),
        fcoe_uplink_port_channels=dict(type='list', elements='dict', options=fcoe_uplink_pc_options),
        appliance_port_channels=dict(type='list', elements='dict', options=appliance_pc_options),
        lan_pin_groups=dict(type='list', elements='dict', options=lan_pin_group_options),
        fc_uplink_ports=dict(type='list', elements='dict', options=fc_uplink_port_options),
        fc_storage_ports=dict(type='list', elements='dict', options=fc_storage_port_options),
        appliance_ports=dict(type='list', elements='dict', options=appliance_port_options),
        ethernet_uplink_ports=dict(type='list', elements='dict', options=ethernet_uplink_port_options),
        fcoe_uplink_ports=dict(type='list', elements='dict', options=fcoe_uplink_port_options)
    )
    
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )
    
    if module.params['state'] == 'present':
        validate_input(module)
    
    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    
    # Resource path used to configure policy
    resource_path = '/fabric/PortPolicies'
    
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name']
    }
    
    if intersight.module.params['state'] == 'present':
        intersight.set_tags_and_description()
        intersight.api_body['DeviceModel'] = intersight.module.params['device_model']

    
    # Configure the port policy
    intersight.configure_policy_or_profile(resource_path=resource_path)
    
    # Save the port policy response
    port_policy_response = intersight.result['api_response']
    
    port_policy_moid = None
    if intersight.module.params['state'] == 'present' and port_policy_response:
        port_policy_moid = port_policy_response.get('Moid')
    
    # Process secondary resources if port policy is present
    secondary_responses = {}
    if intersight.module.params['state'] == 'present' and port_policy_moid:
        # Cache for policy MOIDs to avoid redundant API calls
        policy_cache = {}
        
        # Configure FC port mode
        if intersight.module.params.get('fc_port_mode'):
            configure_fc_port_mode(
                intersight,
                port_policy_moid,
                intersight.module.params['fc_port_mode']
            )
            secondary_responses['fc_port_mode'] = intersight.result.get('api_response')
        
        # Configure breakout ports
        if intersight.module.params.get('breakout_ports'):
            configure_breakout_ports(
                intersight,
                port_policy_moid,
                intersight.module.params['breakout_ports']
            )
            secondary_responses['breakout_ports'] = intersight.result.get('api_response')
        
        # Configure server ports
        if intersight.module.params.get('server_ports'):
            configure_server_ports(
                intersight,
                port_policy_moid,
                intersight.module.params['server_ports']
            )
            secondary_responses['server_ports'] = intersight.result.get('api_response')
        
        # Configure FC Uplink ports
        if intersight.module.params.get('fc_uplink_ports'):
            configure_fc_uplink_ports(
                intersight,
                port_policy_moid,
                intersight.module.params['fc_uplink_ports']
            )
            secondary_responses['fc_uplink_ports'] = intersight.result.get('api_response')
        
        # Configure FC Storage ports
        if intersight.module.params.get('fc_storage_ports'):
            configure_fc_storage_ports(
                intersight,
                port_policy_moid,
                intersight.module.params['fc_storage_ports']
            )
            secondary_responses['fc_storage_ports'] = intersight.result.get('api_response')
        
        # Configure Appliance ports
        if intersight.module.params.get('appliance_ports'):
            configure_appliance_ports(
                intersight,
                policy_cache,
                port_policy_moid,
                intersight.module.params['appliance_ports']
            )
            secondary_responses['appliance_ports'] = intersight.result.get('api_response')
        
        # Configure Ethernet Uplink ports
        if intersight.module.params.get('ethernet_uplink_ports'):
            configure_ethernet_uplink_ports(
                intersight,
                policy_cache,
                port_policy_moid,
                intersight.module.params['ethernet_uplink_ports']
            )
            secondary_responses['ethernet_uplink_ports'] = intersight.result.get('api_response')
        
        # Configure FCoE Uplink ports
        if intersight.module.params.get('fcoe_uplink_ports'):
            configure_fcoe_uplink_ports(
                intersight,
                policy_cache,
                port_policy_moid,
                intersight.module.params['fcoe_uplink_ports']
            )
            secondary_responses['fcoe_uplink_ports'] = intersight.result.get('api_response')
        
        # Configure Ethernet uplink port channels and get their MOIDs
        uplink_pc_moids = {}
        if intersight.module.params.get('ethernet_uplink_port_channels'):
            ethernet_pc_moids = configure_ethernet_uplink_port_channels(
                intersight,
                policy_cache,
                port_policy_moid,
                intersight.module.params['ethernet_uplink_port_channels']
            )
            uplink_pc_moids.update(ethernet_pc_moids)
            secondary_responses['ethernet_uplink_port_channels'] = intersight.result.get('api_response')
        
        # Configure FC uplink port channels
        if intersight.module.params.get('fc_uplink_port_channels'):
            fc_pc_moids = configure_fc_uplink_port_channels(
                intersight,
                port_policy_moid,
                intersight.module.params['fc_uplink_port_channels']
            )
            uplink_pc_moids.update(fc_pc_moids)
            secondary_responses['fc_uplink_port_channels'] = intersight.result.get('api_response')
        
        # Configure FCoE uplink port channels
        if intersight.module.params.get('fcoe_uplink_port_channels'):
            fcoe_pc_moids = configure_fcoe_uplink_port_channels(
                intersight,
                policy_cache,
                port_policy_moid,
                intersight.module.params['fcoe_uplink_port_channels']
            )
            uplink_pc_moids.update(fcoe_pc_moids)
            secondary_responses['fcoe_uplink_port_channels'] = intersight.result.get('api_response')
        
        # Configure Appliance port channels
        if intersight.module.params.get('appliance_port_channels'):
            appliance_pc_moids = configure_appliance_port_channels(
                intersight,
                policy_cache,
                port_policy_moid,
                intersight.module.params['appliance_port_channels']
            )
            uplink_pc_moids.update(appliance_pc_moids)
            secondary_responses['appliance_port_channels'] = intersight.result.get('api_response')
        
        # Configure LAN pin groups (must be after all port channels)
        if intersight.module.params.get('lan_pin_groups'):
            configure_lan_pin_groups(
                intersight,
                port_policy_moid,
                intersight.module.params['lan_pin_groups'],
                uplink_pc_moids
            )
            secondary_responses['lan_pin_groups'] = intersight.result.get('api_response')
    
    # Combine port policy and secondary resources in the main response
    if port_policy_response:
        port_policy_response['secondary_resources'] = secondary_responses
        intersight.result['api_response'] = port_policy_response
    
    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
