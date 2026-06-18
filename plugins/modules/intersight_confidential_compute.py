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
module: intersight_confidential_compute
short_description: Confidential computing BIOS policy for Cisco Intersight
description:
  - Creates BIOS policies with hardware-level confidential computing features enabled.
  - Supports AMD SEV (Secure Encrypted Virtualization), AMD SEV-SNP, and Intel SGX
    (Software Guard Extensions) for secure AI enclaves.
  - Combines the correct BIOS knob settings needed to enable memory encryption and
    trusted execution environments on Cisco UCS servers.
  - Intended for AI workloads that require protection of proprietary model data in memory.
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
  security_profile:
    description:
      - The confidential computing security profile to apply.
      - C(amd_sev) enables AMD Secure Encrypted Virtualization with memory encryption for VMs.
        Encrypts VM memory with per-VM keys so the hypervisor cannot read guest data.
        Requires AMD EPYC processors (Milan/Genoa or later).
      - C(amd_sev_snp) enables AMD SEV with Secure Nested Paging for stronger isolation.
        Adds integrity protection on top of SEV memory encryption, preventing hypervisor
        tampering with guest memory mappings. Requires AMD EPYC Genoa or later.
      - C(intel_sgx) enables Intel Software Guard Extensions for application-level enclaves.
        Creates hardware-encrypted memory enclaves that protect specific application data
        even from the OS and hypervisor. Requires Intel Xeon Scalable (Ice Lake or later).
      - C(intel_sgx_with_auto_reg) enables Intel SGX with automatic registration agent.
        Includes all intel_sgx settings plus enables the SGX auto-registration agent for
        simplified attestation service enrollment.
    type: str
    choices: [amd_sev, amd_sev_snp, intel_sgx, intel_sgx_with_auto_reg]
  sev_asid_count:
    description:
      - Number of AMD SEV Address Space Identifiers (ASIDs) to allocate.
      - Higher ASID counts allow more concurrent encrypted VMs but may reduce available ASIDs for SEV-SNP.
      - Only applicable for amd_sev and amd_sev_snp security profiles.
    type: str
    choices: [platform-default, '253 ASIDs', '509 ASIDs']
  sgx_epoch0:
    description:
      - Intel SGX Epoch 0 value. Changing this invalidates all existing SGX sealed data.
      - Only applicable for intel_sgx and intel_sgx_with_auto_reg profiles.
      - Use with caution in production environments.
    type: str
  sgx_epoch1:
    description:
      - Intel SGX Epoch 1 value. Changing this invalidates all existing SGX sealed data.
      - Only applicable for intel_sgx and intel_sgx_with_auto_reg profiles.
      - Use with caution in production environments.
    type: str
  enable_tme:
    description:
      - Override for Intel Total Memory Encryption (TME).
      - TME is a prerequisite for SGX and encrypts all system memory with a platform key.
      - Automatically enabled by intel_sgx profiles; set explicitly only to override.
    type: str
    choices: [platform-default, enabled, disabled]
  numa_optimized:
    description:
      - Override for NUMA optimization.
      - All confidential compute profiles enable NUMA optimization by default.
    type: str
    choices: [platform-default, enabled, disabled]
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Create AMD SEV policy for encrypted AI VMs
  cisco.intersight.intersight_confidential_compute:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: AI-Factory
    name: bios-amd-sev-ai
    description: AMD SEV for secure AI inference VMs
    security_profile: amd_sev
    sev_asid_count: "509 ASIDs"

- name: Create AMD SEV-SNP policy for maximum VM isolation
  cisco.intersight.intersight_confidential_compute:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-sev-snp-training
    description: SEV-SNP for secure model training
    security_profile: amd_sev_snp

- name: Create Intel SGX policy for enclave-based inference
  cisco.intersight.intersight_confidential_compute:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-sgx-inference
    description: SGX enclaves for confidential inference
    security_profile: intel_sgx_with_auto_reg

- name: Delete confidential compute policy
  cisco.intersight.intersight_confidential_compute:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: bios-amd-sev-ai
    security_profile: amd_sev
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "bios-amd-sev-ai",
        "ObjectType": "bios.Policy",
        "Sev": "509 ASIDs",
        "CbsSevSnpSupport": "enabled"
    }
applied_settings:
  description: The BIOS settings applied by the security profile and any overrides.
  returned: when state is present
  type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


# Confidential computing security profile presets
SECURITY_PROFILES = {
    'amd_sev': {
        # AMD SEV - memory encryption for VMs
        'Sev': '509 ASIDs',
        # NUMA optimization for consistent memory locality
        'NumaOptimized': 'enabled',
        # IOMMU required for SEV
        'CbsDfCmnDramNps': 'Auto',
        # SMT enabled for VM density
        'CpuHwpm': 'HWPM Native Mode',
    },
    'amd_sev_snp': {
        # AMD SEV-SNP - memory encryption + integrity protection
        'Sev': '509 ASIDs',
        'CbsSevSnpSupport': 'enabled',
        'NumaOptimized': 'enabled',
        'CbsDfCmnDramNps': 'Auto',
        'CpuHwpm': 'HWPM Native Mode',
    },
    'intel_sgx': {
        # Intel SGX - application-level enclaves
        'EnableSgx': 'enabled',
        'EnableTme': 'enabled',
        'NumaOptimized': 'enabled',
        'CpuHwpm': 'HWPM Native Mode',
    },
    'intel_sgx_with_auto_reg': {
        # Intel SGX with auto-registration for attestation
        'EnableSgx': 'enabled',
        'EnableTme': 'enabled',
        'SgxAutoRegistrationAgent': 'enabled',
        'NumaOptimized': 'enabled',
        'CpuHwpm': 'HWPM Native Mode',
    },
}

# Map of override parameter names to API property names
OVERRIDE_MAP = {
    'enable_tme': 'EnableTme',
    'numa_optimized': 'NumaOptimized',
}


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        security_profile=dict(
            type='str',
            choices=['amd_sev', 'amd_sev_snp', 'intel_sgx', 'intel_sgx_with_auto_reg'],
        ),
        sev_asid_count=dict(type='str', choices=['platform-default', '253 ASIDs', '509 ASIDs']),
        sgx_epoch0=dict(type='str'),
        sgx_epoch1=dict(type='str'),
        enable_tme=dict(type='str', choices=['platform-default', 'enabled', 'disabled']),
        numa_optimized=dict(type='str', choices=['platform-default', 'enabled', 'disabled']),
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
        if not module.params.get('security_profile'):
            module.fail_json(msg="security_profile is required when state is 'present'")

        intersight.set_tags_and_description()

        # Apply security profile preset
        profile_name = module.params['security_profile']
        profile_settings = SECURITY_PROFILES[profile_name].copy()

        # Apply SEV ASID count override for AMD profiles
        if module.params.get('sev_asid_count') is not None and profile_name in ('amd_sev', 'amd_sev_snp'):
            profile_settings['Sev'] = module.params['sev_asid_count']

        # Apply SGX epoch overrides for Intel profiles
        if profile_name in ('intel_sgx', 'intel_sgx_with_auto_reg'):
            if module.params.get('sgx_epoch0') is not None:
                profile_settings['SgxEpoch0'] = module.params['sgx_epoch0']
            if module.params.get('sgx_epoch1') is not None:
                profile_settings['SgxEpoch1'] = module.params['sgx_epoch1']

        # Apply generic overrides
        for param_name, api_property in OVERRIDE_MAP.items():
            if module.params.get(param_name) is not None:
                profile_settings[api_property] = module.params[param_name]

        intersight.api_body.update(profile_settings)
        intersight.result['applied_settings'] = profile_settings

    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
