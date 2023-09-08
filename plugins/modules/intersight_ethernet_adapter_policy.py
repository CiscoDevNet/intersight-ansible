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
module: intersight_ethernet_adapter_policy
short_description: Ethernet Adapter policy configuration for Cisco Intersight
description:
  - Ethernet Adapter policy configuration for Cisco Intersight.
  - Used to configure Ethernet Adapter Policy on Cisco Intersight managed devices.
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
      - The name assigned to the Ethernet Adapter policy.
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
  advanced_filter:
    description:
      -  Enables advanced filtering on the interface.
    default: false
    type: bool
  arfs_settings:
    description:
      -  Settings for Accelerated Receive Flow Steering to reduce the network latency and increase CPU cache efficiency.
    type: list
    elements: dict
    suboptions:
      enabled:
        description:
          - Status of Accelerated Receive Flow Steering on the virtual ethernet interface
        type: bool
        default: false
  completion_queue_settings:
    description:
      -  Completion Queue resource settings.
    type: list
    elements: dict
    suboptions:
      count:
        description:
          - The number of completion queue resources to allocate. In general, the number of completion queue resources to allocate is equal to the number
          - of transmit queue resources plus the number of receive queue resources
        type: int
        default: 5
      ring_size:
        description:
          - The number of descriptors in each completion queue
        type: int
        default: 1
  geneve_enabled:
    description:
      - GENEVE offload protocol allows you to create logical networks that span physical network boundaries by allowing any information to be encoded
      - in a packet and passed between tunnel endpoints.
    default: False
    type: bool
  interrupt_scaling:
    description:
      -  Enables Interrupt Scaling on the interface.
    default: False
    type: bool
  interrupt_settings:
    description:
      -  Interrupt Settings for the virtual ethernet interface.
    type: list
    elements: dict
    suboptions:
      coalescing_time:
        description:
          - The time to wait between interrupts or the idle period that must be encountered before an interrupt is sent.
          - To turn off interrupt coalescing, enter 0 (zero) in this field
        type: int
        default: 125
      coalescing_type:
        description:
          - Interrupt Coalescing Type. This can be one of the following  MIN  - The system waits for the time specified in the Coalescing Time field
          - before sending another interrupt event IDLE - The system does not send an interrupt until there is a period of no activity lasting as least
          - as long as the time specified in the Coalescing Time field.
          - MIN - The system waits for the time specified in the Coalescing Time field before sending another interrupt event.
          - IDLE - The system does not send an interrupt until there is a period of no activity lasting as least as long
          - as the time specified in the Coalescing Time field
        type : str
        choices : [ 'MIN', 'IDLE' ]
        default: MIN
      count:
        description:
          - The number of interrupt resources to allocate. Typical value is be equal to the number of completion queue resources
        type: int
        default: 8
      mode:
        description:
          - Preferred driver interrupt mode. This can be one of the following:- MSIx - Message Signaled Interrupts (MSI) with the optional extension.
          - MSI  - MSI only. INTx - PCI INTx interrupts. MSIx is the recommended option.
          - MSIx - Message Signaled Interrupt (MSI) mechanism with the optional extension (MSIx). MSIx is the recommended and default option.
          - MSI - Message Signaled Interrupt (MSI) mechanism that treats messages as interrupts.
          - INTx - Line-based interrupt (INTx) mechanism similar to the one used in Legacy systems.
        type: str
        choices: [ 'MSIx', 'MSI', 'INTx' ]
        default: MSIx
  nvgre_settings:
    description:
      -  Network Virtualization using Generic Routing Encapsulation Settings.
    type: list
    elements: dict
    suboptions:
      enabled:
        description:
          - Status of the Network Virtualization using Generic Routing Encapsulation on the virtual ethernet interface
        type: bool
        default: False
  ptp_settings:
    description:
      - Settings for Precision Time Protocol which can provide precise time of day information and time-stampted inputs, as well as scheduled
      - and/or synchronized outputs for a variety of systems.
    type: list
    elements: dict
    suboptions:
      enabled:
        description:
          - Status of Precision Time Protocol (PTP) on the virtual ethernet interface. PTP can be enabled only on one vNIC on an adapter.
        type: bool
        default: False
  roce_settings:
    description:
      -  Settings for RDMA over Converged Ethernet.
    type: list
    elements: dict
    suboptions:
      class_of_service:
        description:
          - The Class of Service for RoCE on this virtual interface.
          - 5 - RDMA CoS Service Level 5.
          - 1 - RDMA CoS Service Level 1.
          - 2 - RDMA CoS Service Level 2.
          - 4 - RDMA CoS Service Level 4.
          - 6 - RDMA CoS Service Level 6.
        type: int
        choices: [5, 1, 2, 4, 6]
        default: 5
      enabled:
        description:
          - If enabled sets RDMA over Converged Ethernet (RoCE) on this virtual interface
        type: bool
        default: False
      memory_regions:
        description:
          - The number of memory regions per adapter. Recommended value = integer power of 2.
        type: int
        default: 131072
      queue_pairs:
        description:
          - The number of queue pairs per adapter. Recommended value = integer power of 2.
        type: int
        default: 256
      resource_groups:
        description:
          - The number of resource groups per adapter. Recommended value = be an integer power of 2 greater than or equal to the number of CPU cores on
          - the system for optimum performance.
        type: int
        default: 2
      version:
        description:
          - Configure RDMA over Converged Ethernet (RoCE) version on the virtual interface.
          - Only RoCEv1 is supported on Cisco VIC 13xx series adapters and only RoCEv2 is supported on Cisco VIC 14xx series adapters.
          - 1 - RDMA over Converged Ethernet Protocol Version 1.
          - 2 - RDMA over Converged Ethernet Protocol Version 2.
        type: int
        choices: [1, 2]
        default: 1
  rss_hash_settings:
    description:
      -  Receive Side Scaling allows the incoming traffic to be spread across multiple CPU cores.
    type: list
    elements: dict
    suboptions:
      ipv4_hash:
        description:
          - When enabled, the IPv4 address is used for traffic distribution.
        type: bool
        default: False
      ipv6_ext_hash:
        description:
          - When enabled, the IPv6 extensions are used for traffic distribution.
        type: bool
        default: False
      ipv6_hash:
        description:
          - When enabled, the IPv6 address is used for traffic distribution.
        type: bool
        default: False
      tcp_ipv4_hash:
        description:
          - When enabled, both the IPv4 address and TCP port number are used for traffic distribution
        type: bool
        default: False
      tcp_ipv6_ext_hash:
        description:
          - When enabled, both the IPv6 extensions and TCP port number are used for traffic distribution.
        type: bool
        default: False
      tcp_ipv6_hash:
        description:
          - When enabled, both the IPv6 address and TCP port number are used for traffic distribution
        type: bool
        default: False
      udp_ipv4_hash:
        description:
          - When enabled, both the IPv4 address and UDP port number are used for traffic distribution
        type: bool
        default: False
      udp_ipv6_hash:
        description:
          - When enabled, both the IPv6 address and UDP port number are used for traffic distribution
        type: bool
        default: False
  rss_settings:
    description:
      -  Receive Side Scaling allows the incoming traffic to be spread across multiple CPU cores.
    default: True
    type: bool
  rx_queue_settings:
    description:
      -  Receive Queue resouce settings.
    type: list
    elements: dict
    suboptions:
      count:
        description:
          - The number of queue resources to allocate.
        type: int
        default: 4
      ring_size:
        description:
          - The number of descriptors in each queue
        type: int
        default: 512
  tcp_offload_settings:
    description:
      -  The TCP offload settings decide whether to offload the TCP related network functions from the CPU to the network hardware or not.
    type: list
    elements: dict
    suboptions:
      large_receive:
        description:
          - Enables the reassembly of segmented packets in hardware before sending them to the CPU
        type: bool
        default: True
      large_send:
        description:
          - Enables the CPU to send large packets to the hardware for segmentation
        type: bool
        default: True
      rx_checksum:
        description:
          - When enabled, the CPU sends all packet checksums to the hardware for validation.
        type: bool
        default: True
      tx_checksum:
        description:
          - When enabled, the CPU sends all packets to the hardware so that the checksum can be calculated.
        type: bool
        default: True
  tx_queue_settings:
    description:
      -  Transmit Queue resource settings.
    type: list
    elements: dict
    suboptions:
      count:
        description:
          - The number of queue resources to allocate.
        type: int
        default: 1
      ring_size:
        description:
          - The number of descriptors in each queue
        type: int
        default: 256
  uplink_failback_timeout:
    description:
      - Uplink Failback Timeout in seconds when uplink failover is enabled for a vNIC.
      - After a vNIC has started using its secondary interface, this setting controls how long the primary interface must be available
      - before the system resumes using the primary interface for the vNIC.
    default: 5
    type: int
  vxlan_settings:
    description:
      -  Virtual Extensible LAN Protocol Settings.
    type: list
    elements: dict
    suboptions:
      enabled:
        description:
          - Status of the Virtual Extensible LAN Protocol on the virtual ethernet interface
        type: bool
        default: False
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure Ethernet Adapter Policy
  cisco.intersight.intersight_ethernet_adapter_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-EAP
    description: Ethernet adapter policy for COS
    tags:
      - Key: Site
        Value: RCDN
    geneve_enabled: True
    vxlan_settings:
      enabled: True

- name: Delete Ethernet Adapter Policy
  cisco.intersight.intersight_ethernet_adapter_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-EAP
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
        "ObjectType": "vnic.LanConnectivityPolicy",
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


def check_and_add_prop(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = params[prop_key]


def check_and_add_prop_dict(prop, prop_key, params, api_body):
    if prop_key in params.keys():
        api_body[prop] = {}
        if params[prop_key] :
            for item in params[prop_key]:
                for key in item.keys():
                    api_body[prop][to_camel_case(key)] = item[key]


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def main():
    arfs_spec = {
        "enabled" : {"type": "bool", "default": False}
    }
    completion_queue_spec = {
        "count": {"type": "int", "default": 5},
        "ring_size": {"type": "int", "default": 1}
    }
    interrupt_setting_spec = {
        "coalescing_time" : {"type": "int", "default": 125},
        "coalescing_type": {"type": "str", "default": "MIN", "choices": ['MIN', 'IDLE']},
        "count": {"type": "int", "default": 8},
        "mode": {"type": "str", "default": "MSIx", "choices": ['MSIx', 'MSI' , 'INTx']}
    }
    nvgre_settings_spec = {
        "enabled" : {"type": "bool", "default": False}
    }
    ptp_settings_spec = {
        "enabled" : {"type": "bool", "default": False}
    }
    roce_settings_spec = {
        "class_of_service": {"type": "int", "default": 5, "choices": [5, 1, 2, 4, 6]},
        "enabled" : {"type": "bool", "default": False},
        "memory_regions" : {"type": "int", "default": 131072},
        "queue_pairs" : {"type": "int", "default": 256},
        "resource_groups" : {"type": "int", "default": 2},
        "version": {"type": "int", "default": 1, "choices": [1, 2]},
    }
    rss_hash_settings_spec = {
        "ipv4_hash" : {"type": "bool", "default": False},
        "ipv6_ext_hash" : {"type": "bool", "default": False},
        "ipv6_hash" : {"type": "bool", "default": False},
        "tcp_ipv4_hash" : {"type": "bool", "default": False},
        "tcp_ipv6_ext_hash" : {"type": "bool", "default": False},
        "tcp_ipv6_hash" : {"type": "bool", "default": False},
        "udp_ipv4_hash" : {"type": "bool", "default": False},
        "udp_ipv6_hash" : {"type": "bool", "default": False},
    }
    rx_queue_settings_spec = {
        "count" : {"type": "int", "default": 4},
        "ring_size" : {"type": "int", "default": 512},
    }
    tcp_offload_settings_spec = {
        "large_receive" : {"type": "bool", "default": True},
        "large_send" : {"type": "bool", "default": True},
        "rx_checksum" : {"type": "bool", "default": True},
        "tx_checksum" : {"type": "bool", "default": True},
    }
    tx_queue_settings_spec = {
        "count" : {"type": "int", "default": 1},
        "ring_size" : {"type": "int", "default": 256},
    }
    vxlan_settings_spec = {
        "enabled" : {"type": "bool", "default": False}
    }
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        advanced_filter={
            "type": "bool",
            "default": False
        },
        arfs_settings={
            "type": "list",
            "elements": "dict",
            "options" : arfs_spec
        },
        completion_queue_settings={
            "type": "list",
            "elements": "dict",
            "options": completion_queue_spec
        },
        geneve_enabled={
            "type": "bool",
            "default": False
        },
        interrupt_scaling={
            "type": "bool",
            "default": False
        },
        interrupt_settings={
            "type": "list",
            "elements": "dict",
            "options": interrupt_setting_spec
        },
        nvgre_settings={
            "type": "list",
            "elements": "dict",
            "options": nvgre_settings_spec
        },
        ptp_settings={
            "type": "list",
            "elements": "dict",
            "options": ptp_settings_spec
        },
        roce_settings={
            "type": "list",
            "elements": "dict",
            "options": roce_settings_spec
        },
        rss_hash_settings={
            "type": "list",
            "elements": "dict",
            "options": rss_hash_settings_spec
        },
        rss_settings={
            "type": "bool",
            "default": True
        },
        rx_queue_settings={
            "type": "list",
            "elements": "dict",
            "options": rx_queue_settings_spec
        },
        tcp_offload_settings={
            "type": "list",
            "elements": "dict",
            "options": tcp_offload_settings_spec
        },
        tx_queue_settings={
            "type": "list",
            "elements": "dict",
            "options": tx_queue_settings_spec
        },
        uplink_failback_timeout={
            "type": "int",
            "default": 5
        },
        vxlan_settings={
            "type": "list",
            "elements": "dict",
            "options": vxlan_settings_spec
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
    resource_path = '/vnic/EthAdapterPolicies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
    }
    check_and_add_prop('AdvancedFilter', 'advanced_filter', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('ArfsSettings', 'arfs_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('CompletionQueueSettings', 'completion_queue_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop('GeneveEnabled', 'geneve_enabled', intersight.module.params, intersight.api_body)
    check_and_add_prop('InterruptScaling', 'interrupt_scaling', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('InterruptSettings', 'interrupt_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('NvgreSettings', 'nvgre_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('PtpSettings', 'ptp_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('RoceSettings', 'roce_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('RssHashSettings', 'rss_hash_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop('RssSettings', 'rss_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('RxQueueSettings', 'rx_queue_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('TcpOffloadSettings', 'tcp_offload_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('TxQueueSettings', 'tx_queue_settings', intersight.module.params, intersight.api_body)
    check_and_add_prop('UplinkFailbackTimeout', 'uplink_failback_timeout', intersight.module.params, intersight.api_body)
    check_and_add_prop_dict('VxlanSettings', 'vxlan_settings', intersight.module.params, intersight.api_body)
    #
    # Code below should be common across all policy modules
    #
    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
