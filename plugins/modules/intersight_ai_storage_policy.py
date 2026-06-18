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
module: intersight_ai_storage_policy
short_description: AI-optimized storage policy for Cisco Intersight
description:
  - Creates storage policies optimized for AI workloads including inference model storage,
    training data, and telemetry caches.
  - Provides named storage presets that configure NVMe tiering, drive groups, and
    virtual drive layouts for common AI deployment patterns.
  - Builds on the Intersight storage policy API with AI-specific defaults for
    high-throughput, low-latency access to model weights and datasets.
  - For full storage configuration control, use M(cisco.intersight.intersight_storage_policy) instead.
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
      - The name assigned to the storage policy.
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
      - The user-defined description of the storage policy.
    type: str
    aliases: [descr]
  storage_profile:
    description:
      - The AI storage preset profile to apply.
      - C(inference_optimized) configures NVMe drives in direct-attach mode for lowest latency
        access to model weights. Sets all available NVMe slots to direct-attach, disables
        JBOD for VD creation, and uses RAID0 with read-ahead caching for maximum throughput.
      - C(training_data) configures storage for large dataset access during training.
        Uses RAID5/RAID6 for data protection with write-back caching and larger strip sizes
        for sequential read throughput.
      - C(model_cache) configures a fast NVMe cache tier for model artifacts with M.2 boot.
        Enables M.2 virtual drive for OS boot and sets remaining NVMe drives to direct-attach
        for model weight caching.
      - C(edge_compact) configures storage for Unified Edge nodes with limited drive bays.
        Uses M.2 boot with minimal RAID0 configuration suitable for edge inference with
        constrained storage capacity.
    type: str
    choices: [inference_optimized, training_data, model_cache, edge_compact]
  nvme_slots:
    description:
      - NVMe drive slots to configure in the selected mode.
      - Overrides the default slot configuration from the storage profile.
      - Allowed slots are 1-9, 21-24, 101-104.
      - 'Slot format examples: "1,4,5", "2", "1-5", "1,2,6-8"'
    type: str
  nvme_mode:
    description:
      - Override the NVMe attachment mode.
      - C(direct) attaches NVMe drives directly to the CPU for lowest latency.
      - C(controller) routes NVMe through the RAID controller for management features.
    type: str
    choices: [direct, controller]
  m2_boot_enabled:
    description:
      - Override whether to enable M.2 RAID boot drive.
      - When true, configures M.2 MSTOR-RAID-1 as the boot virtual drive.
    type: bool
  raid_level:
    description:
      - Override the RAID level for data drive groups.
      - Only applicable for training_data profile.
    type: str
    choices: [Raid0, Raid1, Raid5, Raid6, Raid10]
  read_policy:
    description:
      - Override the read cache policy for virtual drives.
    type: str
    choices: [Default, ReadAhead, NoReadAhead]
  write_policy:
    description:
      - Override the write cache policy for virtual drives.
    type: str
    choices: [Default, WriteThrough, WriteBackGoodBbu, AlwaysWriteBack]
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Create inference-optimized storage policy
  cisco.intersight.intersight_ai_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: AI-Factory
    name: storage-ai-inference
    description: NVMe direct-attach for model weight storage
    storage_profile: inference_optimized

- name: Create training data storage policy with RAID6
  cisco.intersight.intersight_ai_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: storage-ai-training
    description: Protected storage for training datasets
    storage_profile: training_data
    raid_level: Raid6
    write_policy: AlwaysWriteBack

- name: Create model cache storage for inference servers
  cisco.intersight.intersight_ai_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: storage-model-cache
    description: M.2 boot with NVMe model cache
    storage_profile: model_cache
    nvme_slots: "1-4"

- name: Create edge storage policy
  cisco.intersight.intersight_ai_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: storage-edge-inference
    storage_profile: edge_compact

- name: Delete AI storage policy
  cisco.intersight.intersight_ai_storage_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: storage-ai-inference
    storage_profile: inference_optimized
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "storage-ai-inference",
        "ObjectType": "storage.StoragePolicy",
        "DirectAttachedNvmeSlots": "1-4"
    }
applied_settings:
  description: The storage settings applied by the profile and any overrides.
  returned: when state is present
  type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


# Default NVMe slot ranges
DEFAULT_NVME_SLOTS = '1-4'

# Storage profile presets
STORAGE_PROFILES = {
    'inference_optimized': {
        # All NVMe direct-attach for lowest latency model access
        'DirectAttachedNvmeSlots': DEFAULT_NVME_SLOTS,
        'UseJbodForVdCreation': False,
        'UnusedDisksState': 'NoChange',
        'DefaultDriveMode': 'UnconfiguredGood',
        'M2VirtualDrive': {
            'Enable': False,
            'ControllerSlot': 'MSTOR-RAID-1',
            'Name': 'MStorBootVd',
        },
        'Raid0Drive': {
            'Enable': True,
            'VirtualDrivePolicy': {
                'StripSize': 256,
                'AccessPolicy': 'ReadWrite',
                'ReadPolicy': 'ReadAhead',
                'WritePolicy': 'WriteThrough',
                'DriveCache': 'Enable',
            },
        },
    },
    'training_data': {
        # RAID-protected storage for training datasets
        'UseJbodForVdCreation': False,
        'UnusedDisksState': 'UnconfiguredGood',
        'DefaultDriveMode': 'UnconfiguredGood',
        'M2VirtualDrive': {
            'Enable': True,
            'ControllerSlot': 'MSTOR-RAID-1',
            'Name': 'MStorBootVd',
        },
        'Raid0Drive': {
            'Enable': False,
            'VirtualDrivePolicy': {
                'StripSize': 512,
                'AccessPolicy': 'ReadWrite',
                'ReadPolicy': 'ReadAhead',
                'WritePolicy': 'WriteBackGoodBbu',
                'DriveCache': 'Enable',
            },
        },
        '_raid_level': 'Raid5',
        '_read_policy': 'ReadAhead',
        '_write_policy': 'WriteBackGoodBbu',
    },
    'model_cache': {
        # M.2 boot + NVMe direct-attach model cache
        'DirectAttachedNvmeSlots': DEFAULT_NVME_SLOTS,
        'UseJbodForVdCreation': False,
        'UnusedDisksState': 'NoChange',
        'DefaultDriveMode': 'UnconfiguredGood',
        'M2VirtualDrive': {
            'Enable': True,
            'ControllerSlot': 'MSTOR-RAID-1',
            'Name': 'MStorBootVd',
        },
        'Raid0Drive': {
            'Enable': False,
            'VirtualDrivePolicy': {
                'StripSize': 64,
                'AccessPolicy': 'Default',
                'ReadPolicy': 'Default',
                'WritePolicy': 'Default',
                'DriveCache': 'Default',
            },
        },
    },
    'edge_compact': {
        # Minimal storage for edge nodes
        'UseJbodForVdCreation': False,
        'UnusedDisksState': 'NoChange',
        'DefaultDriveMode': 'UnconfiguredGood',
        'M2VirtualDrive': {
            'Enable': True,
            'ControllerSlot': 'MSTOR-RAID-1',
            'Name': 'MStorBootVd',
        },
        'Raid0Drive': {
            'Enable': True,
            'VirtualDrivePolicy': {
                'StripSize': 64,
                'AccessPolicy': 'ReadWrite',
                'ReadPolicy': 'ReadAhead',
                'WritePolicy': 'WriteThrough',
                'DriveCache': 'Default',
            },
        },
    },
}


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        storage_profile=dict(
            type='str',
            choices=['inference_optimized', 'training_data', 'model_cache', 'edge_compact'],
        ),
        nvme_slots=dict(type='str'),
        nvme_mode=dict(type='str', choices=['direct', 'controller']),
        m2_boot_enabled=dict(type='bool'),
        raid_level=dict(type='str', choices=['Raid0', 'Raid1', 'Raid5', 'Raid6', 'Raid10']),
        read_policy=dict(type='str', choices=['Default', 'ReadAhead', 'NoReadAhead']),
        write_policy=dict(type='str', choices=['Default', 'WriteThrough', 'WriteBackGoodBbu', 'AlwaysWriteBack']),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/storage/StoragePolicies'

    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
    }

    if module.params['state'] == 'present':
        if not module.params.get('storage_profile'):
            module.fail_json(msg="storage_profile is required when state is 'present'")

        intersight.set_tags_and_description()

        # Deep copy profile settings
        profile_name = module.params['storage_profile']
        import copy
        settings = copy.deepcopy(STORAGE_PROFILES[profile_name])

        # Remove internal metadata keys
        settings.pop('_raid_level', None)
        settings.pop('_read_policy', None)
        settings.pop('_write_policy', None)

        # Apply NVMe slot overrides
        if module.params.get('nvme_slots') is not None:
            nvme_mode = module.params.get('nvme_mode', 'direct')
            if nvme_mode == 'direct':
                settings['DirectAttachedNvmeSlots'] = module.params['nvme_slots']
                settings.pop('ControllerAttachedNvmeSlots', None)
            else:
                settings['ControllerAttachedNvmeSlots'] = module.params['nvme_slots']
                settings.pop('DirectAttachedNvmeSlots', None)
        elif module.params.get('nvme_mode') is not None:
            # Mode override without slot override — move existing slots
            nvme_slots = settings.pop('DirectAttachedNvmeSlots', settings.pop('ControllerAttachedNvmeSlots', None))
            if nvme_slots:
                if module.params['nvme_mode'] == 'direct':
                    settings['DirectAttachedNvmeSlots'] = nvme_slots
                else:
                    settings['ControllerAttachedNvmeSlots'] = nvme_slots

        # Apply M.2 boot override
        if module.params.get('m2_boot_enabled') is not None:
            settings['M2VirtualDrive']['Enable'] = module.params['m2_boot_enabled']

        # Apply cache policy overrides to RAID0 drive config
        if module.params.get('read_policy') is not None:
            settings['Raid0Drive']['VirtualDrivePolicy']['ReadPolicy'] = module.params['read_policy']
        if module.params.get('write_policy') is not None:
            settings['Raid0Drive']['VirtualDrivePolicy']['WritePolicy'] = module.params['write_policy']

        intersight.api_body.update(settings)
        intersight.result['applied_settings'] = settings

    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
