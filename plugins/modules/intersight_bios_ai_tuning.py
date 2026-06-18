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
module: intersight_bios_ai_tuning
short_description: AI-optimized BIOS policy presets for Cisco Intersight
description:
  - Creates BIOS policies with pre-validated settings optimized for AI and GPU workloads.
  - Provides named tuning profiles that set multiple BIOS knobs at once for common AI use cases.
  - Profiles target NVIDIA H100/B200 GPU servers and Intel/AMD CPU platforms used in Cisco AI Factory.
  - Individual BIOS knobs can be overridden after the preset is applied.
  - For full BIOS knob control, use M(cisco.intersight.intersight_bios_policy) instead.
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
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    type: str
    default: default
  name:
    description:
      - The name assigned to the BIOS policy.
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
      - The user-defined description of the BIOS policy.
    type: str
    aliases: [descr]
  tuning_profile:
    description:
      - The AI tuning profile preset to apply.
      - C(gpu_inference) optimizes for maximum GPU throughput with low-latency memory access.
        Sets GPU ACS control enabled, NUMA optimized, hardware P-states disabled for consistent
        performance, SR-IOV enabled, and memory interleave optimized.
      - C(gpu_training) optimizes for large-scale GPU training workloads with maximum memory
        bandwidth. Includes all gpu_inference settings plus maximum power performance tuning,
        workload configuration set to balanced, and package C-state limit for sustained throughput.
      - C(cpu_inference) optimizes for CPU-based inference with low-latency tuning.
        Enables hardware P-states for native performance, Intel Turbo Boost, LLC prefetch,
        and NUMA optimization without GPU-specific settings.
      - C(edge_ai) optimizes for Cisco Unified Edge nodes with power-aware AI tuning.
        Balances performance with power efficiency using energy-efficient turbo, hardware P-states,
        and NUMA optimization suitable for edge deployment constraints.
    type: str
    choices: [gpu_inference, gpu_training, cpu_inference, edge_ai]
  gpu_count:
    description:
      - Number of GPUs to enable via ACS Control (1-8).
      - Only applicable for gpu_inference and gpu_training profiles.
      - GPUs beyond this count will have ACS control set to platform-default.
    type: int
    default: 8
  numa_optimized:
    description:
      - Override the NUMA optimization setting from the tuning profile.
    type: str
    choices: [platform-default, enabled, disabled]
  cpu_power_management:
    description:
      - Override the CPU power management setting from the tuning profile.
    type: str
    choices: [platform-default, performance, energy-efficient, custom]
  sriov:
    description:
      - Override the SR-IOV setting from the tuning profile.
      - SR-IOV is required for GPU passthrough in virtualized environments.
    type: str
    choices: [platform-default, enabled, disabled]
  intel_turbo_boost_tech:
    description:
      - Override the Intel Turbo Boost Technology setting.
    type: str
    choices: [platform-default, enabled, disabled]
  cpu_performance:
    description:
      - Override the CPU performance setting from the tuning profile.
    type: str
    choices: [platform-default, custom, enterprise, high-throughput, hpc]
  cpu_energy_performance:
    description:
      - Override the CPU energy performance bias setting.
    type: str
    choices: [platform-default, balanced-energy, balanced-performance, energy-efficient, performance]
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Create GPU inference optimized BIOS policy for 8-GPU server
  cisco.intersight.intersight_bios_ai_tuning:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: AI-Factory
    name: bios-gpu-inference-h100
    description: BIOS tuning for H100 GPU inference servers
    tuning_profile: gpu_inference
    gpu_count: 8

- name: Create GPU training BIOS policy with power override
  cisco.intersight.intersight_bios_ai_tuning:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-gpu-training
    tuning_profile: gpu_training
    cpu_power_management: performance

- name: Create CPU inference BIOS policy for non-GPU workloads
  cisco.intersight.intersight_bios_ai_tuning:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-cpu-inference
    tuning_profile: cpu_inference
    intel_turbo_boost_tech: enabled

- name: Create edge AI BIOS policy for Unified Edge nodes
  cisco.intersight.intersight_bios_ai_tuning:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-edge-ai
    tuning_profile: edge_ai
    gpu_count: 2

- name: Delete AI BIOS policy
  cisco.intersight.intersight_bios_ai_tuning:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-gpu-inference-h100
    tuning_profile: gpu_inference
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "bios-gpu-inference-h100",
        "ObjectType": "bios.Policy",
        "NumaOptimized": "enabled",
        "AcsControlGpu1state": "enabled"
    }
applied_settings:
  description: The BIOS settings applied by the tuning profile and any overrides.
  returned: when state is present
  type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


# AI tuning profile presets
# Each profile maps Intersight BIOS API property names to their values.
TUNING_PROFILES = {
    'gpu_inference': {
        # NUMA and memory optimization
        'NumaOptimized': 'enabled',
        'CbsDfCmnAcpiSratL3numa': 'enabled',
        # CPU performance - disable P-states for consistent GPU-driven latency
        'CpuPowerManagement': 'performance',
        'CpuPerformance': 'high-throughput',
        'CpuEnergyPerformance': 'performance',
        'PackageCstateLimit': 'C0 C1 State',
        'AutonomousCstateEnable': 'disabled',
        'CpuHwpm': 'Disabled',
        # GPU and I/O
        'SrIov': 'enabled',
        'AcsControlSlot11state': 'enabled',
        'AcsControlSlot12state': 'enabled',
        'AcsControlSlot13state': 'enabled',
        'AcsControlSlot14state': 'enabled',
        # Memory performance
        'LlcPrefetch': 'enabled',
        'XptPrefetch': 'enabled',
    },
    'gpu_training': {
        # All gpu_inference settings plus maximum power
        'NumaOptimized': 'enabled',
        'CbsDfCmnAcpiSratL3numa': 'enabled',
        'CpuPowerManagement': 'performance',
        'CpuPerformance': 'high-throughput',
        'CpuEnergyPerformance': 'performance',
        'PackageCstateLimit': 'C0 C1 State',
        'AutonomousCstateEnable': 'disabled',
        'CpuHwpm': 'Disabled',
        'SrIov': 'enabled',
        'AcsControlSlot11state': 'enabled',
        'AcsControlSlot12state': 'enabled',
        'AcsControlSlot13state': 'enabled',
        'AcsControlSlot14state': 'enabled',
        'LlcPrefetch': 'enabled',
        'XptPrefetch': 'enabled',
        # Training-specific: maximum power and bandwidth
        'WorkloadConfig': 'Balanced',
    },
    'cpu_inference': {
        # CPU-optimized for inference without GPU focus
        'NumaOptimized': 'enabled',
        'CbsDfCmnAcpiSratL3numa': 'enabled',
        'CpuPowerManagement': 'performance',
        'CpuPerformance': 'high-throughput',
        'CpuEnergyPerformance': 'performance',
        'IntelTurboBoostTech': 'enabled',
        'CpuHwpm': 'HWPM Native Mode',
        'LlcPrefetch': 'enabled',
        'XptPrefetch': 'enabled',
    },
    'edge_ai': {
        # Power-aware AI tuning for edge nodes
        'NumaOptimized': 'enabled',
        'CpuPowerManagement': 'energy-efficient',
        'CpuPerformance': 'enterprise',
        'CpuEnergyPerformance': 'balanced-performance',
        'EnergyEfficientTurbo': 'enabled',
        'IntelTurboBoostTech': 'enabled',
        'CpuHwpm': 'HWPM Native Mode',
        'LlcPrefetch': 'enabled',
    },
}

# GPU ACS control API property names by slot index (1-8)
GPU_ACS_PROPERTIES = [
    'AcsControlGpu1state',
    'AcsControlGpu2state',
    'AcsControlGpu3state',
    'AcsControlGpu4state',
    'AcsControlGpu5state',
    'AcsControlGpu6state',
    'AcsControlGpu7state',
    'AcsControlGpu8state',
]

# Map of override parameter names to API property names
OVERRIDE_MAP = {
    'numa_optimized': 'NumaOptimized',
    'cpu_power_management': 'CpuPowerManagement',
    'sriov': 'SrIov',
    'intel_turbo_boost_tech': 'IntelTurboBoostTech',
    'cpu_performance': 'CpuPerformance',
    'cpu_energy_performance': 'CpuEnergyPerformance',
}


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        tuning_profile=dict(type='str', choices=['gpu_inference', 'gpu_training', 'cpu_inference', 'edge_ai']),
        gpu_count=dict(type='int', default=8),
        numa_optimized=dict(type='str', choices=['platform-default', 'enabled', 'disabled']),
        cpu_power_management=dict(type='str', choices=['platform-default', 'performance', 'energy-efficient', 'custom']),
        sriov=dict(type='str', choices=['platform-default', 'enabled', 'disabled']),
        intel_turbo_boost_tech=dict(type='str', choices=['platform-default', 'enabled', 'disabled']),
        cpu_performance=dict(type='str', choices=['platform-default', 'custom', 'enterprise', 'high-throughput', 'hpc']),
        cpu_energy_performance=dict(
            type='str',
            choices=['platform-default', 'balanced-energy', 'balanced-performance', 'energy-efficient', 'performance']
        ),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/bios/Policies'

    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
    }

    if module.params['state'] == 'present':
        if not module.params.get('tuning_profile'):
            module.fail_json(msg="tuning_profile is required when state is 'present'")

        intersight.set_tags_and_description()

        # Apply tuning profile preset
        profile_name = module.params['tuning_profile']
        profile_settings = TUNING_PROFILES[profile_name].copy()

        # Apply GPU ACS control based on gpu_count for GPU profiles
        if profile_name in ('gpu_inference', 'gpu_training'):
            gpu_count = min(max(module.params['gpu_count'], 0), 8)
            for i, prop in enumerate(GPU_ACS_PROPERTIES):
                profile_settings[prop] = 'enabled' if i < gpu_count else 'platform-default'

        # Apply user overrides
        for param_name, api_property in OVERRIDE_MAP.items():
            if module.params.get(param_name) is not None:
                profile_settings[api_property] = module.params[param_name]

        intersight.api_body.update(profile_settings)
        intersight.result['applied_settings'] = profile_settings

    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
