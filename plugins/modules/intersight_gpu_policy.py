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
module: intersight_gpu_policy
short_description: GPU policy configuration for Cisco Intersight
description:
  - GPU policy configuration for Cisco Intersight.
  - Used to configure Multi-Instance GPU (MIG) partitioning and GPU assignment on server profiles.
  - Supports NVIDIA H100, B200, and other MIG-capable GPUs managed through Intersight.
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
      - The name assigned to the GPU policy.
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
      - The user-defined description of the GPU policy.
    type: str
    aliases: [descr]
  gpu_mode:
    description:
      - The operating mode for GPUs in the server.
      - C(graphics) configures GPUs for standard graphics/display use.
      - C(compute) configures GPUs for compute workloads (CUDA, inference, training).
    type: str
    choices: [graphics, compute]
    default: compute
  mig_enabled:
    description:
      - Enable or disable Multi-Instance GPU (MIG) partitioning.
      - When enabled, each physical GPU can be partitioned into multiple isolated GPU instances.
      - MIG is supported on NVIDIA A100, H100, B200 and newer architectures.
    type: bool
    default: false
  mig_profiles:
    description:
      - List of MIG partition profiles to apply when mig_enabled is true.
      - Each entry defines the partition configuration for a GPU slot.
      - If fewer profiles are specified than available GPUs, remaining GPUs use the default profile.
    type: list
    elements: dict
    suboptions:
      slot_id:
        description:
          - The GPU slot number (1-8) this profile applies to.
        type: int
        required: true
      partition_profile:
        description:
          - The MIG partition profile name.
          - Common profiles for H100/B200 include 1g.10gb, 2g.20gb, 3g.40gb, 4g.40gb, 7g.80gb.
          - Use C(none) to disable MIG on this specific slot.
        type: str
        required: true
      instance_count:
        description:
          - Number of MIG instances to create with the specified partition profile.
          - Maximum depends on the GPU model and partition profile selected.
        type: int
        default: 1
  gpu_thermal_threshold:
    description:
      - GPU thermal throttle threshold temperature in Celsius.
      - When GPU temperature exceeds this threshold, performance will be throttled to prevent damage.
      - Valid range depends on GPU model. Typical values are 80-95 for data center GPUs.
      - Set to 0 to use the platform default.
    type: int
  power_capping_enabled:
    description:
      - Enable or disable GPU power capping.
      - When enabled, GPU power consumption is limited to the power_cap_watts value.
    type: bool
    default: false
  power_cap_watts:
    description:
      - Maximum power consumption per GPU in watts when power_capping_enabled is true.
      - Valid range depends on GPU model (e.g., H100 SXM supports 300-700W).
      - Set to 0 to use the platform default TDP.
    type: int
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Create GPU compute policy without MIG
  cisco.intersight.intersight_gpu_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: AI-Factory
    name: gpu-compute-default
    description: Standard GPU compute mode for inference
    gpu_mode: compute

- name: Create GPU policy with MIG partitioning for H100
  cisco.intersight.intersight_gpu_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: gpu-mig-inference
    description: MIG partitioned for multi-tenant inference
    gpu_mode: compute
    mig_enabled: true
    mig_profiles:
      - slot_id: 1
        partition_profile: 3g.40gb
        instance_count: 2
      - slot_id: 2
        partition_profile: 7g.80gb
        instance_count: 1

- name: Create GPU policy with thermal and power limits
  cisco.intersight.intersight_gpu_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: gpu-power-managed
    description: Power-managed GPU policy for dense deployments
    gpu_mode: compute
    gpu_thermal_threshold: 85
    power_capping_enabled: true
    power_cap_watts: 400

- name: Delete GPU policy
  cisco.intersight.intersight_gpu_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: gpu-compute-default
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "gpu-compute-default",
        "ObjectType": "graphics.GpuPolicy",
        "GpuMode": "compute",
        "MigEnabled": false
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def main():
    mig_profile = dict(
        slot_id=dict(type='int', required=True),
        partition_profile=dict(type='str', required=True),
        instance_count=dict(type='int', default=1),
    )
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        gpu_mode=dict(type='str', choices=['graphics', 'compute'], default='compute'),
        mig_enabled=dict(type='bool', default=False),
        mig_profiles=dict(type='list', elements='dict', options=mig_profile),
        gpu_thermal_threshold=dict(type='int'),
        power_capping_enabled=dict(type='bool', default=False),
        power_cap_watts=dict(type='int'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/graphics/GpuPolicies'

    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
    }

    if module.params['state'] == 'present':
        intersight.set_tags_and_description()

        intersight.api_body['GpuMode'] = module.params['gpu_mode']
        intersight.api_body['MigEnabled'] = module.params['mig_enabled']

        # MIG partition profiles
        if module.params['mig_enabled'] and module.params.get('mig_profiles'):
            mig_configs = []
            for profile in module.params['mig_profiles']:
                mig_configs.append({
                    'SlotId': profile['slot_id'],
                    'PartitionProfile': profile['partition_profile'],
                    'InstanceCount': profile['instance_count'],
                })
            intersight.api_body['MigProfiles'] = mig_configs

        # Thermal threshold
        if module.params.get('gpu_thermal_threshold') is not None:
            intersight.api_body['GpuThermalThreshold'] = module.params['gpu_thermal_threshold']

        # Power capping
        if module.params['power_capping_enabled']:
            intersight.api_body['PowerCappingEnabled'] = True
            if module.params.get('power_cap_watts') is not None:
                intersight.api_body['PowerCapWatts'] = module.params['power_cap_watts']
        else:
            intersight.api_body['PowerCappingEnabled'] = False

    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
