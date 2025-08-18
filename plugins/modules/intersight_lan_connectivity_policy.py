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
module: intersight_lan_connectivity_policy
short_description: Manage LAN Connectivity Policies and vNICs for Cisco Intersight
description:
  - Create, update, and delete LAN Connectivity Policies on Cisco Intersight.
  - Manage individual vNICs within LAN Connectivity policies.
  - Supports both Standalone and FIAttached target platforms with different configuration options.
  - LAN Connectivity policies define network connectivity settings for server profiles.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/vnic/LanConnectivityPolicy/get/).
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
      - The name assigned to the LAN Connectivity Policy.
      - Must be unique within the organization.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description for the LAN Connectivity Policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  target_platform:
    description:
      - The platform type for which the LAN Connectivity policy is intended.
      - standalone for standalone servers, attached for fabric interconnect attached servers.
    type: str
    choices: ['standalone', 'attached']
    default: 'standalone'
  azure_qos_enabled:
    description:
      - Enable Azure QoS for the LAN Connectivity policy.
      - Only applicable when target_platform is 'attached'.
    type: bool
    default: false
  iqn_allocation_type:
    description:
      - IQN allocation type for the LAN Connectivity policy.
      - Only applicable when target_platform is 'attached'.
    type: str
    choices: ['None', 'Pool', 'Static']
    default: 'None'
  placement_mode:
    description:
      - Placement mode for vNIC assignment.
      - Only applicable when target_platform is 'attached'.
    type: str
    choices: ['custom', 'auto']
    default: 'custom'
  iqn_pool_name:
    description:
      - Relationship to the iSCSI Qualified Name Pool.
      - Required when iqn_allocation_type is 'Pool'.
      - Only applicable for attached target platform.
    type: str
  static_iqn_name:
    description:
      - User provided static iSCSI Qualified Name (IQN) for use as initiator identifiers by iSCSI vNICs in a Fabric Interconnect domain.
      - Required when iqn_allocation_type is 'Static'.
      - Only applicable for attached target platform.
    type: str
  vnics:
    description:
      - List of vNICs to be created and attached to the LAN Connectivity policy.
      - Each vNIC will be configured with the specified network and adapter policies.
      - Required when C(state) is C(present).
      - At least one vNIC must be specified for both Standalone and FIAttached platforms.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The name of the vNIC.
          - Must be unique within the LAN Connectivity policy.
        type: str
        required: true
      placement_slot_id:
        description:
          - PCIe Slot where the VIC adapter is installed.
          - Supported values are (1-15) and MLOM.
          - Required when vNIC state is 'present'.
        type: str
      pci_link:
        description:
          - The PCI Link used as transport for the virtual interface.
          - PCI Link is only applicable for select Cisco UCS VIC 1300 models (UCSC-PCIE-C40Q-03, UCSB-MLOM-40G-03, UCSB-VIC-M83-8P) that support two PCI links.
          - The value, if specified, for any other VIC model will be ignored.
        type: int
        choices: [0, 1]
        default: 0
      uplink_port:
        description:
          - Adapter port on which the virtual interface will be created.
        type: int
        choices: [0, 1, 2, 3]
        default: 0
      order:
        description:
          - The order in which the virtual interface is brought up.
          - The order assigned to an interface should be unique for all the Ethernet and Fibre-Channel interfaces on each PCI link on a VIC adapter.
          - The order should start from zero with no overlaps.
          - The maximum value of PCI order is limited by the number of virtual interfaces (Ethernet and Fibre-Channel) on each PCI link on a VIC adapter.
          - All VIC adapters have a single PCI link except VIC 1340, VIC 1380 and VIC 1385 which have two.
        type: int
        default: 0
      cdn_source:
        description:
          - Source of the CDN. It can either be user specified or be the same as the vNIC name.
        type: str
        choices: ['vnic', 'user']
        default: 'vnic'
      cdn_value:
        description:
          - CDN value when cdn_source is 'user'.
        type: str
      eth_network_policy_name:
        description:
          - Relationship to the Ethernet Network Policy.
          - Required when vNIC state is 'present'.
        type: str
      eth_qos_policy_name:
        description:
          - Relationship to the Ethernet QoS Policy.
          - Required when vNIC state is 'present'.
        type: str
      eth_adapter_policy_name:
        description:
          - Relationship to the Ethernet Adapter Policy.
          - Required when vNIC state is 'present'.
        type: str
      connection_type:
        description:
          - Type of connection for the vNIC.
        type: str
        choices: ['none', 'usnic', 'vmq', 'sriov']
        default: 'none'
      mac_address_type:
        description:
          - Type of MAC address assignment.
          - Only applicable for attached target platform.
        type: str
        choices: ['pool', 'static']
        default: 'pool'
      mac_pool_name:
        description:
          - The MAC pool that is assigned.
          - Required when mac_address_type is 'pool' and target platform is attached.
          - Only applicable for attached target platform.
        type: str
      static_mac_address:
        description:
          - The MAC address must be in hexadecimal format xx:xx:xx:xx:xx:xx.
          - To ensure uniqueness of MACs in the LAN fabric, you are strongly encouraged to use the following MAC prefix 00:25:B5:xx:xx:xx.
          - Required when mac_address_type is 'static' and target platform is attached.
          - Only applicable for attached target platform.
        type: str
      auto_slot_id:
        description:
          - Enable or disable automatic assignment of the VIC slot ID.
          - If enabled and the server has only one VIC, the same VIC is chosen for all the vNICs.
          - If enabled and the server has multiple VICs, the vNIC/vHBA are deployed on the first VIC.
          - Only applicable for attached target platform.
        type: bool
        default: true
      auto_pci_link:
        description:
          - Enable or disable automatic assignment of the PCI Link in a dual-link adapter.
          - This option applies only to 13xx series VICs that support dual-link.
          - If enabled, the system determines the placement of the vNIC/vHBA on either of the PCI Links.
          - Only applicable for attached target platform.
        type: bool
        default: true
      switch_id:
        description:
          - The fabric port to which the vNICs will be associated.
          - Only applicable for attached target platform.
        type: str
        choices: ['A', 'B']
        default: 'A'
      failover_enabled:
        description:
          - Enables automatic vNIC failover to the secondary Fabric Interconnect
            if the primary path fails.
          - Failover applies only to Cisco VICs that are connected to a Fabric Interconnect cluster.
          - Only applicable for attached target platform.
        type: bool
        default: false
      fabric_eth_network_group_policy_name:
        description:
          - Relationship to the Fabric Ethernet Group Policy.
          - Required when target platform is attached and vNIC state is 'present'.
          - Only applicable for attached target platform.
        type: str
      fabric_eth_network_control_policy_name:
        description:
          - Relationship to the Fabric Ethernet Network Policy.
          - Required when target platform is attached and vNIC state is 'present'.
          - Only applicable for attached target platform.
        type: str
      iscsi_boot_policy_name:
        description:
          - Relationship to the boot iSCSI Policy.
          - Only applicable for attached target platform.
        type: str
      usnic_settings:
        description:
          - USNIC settings when connection_type is 'usnic'.
          - Required when connection_type is 'usnic'.
        type: dict
        suboptions:
          count:
            description:
              - Number of usNIC interfaces to be created.
              - When usNIC is enabled, the valid values are from 1 to 225.
              - When usNIC is disabled, the default value is 0.
            type: int
            default: 0
          cos:
            description:
              - Class of Service to be used for traffic on the usNIC.
            type: int
            choices: [0, 1, 2, 3, 4, 5, 6]
            default: 5
          usnic_adapter_policy_name:
            description:
              - Ethernet Adapter policy to be associated with the usNICs.
              - Required when connection_type is 'usnic'.
            type: str
      vmq_settings:
        description:
          - VMQ settings when connection_type is 'vmq'.
        type: dict
        suboptions:
          enabled:
            description:
              - Enable VMQ.
            type: bool
            default: true
          multi_queue_support:
            description:
              - Enables Virtual Machine Multi-Queue feature on the virtual interface.
              - VMMQ allows configuration of multiple I/O queues for a single VM and thus distributes traffic across multiple CPU cores in a VM.
            type: bool
            default: false
          num_interrupts:
            description:
              - The number of interrupt resources to be allocated.
              - Recommended value is the number of CPU threads or logical processors available in the server.
            type: int
            default: 16
          num_vmqs:
            description:
              - The number of hardware Virtual Machine Queues to be allocated.
              - The number of VMQs per adapter must be one more than the maximum number of VM NICs.
            type: int
            default: 4
          num_sub_vnics:
            description:
              - Number of sub vNICs (0-64).
              - Only applicable when multi_queue_support is true.
            type: int
            default: 64
          vmmq_adapter_policy_name:
            description:
              - Name of the VMMQ Adapter Policy.
              - Only applicable when multi_queue_support is true.
            type: str
      sriov_settings:
        description:
          - SR-IOV settings when connection_type is 'sriov'.
        type: dict
        suboptions:
          enabled:
            description:
              - Enable SR-IOV.
            type: bool
            default: true
          vf_count:
            description:
              - Number of Virtual Functions (1-64).
            type: int
            default: 64
          rx_count_per_vf:
            description:
              - Receive Queue Count per VF (1-8).
            type: int
            default: 4
          tx_count_per_vf:
            description:
              - Transmit Queue Count per VF (1-8).
            type: int
            default: 1
          comp_count_per_vf:
            description:
              - Completion Queue Count per VF (1-16).
            type: int
            default: 5
          int_count_per_vf:
            description:
              - Interrupt Count per VF (1-16).
            type: int
            default: 8
      state:
        description:
          - Whether to create/update or delete the vNIC.
        type: str
        choices: ['present', 'absent']
        default: present
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a LAN Connectivity Policy for Standalone servers
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "standalone-lan-policy"
    description: "LAN connectivity policy for standalone servers"
    target_platform: "Standalone"
    tags:
      - Key: "Environment"
        Value: "Production"
      - Key: "Site"
        Value: "DataCenter-A"
    vnics:
      - name: "eth0"
        placement_slot_id: "1"
        pci_link: 0
        uplink_port: 0
        order: 0
        eth_network_policy_name: "default-network-policy"
        eth_qos_policy_name: "default-qos-policy"
        eth_adapter_policy_name: "default-adapter-policy"
        connection_type: "none"
      - name: "eth1"
        placement_slot_id: "2"
        pci_link: 0
        uplink_port: 1
        order: 1
        eth_network_policy_name: "vlan-network-policy"
        eth_qos_policy_name: "high-qos-policy"
        eth_adapter_policy_name: "performance-adapter-policy"
        connection_type: "none"
    state: present

- name: Create a LAN Connectivity Policy for FI-Attached servers
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "fi-attached-lan-policy"
    description: "LAN connectivity policy for FI-attached servers"
    target_platform: "attached"
    azure_qos_enabled: true
    iqn_allocation_type: "Pool"
    iqn_pool_name: "default-iqn-pool"
    placement_mode: "custom"
    tags:
      - Key: "Environment"
        Value: "Production"
    vnics:
      - name: "vnic-fi-attached"
        order: 0
        cdn_source: "vnic"
        mac_address_type: "pool"
        mac_pool_name: "default-mac-pool"
        auto_slot_id: true
        auto_pci_link: true
        switch_id: "A"
        failover_enabled: false
        fabric_eth_network_group_policy_name: "default-network-group"
        fabric_eth_network_control_policy_name: "default-network-control"
        eth_qos_policy_name: "default-qos-policy"
        eth_adapter_policy_name: "default-adapter-policy"
        connection_type: "none"
        state: present
    state: present

- name: Create a LAN Connectivity Policy with USNIC vNIC
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "usnic-lan-policy"
    description: "Policy with USNIC configuration"
    target_platform: "Standalone"
    vnics:
      - name: "usnic-eth0"
        placement_slot_id: "4"
        pci_link: 0
        uplink_port: 0
        order: 0
        eth_network_policy_name: "hpc-network-policy"
        eth_qos_policy_name: "hpc-qos-policy"
        eth_adapter_policy_name: "hpc-adapter-policy"
        connection_type: "usnic"
        usnic_settings:
          count: 0
          cos: 5
          usnic_adapter_policy_name: "hpc-adapter-policy"
    state: present

- name: Create a LAN Connectivity Policy with VMQ vNIC
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "vmq-lan-policy"
    description: "Policy with VMQ configuration"
    target_platform: "Standalone"
    vnics:
      - name: "vmq-eth0"
        placement_slot_id: "10"
        pci_link: 0
        uplink_port: 2
        order: 0
        eth_network_policy_name: "vm-network-policy"
        eth_qos_policy_name: "vm-qos-policy"
        eth_adapter_policy_name: "vm-adapter-policy"
        connection_type: "vmq"
        vmq_settings:
          enabled: true
          multi_queue_support: false
          num_interrupts: 16
          num_vmqs: 4
    state: present

- name: Create a LAN Connectivity Policy with VMQ multi-queue support
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "vmq-multiqueue-lan-policy"
    description: "Policy with VMQ multi-queue configuration"
    target_platform: "Standalone"
    vnics:
      - name: "vmq-mq-eth0"
        placement_slot_id: "11"
        pci_link: 1
        uplink_port: 3
        order: 0
        eth_network_policy_name: "vm-network-policy"
        eth_qos_policy_name: "vm-qos-policy"
        eth_adapter_policy_name: "vm-adapter-policy"
        connection_type: "vmq"
        vmq_settings:
          enabled: true
          multi_queue_support: true
          num_sub_vnics: 64
          vmmq_adapter_policy_name: "vmmq-adapter-policy"
    state: present

- name: Create a LAN Connectivity Policy with SR-IOV vNIC
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "sriov-lan-policy"
    description: "Policy with SR-IOV configuration"
    target_platform: "Standalone"
    vnics:
      - name: "sriov-eth0"
        placement_slot_id: "14"
        pci_link: 0
        uplink_port: 1
        order: 0
        eth_network_policy_name: "sriov-network-policy"
        eth_qos_policy_name: "sriov-qos-policy"
        eth_adapter_policy_name: "sriov-adapter-policy"
        connection_type: "sriov"
        sriov_settings:
          enabled: true
          vf_count: 64
          rx_count_per_vf: 4
          tx_count_per_vf: 1
          comp_count_per_vf: 5
          int_count_per_vf: 8
    state: present

- name: Create a LAN Connectivity Policy with custom CDN values
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "custom-cdn-lan-policy"
    description: "Policy with custom CDN values"
    target_platform: "Standalone"
    vnics:
      - name: "mgmt-nic"
        placement_slot_id: "1"
        pci_link: 0
        uplink_port: 0
        order: 0
        cdn_source: "user"
        cdn_value: "Management-NIC"
        eth_network_policy_name: "mgmt-network-policy"
        eth_qos_policy_name: "mgmt-qos-policy"
        eth_adapter_policy_name: "mgmt-adapter-policy"
        connection_type: "none"
    state: present

- name: Update LAN connectivity policy - manage vNIC states
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "mixed-vnic-states-policy"
    description: "Policy demonstrating vNIC state management"
    target_platform: "Standalone"
    vnics:
      - name: "eth0"
        placement_slot_id: "1"
        pci_link: 0
        uplink_port: 0
        order: 0
        eth_network_policy_name: "production-network"
        eth_qos_policy_name: "standard-qos"
        eth_adapter_policy_name: "standard-adapter"
        connection_type: "none"
        state: present
      - name: "eth1-old"
        state: absent
      - name: "eth2-new"
        placement_slot_id: "3"
        pci_link: 0
        uplink_port: 1
        order: 1
        eth_network_policy_name: "production-network"
        eth_qos_policy_name: "standard-qos"
        eth_adapter_policy_name: "standard-adapter"
        connection_type: "vmq"
        vmq_settings:
          enabled: true
          multi_queue_support: false
          num_interrupts: 16
          num_vmqs: 4
        state: present
    state: present

- name: Delete a LAN Connectivity Policy
  cisco.intersight.intersight_lan_connectivity_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "old-lan-policy"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "test-lan-policy",
        "ObjectType": "vnic.LanConnectivityPolicy",
        "TargetPlatform": "Standalone",
        "Tags": [
            {
                "Key": "Environment",
                "Value": "Production"
            }
        ],
        "vNICs": [
            {
                "Name": "eth0",
                "ObjectType": "vnic.EthIf",
                "Order": 0,
                "Placement": {
                    "Id": "1"
                }
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def validate_fi_attached_params(module):
    """
    Validate FI-Attached specific parameters
    """
    iqn_allocation_type = module.params.get('iqn_allocation_type')
    static_iqn_name = module.params.get('static_iqn_name')
    iqn_pool_name = module.params.get('iqn_pool_name')

    # Validate IQN allocation type requirements
    if iqn_allocation_type == 'Static' and not static_iqn_name:
        module.fail_json(msg="static_iqn_name is required when iqn_allocation_type is 'Static'")

    if iqn_allocation_type == 'Pool' and not iqn_pool_name:
        module.fail_json(msg="iqn_pool_name is required when iqn_allocation_type is 'Pool'")

    if iqn_allocation_type != 'Static' and static_iqn_name:
        module.fail_json(msg="static_iqn_name should only be specified when iqn_allocation_type is 'Static'")

    if iqn_allocation_type != 'Pool' and iqn_pool_name:
        module.fail_json(msg="iqn_pool_name should only be specified when iqn_allocation_type is 'Pool'")


def validate_fi_attached_vnic_config(module, vnic_config):
    """
    Validate FIAttached specific vNIC configuration
    """
    vnic_name = vnic_config.get('name', 'unknown')
    mac_address_type = vnic_config.get('mac_address_type', 'pool')
    mac_pool_name = vnic_config.get('mac_pool_name')
    static_mac_address = vnic_config.get('static_mac_address')

    # Validate MAC address configuration
    if mac_address_type == 'pool' and not mac_pool_name:
        module.fail_json(msg=f"mac_pool_name is required when mac_address_type is 'pool' for vNIC '{vnic_name}'")

    if mac_address_type == 'static' and not static_mac_address:
        module.fail_json(msg=f"static_mac_address is required when mac_address_type is 'static' for vNIC '{vnic_name}'")

    if mac_address_type != 'pool' and mac_pool_name:
        module.fail_json(msg=f"mac_pool_name should only be specified when mac_address_type is 'pool' for vNIC '{vnic_name}'")

    if mac_address_type != 'static' and static_mac_address:
        module.fail_json(msg=f"static_mac_address should only be specified when mac_address_type is 'static' for vNIC '{vnic_name}'")

    # Validate required FIAttached fields
    fabric_eth_network_group_policy_name = vnic_config.get('fabric_eth_network_group_policy_name')
    fabric_eth_network_control_policy_name = vnic_config.get('fabric_eth_network_control_policy_name')

    if not fabric_eth_network_group_policy_name:
        module.fail_json(msg=f"fabric_eth_network_group_policy_name is required for attached vNIC '{vnic_name}'")

    if not fabric_eth_network_control_policy_name:
        module.fail_json(msg=f"fabric_eth_network_control_policy_name is required for attached vNIC '{vnic_name}'")


def validate_standalone_vnic_config(module, vnic_config):
    """
    Validate Standalone specific vNIC configuration
    """
    vnic_name = vnic_config.get('name', 'unknown')

    # Validate required Standalone fields
    placement_slot_id = vnic_config.get('placement_slot_id')
    eth_network_policy_name = vnic_config.get('eth_network_policy_name')

    if not placement_slot_id:
        module.fail_json(msg=f"placement_slot_id is required for standalone vNIC '{vnic_name}'")

    if not eth_network_policy_name:
        module.fail_json(msg=f"eth_network_policy_name is required for standalone vNIC '{vnic_name}'")


def validate_vnic_cdn_config(module, vnic_config):
    """
    Validate vNIC CDN configuration
    """
    cdn_source = vnic_config.get('cdn_source', 'vnic')
    cdn_value = vnic_config.get('cdn_value')
    vnic_name = vnic_config.get('name', 'unknown')

    if cdn_source == 'user' and not cdn_value:
        module.fail_json(msg=f"cdn_value is required when cdn_source is set to 'user' for vNIC '{vnic_name}'")

    if cdn_source == 'vnic' and cdn_value:
        module.fail_json(msg=f"cdn_value should not be provided when cdn_source is set to 'vnic' for vNIC '{vnic_name}'")


def validate_usnic_settings(module, vnic_config, usnic_settings):
    """
    Validate USNIC connection type settings
    """
    vnic_name = vnic_config.get('name', 'unknown')

    if not usnic_settings:
        module.fail_json(msg=f"usnic_settings is required when connection_type is 'usnic' for vNIC '{vnic_name}'")

    usnic_adapter_policy_name = usnic_settings.get('usnic_adapter_policy_name')
    if not usnic_adapter_policy_name:
        module.fail_json(msg=f"usnic_adapter_policy_name is required in usnic_settings for vNIC '{vnic_name}'")

    count = usnic_settings.get('count', 0)
    cos = usnic_settings.get('cos', 5)

    if count < 0 or count > 225:
        module.fail_json(msg="USNIC count must be between 0 and 225")
    if cos < 0 or cos > 6:
        module.fail_json(msg="USNIC CoS must be between 0 and 6")


def validate_vmq_settings(module, vmq_settings):
    """
    Validate VMQ connection type settings
    """
    multi_queue_support = vmq_settings.get('multi_queue_support', False)

    if not multi_queue_support:
        num_interrupts = vmq_settings.get('num_interrupts', 16)
        num_vmqs = vmq_settings.get('num_vmqs', 4)

        if num_interrupts < 1 or num_interrupts > 514:
            module.fail_json(msg="VMQ num_interrupts must be between 1 and 514")
        if num_vmqs < 1 or num_vmqs > 128:
            module.fail_json(msg="VMQ num_vmqs must be between 1 and 128")
    else:
        num_sub_vnics = vmq_settings.get('num_sub_vnics', 64)
        if num_sub_vnics < 0 or num_sub_vnics > 64:
            module.fail_json(msg="VMQ num_sub_vnics must be between 0 and 64")

        if not vmq_settings.get('vmmq_adapter_policy_name'):
            module.fail_json(msg="vmmq_adapter_policy_name is required when multi_queue_support is true")


def validate_sriov_settings(module, sriov_settings):
    """
    Validate SR-IOV connection type settings
    """
    vf_count = sriov_settings.get('vf_count', 64)
    rx_count_per_vf = sriov_settings.get('rx_count_per_vf', 4)
    tx_count_per_vf = sriov_settings.get('tx_count_per_vf', 1)
    comp_count_per_vf = sriov_settings.get('comp_count_per_vf', 5)
    int_count_per_vf = sriov_settings.get('int_count_per_vf', 8)

    if vf_count < 1 or vf_count > 64:
        module.fail_json(msg="SR-IOV vf_count must be between 1 and 64")
    if rx_count_per_vf < 1 or rx_count_per_vf > 8:
        module.fail_json(msg="SR-IOV rx_count_per_vf must be between 1 and 8")
    if tx_count_per_vf < 1 or tx_count_per_vf > 8:
        module.fail_json(msg="SR-IOV tx_count_per_vf must be between 1 and 8")
    if comp_count_per_vf < 1 or comp_count_per_vf > 16:
        module.fail_json(msg="SR-IOV comp_count_per_vf must be between 1 and 16")
    if int_count_per_vf < 1 or int_count_per_vf > 16:
        module.fail_json(msg="SR-IOV int_count_per_vf must be between 1 and 16")


def get_policy_moid(intersight, policy_cache, module, resource_path, policy_name, policy_type="Policy"):
    """
    Get policy MOID with caching
    """
    if not policy_name:
        return None

    cache_key = f"{resource_path}:{policy_name}"
    if cache_key in policy_cache:
        return policy_cache[cache_key]

    policy_moid = intersight.get_moid_by_name(resource_path=resource_path, resource_name=policy_name)
    if not policy_moid:
        module.fail_json(msg=f"{policy_type} '{policy_name}' not found")

    policy_cache[cache_key] = policy_moid
    return policy_moid


def resolve_vnic_policy_moids(intersight, policy_cache, module, vnic_config, target_platform):
    """
    Resolve all policy MOIDs for a vNIC configuration based on target platform
    """
    policy_moids = {}

    # Common policies for both platforms
    common_policy_mappings = {
        'eth_qos_policy_name': ('/vnic/EthQosPolicies', 'EthQosPolicy', 'Ethernet QoS Policy'),
        'eth_adapter_policy_name': ('/vnic/EthAdapterPolicies', 'EthAdapterPolicy', 'Ethernet Adapter Policy')
    }

    # Platform-specific policies
    if target_platform == 'attached':
        platform_policy_mappings = {
            'fabric_eth_network_group_policy_name': (
                '/fabric/EthNetworkGroupPolicies', 'FabricEthNetworkGroupPolicy', 'Fabric Ethernet Network Group Policy'
            ),
            'fabric_eth_network_control_policy_name': (
                '/fabric/EthNetworkControlPolicies', 'FabricEthNetworkControlPolicy', 'Fabric Ethernet Network Control Policy'
            )
        }

        # MAC pool for FIAttached when using pool type
        if vnic_config.get('mac_address_type', 'pool') == 'pool':
            platform_policy_mappings['mac_pool_name'] = ('/macpool/Pools', 'MacPool', 'MAC Pool')

        # iSCSI boot policy is optional - only add if specified
        if vnic_config.get('iscsi_boot_policy_name'):
            platform_policy_mappings['iscsi_boot_policy_name'] = ('/vnic/IscsiBootPolicies', 'IscsiBootPolicy', 'iSCSI Boot Policy')

    else:  # standalone
        platform_policy_mappings = {
            'eth_network_policy_name': ('/vnic/EthNetworkPolicies', 'EthNetworkPolicy', 'Ethernet Network Policy')
        }

    all_policy_mappings = {}
    all_policy_mappings.update(common_policy_mappings)
    all_policy_mappings.update(platform_policy_mappings)

    for param_name, (resource_path, api_field, policy_type) in all_policy_mappings.items():
        policy_name = vnic_config.get(param_name)
        if policy_name:
            policy_moid = get_policy_moid(
                intersight, policy_cache, module, resource_path, policy_name, policy_type
            )
            # Special handling for FabricEthNetworkGroupPolicy which needs to be an array for the API
            if api_field == 'FabricEthNetworkGroupPolicy':
                policy_moids[api_field] = [policy_moid]
            else:
                policy_moids[api_field] = policy_moid

    return policy_moids


def build_usnic_settings(intersight, policy_cache, module, usnic_settings):
    """
    Build USNIC settings for vNIC API body
    """
    usnic_adapter_policy_name = usnic_settings.get('usnic_adapter_policy_name')
    usnic_adapter_policy_moid = get_policy_moid(
        intersight, policy_cache, module, '/vnic/EthAdapterPolicies',
        usnic_adapter_policy_name, 'USNIC Adapter Policy'
    )

    return {
        'Count': usnic_settings.get('count', 0),
        'UsnicAdapterPolicy': usnic_adapter_policy_moid,
        'Cos': usnic_settings.get('cos', 5)
    }


def build_vmq_settings(intersight, policy_cache, module, vmq_settings):
    """
    Build VMQ settings for vNIC API body
    """
    multi_queue_support = vmq_settings.get('multi_queue_support', False)

    if multi_queue_support:
        vmmq_adapter_policy_name = vmq_settings.get('vmmq_adapter_policy_name')
        vmmq_adapter_policy_moid = get_policy_moid(
            intersight, policy_cache, module, '/vnic/EthAdapterPolicies',
            vmmq_adapter_policy_name, 'VMMQ Adapter Policy'
        )

        return {
            'Enabled': vmq_settings.get('enabled', True),
            'MultiQueueSupport': True,
            'NumSubVnics': vmq_settings.get('num_sub_vnics', 64),
            'VmmqAdapterPolicy': vmmq_adapter_policy_moid
        }
    else:
        return {
            'Enabled': vmq_settings.get('enabled', True),
            'MultiQueueSupport': False,
            'NumInterrupts': vmq_settings.get('num_interrupts', 16),
            'NumVmqs': vmq_settings.get('num_vmqs', 4)
        }


def build_sriov_settings(sriov_settings):
    """
    Build SR-IOV settings for vNIC API body
    """
    return {
        'VfCount': sriov_settings.get('vf_count', 64),
        'RxCountPerVf': sriov_settings.get('rx_count_per_vf', 4),
        'TxCountPerVf': sriov_settings.get('tx_count_per_vf', 1),
        'CompCountPerVf': sriov_settings.get('comp_count_per_vf', 5),
        'IntCountPerVf': sriov_settings.get('int_count_per_vf', 8),
        'Enabled': sriov_settings.get('enabled', True)
    }


def build_vnic_cdn_config(vnic_config):
    """
    Build CDN configuration for vNIC API body
    """
    cdn_config = {
        'Source': vnic_config.get('cdn_source', 'vnic')
    }

    # Add CDN value if specified
    if vnic_config.get('cdn_value'):
        cdn_config['Value'] = vnic_config['cdn_value']

    return cdn_config


def build_vnic_connection_settings(intersight, policy_cache, module, vnic_config):
    """
    Build connection type specific settings for vNIC API body
    """
    connection_settings = {}
    connection_type = vnic_config.get('connection_type', 'none')

    if connection_type == 'usnic':
        usnic_settings = vnic_config.get('usnic_settings', {})
        connection_settings['UsnicSettings'] = build_usnic_settings(intersight, policy_cache, module, usnic_settings)
    elif connection_type == 'vmq':
        vmq_settings = vnic_config.get('vmq_settings', {})
        connection_settings['VmqSettings'] = build_vmq_settings(intersight, policy_cache, module, vmq_settings)
    elif connection_type == 'sriov':
        sriov_settings = vnic_config.get('sriov_settings', {})
        connection_settings['SriovSettings'] = build_sriov_settings(sriov_settings)

    return connection_settings


def build_vnic_api_body(intersight, policy_cache, module, vnic_config, lan_connectivity_policy_moid):
    """
    Build vNIC API body for API call
    """
    target_platform = module.params.get('target_platform')

    if target_platform == 'attached':
        return build_fi_attached_vnic_api_body(intersight, policy_cache, module, vnic_config, lan_connectivity_policy_moid)
    else:
        return build_standalone_vnic_api_body(intersight, policy_cache, module, vnic_config, lan_connectivity_policy_moid)


def build_standalone_vnic_api_body(intersight, policy_cache, module, vnic_config, lan_connectivity_policy_moid):
    """
    Build Standalone vNIC API body for Intersight API call
    """
    # Base vNIC configuration for Standalone
    vnic_api_body = {
        'Name': vnic_config['name'],
        'Placement': {
            'Id': vnic_config['placement_slot_id'],
            'Uplink': vnic_config.get('uplink_port', 0),
            'PciLink': vnic_config.get('pci_link', 0)
        },
        'Order': vnic_config.get('order', 0),
        'LanConnectivityPolicy': lan_connectivity_policy_moid
    }

    # Add common CDN configuration
    vnic_api_body['Cdn'] = build_vnic_cdn_config(vnic_config)

    # Resolve and add policy MOIDs
    policy_moids = resolve_vnic_policy_moids(intersight, policy_cache, module, vnic_config, 'standalone')
    vnic_api_body.update(policy_moids)

    # Add common connection type settings
    connection_settings = build_vnic_connection_settings(intersight, policy_cache, module, vnic_config)
    vnic_api_body.update(connection_settings)

    return vnic_api_body


def build_fi_attached_vnic_api_body(intersight, policy_cache, module, vnic_config, lan_connectivity_policy_moid):
    """
    Build FIAttached vNIC API body for Intersight API call
    """
    # Base vNIC configuration for FIAttached
    # Map lowercase user input to API format
    mac_address_type = vnic_config.get('mac_address_type', 'pool')
    api_mac_address_type = 'STATIC' if mac_address_type == 'static' else 'POOL'

    vnic_api_body = {
        'Name': vnic_config['name'],
        'MacAddressType': api_mac_address_type,
        'Placement': {
            'SwitchId': vnic_config.get('switch_id', 'A'),
            'AutoSlotId': vnic_config.get('auto_slot_id', True),
            'AutoPciLink': vnic_config.get('auto_pci_link', True)
        },
        'Order': vnic_config.get('order', 0),
        'FailoverEnabled': vnic_config.get('failover_enabled', False),
        'LanConnectivityPolicy': lan_connectivity_policy_moid
    }

    # Add common CDN configuration
    vnic_api_body['Cdn'] = build_vnic_cdn_config(vnic_config)

    # Add static MAC address if using static type
    if mac_address_type == 'static':
        vnic_api_body['StaticMacAddress'] = vnic_config['static_mac_address']

    # Resolve and add policy MOIDs
    policy_moids = resolve_vnic_policy_moids(intersight, policy_cache, module, vnic_config, 'attached')
    vnic_api_body.update(policy_moids)

    # Add common connection type settings
    connection_settings = build_vnic_connection_settings(intersight, policy_cache, module, vnic_config)
    vnic_api_body.update(connection_settings)

    return vnic_api_body


def validate_input(module):
    """
    Validate module input parameters
    """
    # Validate FI-Attached specific requirements
    target_platform = module.params.get('target_platform')
    if target_platform == 'attached':
        validate_fi_attached_params(module)

    # Validate vNIC configurations
    vnics = module.params.get('vnics', [])
    for vnic_config in vnics:
        vnic_name = vnic_config.get('name')
        vnic_state = vnic_config.get('state', 'present')

        # Only validate present vNICs - absent vNICs only need name
        if vnic_state == 'present':
            # Validate common required fields
            required_fields = ['eth_qos_policy_name', 'eth_adapter_policy_name']
            for field in required_fields:
                if not vnic_config.get(field):
                    module.fail_json(msg=f"{field} is required when vNIC state is 'present' for vNIC '{vnic_name}'")

            # Validate target platform specific fields
            target_platform = module.params.get('target_platform')
            if target_platform == 'attached':
                validate_fi_attached_vnic_config(module, vnic_config)
            else:
                validate_standalone_vnic_config(module, vnic_config)

            # Validate CDN configuration
            validate_vnic_cdn_config(module, vnic_config)

            connection_type = vnic_config.get('connection_type', 'none')

            # Validate connection type specific settings
            if connection_type == 'usnic':
                usnic_settings = vnic_config.get('usnic_settings')
                validate_usnic_settings(module, vnic_config, usnic_settings)
            elif connection_type == 'vmq':
                vmq_settings = vnic_config.get('vmq_settings', {})
                validate_vmq_settings(module, vmq_settings)
            elif connection_type == 'sriov':
                sriov_settings = vnic_config.get('sriov_settings', {})
                validate_sriov_settings(module, sriov_settings)


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        target_platform=dict(type='str', choices=['standalone', 'attached'], default='standalone'),
        azure_qos_enabled=dict(type='bool', default=False),
        iqn_allocation_type=dict(type='str', choices=['None', 'Pool', 'Static'], default='None'),
        placement_mode=dict(type='str', choices=['custom', 'auto'], default='custom'),
        iqn_pool_name=dict(type='str'),
        static_iqn_name=dict(type='str'),
        vnics=dict(type='list', elements='dict', options=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            placement_slot_id=dict(type='str'),
            pci_link=dict(type='int', choices=[0, 1], default=0),
            uplink_port=dict(type='int', choices=[0, 1, 2, 3], default=0),
            order=dict(type='int', default=0),
            cdn_source=dict(type='str', choices=['vnic', 'user'], default='vnic'),
            cdn_value=dict(type='str'),
            eth_network_policy_name=dict(type='str'),
            eth_qos_policy_name=dict(type='str'),
            eth_adapter_policy_name=dict(type='str'),
            mac_address_type=dict(type='str', choices=['pool', 'static'], default='pool'),
            mac_pool_name=dict(type='str'),
            static_mac_address=dict(type='str'),
            auto_slot_id=dict(type='bool', default=True),
            auto_pci_link=dict(type='bool', default=True),
            switch_id=dict(type='str', choices=['A', 'B'], default='A'),
            failover_enabled=dict(type='bool', default=False),
            fabric_eth_network_group_policy_name=dict(type='str'),
            fabric_eth_network_control_policy_name=dict(type='str'),
            iscsi_boot_policy_name=dict(type='str'),
            connection_type=dict(type='str', choices=['none', 'usnic', 'vmq', 'sriov'], default='none'),
            usnic_settings=dict(type='dict', options=dict(
                count=dict(type='int', default=0),
                cos=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6], default=5),
                usnic_adapter_policy_name=dict(type='str')
            )),
            vmq_settings=dict(type='dict', options=dict(
                enabled=dict(type='bool', default=True),
                multi_queue_support=dict(type='bool', default=False),
                num_interrupts=dict(type='int', default=16),
                num_vmqs=dict(type='int', default=4),
                num_sub_vnics=dict(type='int', default=64),
                vmmq_adapter_policy_name=dict(type='str')
            )),
            sriov_settings=dict(type='dict', options=dict(
                enabled=dict(type='bool', default=True),
                vf_count=dict(type='int', default=64),
                rx_count_per_vf=dict(type='int', default=4),
                tx_count_per_vf=dict(type='int', default=1),
                comp_count_per_vf=dict(type='int', default=5),
                int_count_per_vf=dict(type='int', default=8)
            ))
        ))
    )

    required_if = [
        ['state', 'present', ['vnics']],
    ]

    module = AnsibleModule(
        argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    if module.params['state'] == 'present':
        validate_input(module)

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Resource path used to configure policy
    resource_path = '/vnic/LanConnectivityPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name']
    }

    if intersight.module.params['state'] == 'present':
        intersight.set_tags_and_description()

        target_platform = intersight.module.params['target_platform']
        api_target_platform = 'FIAttached' if target_platform == 'attached' else 'Standalone'
        intersight.api_body['TargetPlatform'] = api_target_platform

        # Add FIAttached-specific parameters
        if intersight.module.params['target_platform'] == 'attached':
            intersight.api_body['AzureQosEnabled'] = intersight.module.params['azure_qos_enabled']
            intersight.api_body['IqnAllocationType'] = intersight.module.params['iqn_allocation_type']
            intersight.api_body['PlacementMode'] = intersight.module.params['placement_mode']

            # Resolve IQN pool MOID if specified
            if intersight.module.params['iqn_pool_name']:
                iqn_pool_moid = intersight.get_moid_by_name(
                    resource_path='/iqnpool/Pools',
                    resource_name=intersight.module.params['iqn_pool_name']
                )
                if not iqn_pool_moid:
                    intersight.module.fail_json(msg=f"IQN Pool '{intersight.module.params['iqn_pool_name']}' not found")
                intersight.api_body['IqnPool'] = iqn_pool_moid

            if intersight.module.params['static_iqn_name']:
                intersight.api_body['StaticIqnName'] = intersight.module.params['static_iqn_name']

    intersight.configure_policy_or_profile(resource_path=resource_path)

    # Save the LAN connectivity policy response
    lan_connectivity_policy_response = intersight.result['api_response']

    lan_connectivity_policy_moid = None
    if intersight.module.params['state'] == 'present' and lan_connectivity_policy_response:
        lan_connectivity_policy_moid = lan_connectivity_policy_response.get('Moid')

    # Process vNICs
    vnics_response = []
    if intersight.module.params['state'] == 'present' and intersight.module.params.get('vnics'):
        # Cache for policy MOIDs to avoid redundant API calls
        policy_cache = {}

        for vnic_config in intersight.module.params['vnics']:
            vnic_state = vnic_config.get('state', 'present')

            # Only build API body for present vNICs
            if vnic_state == 'present':
                # Build vNIC API body using helper function
                vnic_api_body = build_vnic_api_body(
                    intersight, policy_cache, module, vnic_config, lan_connectivity_policy_moid
                )
                intersight.api_body = vnic_api_body

            # Configure the vNIC (create/update/delete)
            resource_path = '/vnic/EthIfs'
            intersight.configure_secondary_resource(
                resource_path=resource_path,
                resource_name=vnic_config['name'],
                state=vnic_state
            )

            # Save the vNIC response only if it's present
            if vnic_state == 'present':
                vnics_response.append(intersight.result['api_response'])

    # Combine LAN connectivity policy and vNICs in the main response
    if lan_connectivity_policy_response:
        lan_connectivity_policy_response['vNICs'] = vnics_response
        intersight.result['api_response'] = lan_connectivity_policy_response

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
