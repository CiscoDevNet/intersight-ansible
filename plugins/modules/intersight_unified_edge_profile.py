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
module: intersight_unified_edge_profile
short_description: Unified Edge server profile template for Cisco Intersight
description:
  - Creates validated server profile templates for Cisco Unified Edge nodes
    used in AI Factory edge inference deployments.
  - Provides hardware-specific presets for supported Unified Edge platforms
    (UCS XE9305, XE130c M8, XE150c M8) with appropriate thermal limits,
    power budgets, and expansion constraints.
  - Attaches user-specified policies for BIOS, boot, storage, network,
    and other configuration via the PolicyBucket mechanism.
  - For generic server profile template management, use
    M(cisco.intersight.intersight_server_profile_template) instead.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
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
    type: str
    default: default
  name:
    description:
      - The name assigned to the server profile template.
      - The name must be between 1 and 64 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  description:
    description:
      - The user-defined description of the server profile template.
    type: str
    aliases: [descr]
  hardware_platform:
    description:
      - The Unified Edge hardware platform this template targets.
      - C(xe9305) targets the UCS XE9305 compact edge server.
        Designed for single-GPU or CPU-only inference at the edge with constrained
        thermal envelope and limited PCIe expansion.
      - C(xe130c_m8) targets the UCS XE130c M8 short-depth edge server.
        Supports up to 2 GPUs with moderate thermal headroom for inference workloads
        in ruggedized edge environments.
      - C(xe150c_m8) targets the UCS XE150c M8 edge compute server.
        Full-height edge server supporting up to 4 GPUs with higher power budget
        for demanding edge AI inference and light training workloads.
    type: str
    choices: [xe9305, xe130c_m8, xe150c_m8]
  bios_policy:
    description:
      - Name of BIOS Policy to associate with this template.
      - Consider using a policy created by M(cisco.intersight.intersight_bios_ai_tuning)
        with the C(edge_ai) tuning profile.
    type: str
  boot_order_policy:
    description:
      - Name of Boot Order Policy to associate with this template.
    type: str
  firmware_policy:
    description:
      - Name of Firmware Policy to associate with this template.
    type: str
  storage_policy:
    description:
      - Name of Storage Policy to associate with this template.
      - Consider using a policy created by M(cisco.intersight.intersight_ai_storage_policy)
        with the C(edge_compact) storage profile.
    type: str
  thermal_policy:
    description:
      - Name of Thermal Policy to associate with this template.
      - If not specified, the hardware_platform preset will suggest an appropriate thermal mode.
    type: str
  power_policy:
    description:
      - Name of Power Policy to associate with this template.
    type: str
  lan_connectivity_policy:
    description:
      - Name of LAN Connectivity Policy to associate with this template.
    type: str
  ipmi_over_lan_policy:
    description:
      - Name of IPMI over LAN Policy to associate with this template.
    type: str
  kvm_policy:
    description:
      - Name of Virtual KVM Policy to associate with this template.
    type: str
  network_connectivity_policy:
    description:
      - Name of Network Connectivity Policy to associate with this template.
    type: str
  ntp_policy:
    description:
      - Name of NTP Policy to associate with this template.
    type: str
  snmp_policy:
    description:
      - Name of SNMP Policy to associate with this template.
    type: str
  ssh_policy:
    description:
      - Name of SSH Policy to associate with this template.
    type: str
  syslog_policy:
    description:
      - Name of Syslog Policy to associate with this template.
    type: str
  local_user_policy:
    description:
      - Name of Local User Policy to associate with this template.
    type: str
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Create XE9305 edge inference profile template
  cisco.intersight.intersight_unified_edge_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: Edge-Sites
    name: spt-xe9305-inference
    description: XE9305 compact edge inference server
    hardware_platform: xe9305
    bios_policy: bios-edge-ai
    boot_order_policy: boot-uefi-nvme
    storage_policy: storage-edge-inference
    lan_connectivity_policy: lan-edge-mgmt

- name: Create XE130c M8 edge GPU inference template
  cisco.intersight.intersight_unified_edge_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: spt-xe130c-gpu-inference
    description: XE130c M8 with 2 GPUs for edge inference
    hardware_platform: xe130c_m8
    bios_policy: bios-edge-ai
    storage_policy: storage-model-cache
    firmware_policy: fw-latest

- name: Create XE150c M8 high-performance edge template
  cisco.intersight.intersight_unified_edge_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: spt-xe150c-training
    description: XE150c M8 for edge training and inference
    hardware_platform: xe150c_m8
    bios_policy: bios-gpu-inference-h100
    storage_policy: storage-ai-inference

- name: Delete edge profile template
  cisco.intersight.intersight_unified_edge_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: spt-xe9305-inference
    hardware_platform: xe9305
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "spt-xe9305-inference",
        "ObjectType": "server.ProfileTemplate",
        "TargetPlatform": "UnifiedEdgeServer"
    }
hardware_constraints:
  description: Hardware constraints and recommendations for the selected platform.
  returned: when state is present
  type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import (
    IntersightModule,
    intersight_argument_spec,
    resolve_policy_bucket,
    sync_policy_bucket,
)


# Hardware platform constraints and metadata
HARDWARE_PLATFORMS = {
    'xe9305': {
        'description': 'UCS XE9305 compact edge server',
        'max_gpus': 0,
        'max_power_watts': 500,
        'thermal_recommendation': 'Acoustic',
        'form_factor': 'compact',
        'pcie_slots': 1,
    },
    'xe130c_m8': {
        'description': 'UCS XE130c M8 short-depth edge server',
        'max_gpus': 2,
        'max_power_watts': 1200,
        'thermal_recommendation': 'Balanced',
        'form_factor': 'short-depth',
        'pcie_slots': 3,
    },
    'xe150c_m8': {
        'description': 'UCS XE150c M8 edge compute server',
        'max_gpus': 4,
        'max_power_watts': 2400,
        'thermal_recommendation': 'HighPower',
        'form_factor': 'full-height',
        'pcie_slots': 6,
    },
}

# Policy mapping for PolicyBucket resolution
POLICY_MAPPING = {
    'bios_policy': {'resource_path': '/bios/Policies', 'object_type': 'bios.Policy'},
    'boot_order_policy': {'resource_path': '/boot/PrecisionPolicies', 'object_type': 'boot.PrecisionPolicy'},
    'firmware_policy': {'resource_path': '/firmware/Policies', 'object_type': 'firmware.Policy'},
    'storage_policy': {'resource_path': '/storage/StoragePolicies', 'object_type': 'storage.StoragePolicy'},
    'thermal_policy': {'resource_path': '/thermal/Policies', 'object_type': 'thermal.Policy'},
    'power_policy': {'resource_path': '/power/Policies', 'object_type': 'power.Policy'},
    'lan_connectivity_policy': {'resource_path': '/vnic/LanConnectivityPolicies', 'object_type': 'vnic.LanConnectivityPolicy'},
    'ipmi_over_lan_policy': {'resource_path': '/ipmioverlan/Policies', 'object_type': 'ipmioverlan.Policy'},
    'kvm_policy': {'resource_path': '/kvm/Policies', 'object_type': 'kvm.Policy'},
    'network_connectivity_policy': {'resource_path': '/networkconfig/Policies', 'object_type': 'networkconfig.Policy'},
    'ntp_policy': {'resource_path': '/ntp/Policies', 'object_type': 'ntp.Policy'},
    'snmp_policy': {'resource_path': '/snmp/Policies', 'object_type': 'snmp.Policy'},
    'ssh_policy': {'resource_path': '/ssh/Policies', 'object_type': 'ssh.Policy'},
    'syslog_policy': {'resource_path': '/syslog/Policies', 'object_type': 'syslog.Policy'},
    'local_user_policy': {'resource_path': '/iam/EndPointUserPolicies', 'object_type': 'iam.EndPointUserPolicy'},
}


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        hardware_platform=dict(type='str', choices=['xe9305', 'xe130c_m8', 'xe150c_m8']),
        bios_policy=dict(type='str'),
        boot_order_policy=dict(type='str'),
        firmware_policy=dict(type='str'),
        storage_policy=dict(type='str'),
        thermal_policy=dict(type='str'),
        power_policy=dict(type='str'),
        lan_connectivity_policy=dict(type='str'),
        ipmi_over_lan_policy=dict(type='str'),
        kvm_policy=dict(type='str'),
        network_connectivity_policy=dict(type='str'),
        ntp_policy=dict(type='str'),
        snmp_policy=dict(type='str'),
        ssh_policy=dict(type='str'),
        syslog_policy=dict(type='str'),
        local_user_policy=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/server/ProfileTemplates'

    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
    }

    if module.params['state'] == 'present':
        if not module.params.get('hardware_platform'):
            module.fail_json(msg="hardware_platform is required when state is 'present'")

        intersight.set_tags_and_description()

        # Always set target platform to Unified Edge
        intersight.api_body['TargetPlatform'] = 'UnifiedEdgeServer'

        # Expose hardware constraints to the user
        platform = module.params['hardware_platform']
        intersight.result['hardware_constraints'] = HARDWARE_PLATFORMS[platform]

    intersight.configure_policy_or_profile(resource_path=resource_path)
    template_response = intersight.result['api_response']
    template_moid = template_response.get('Moid') if template_response else None

    # Sync PolicyBucket for attached policies
    if template_moid and module.params['state'] == 'present':
        organization_name = module.params['organization']
        desired_bucket = resolve_policy_bucket(intersight, organization_name, POLICY_MAPPING)
        current_bucket = template_response.get('PolicyBucket') or []
        bucket_path = '/server/ProfileTemplates/' + template_moid + '/PolicyBucket'
        sync_policy_bucket(intersight, bucket_path, desired_bucket, current_bucket)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
