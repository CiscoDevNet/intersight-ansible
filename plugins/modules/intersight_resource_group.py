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
module: intersight_resource_group
short_description: Resource Group configuration for Cisco Intersight
description:
  - Manages Resource Group configuration on Cisco Intersight.
  - Resource Groups define a set of resources that can be used for access control and organization assignment.
  - Users specify Intersight-managed UCS domains by their target name (as shown in the Intersight Targets page).
  - Optionally, specific servers (sub-targets) within a domain can be selected by serial number.
  - Resource Groups are account-level resources and are not scoped to an organization.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/resource/Group/model/).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    type: str
    choices: [present, absent]
    default: present
  name:
    description:
      - The name assigned to the Resource Group.
      - The name must be between 1 and 64 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description for the Resource Group.
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  resources:
    description:
      - List of Intersight-managed UCS domain resources to include in the Resource Group.
      - Required when O(state) is C(present).
      - Each entry specifies a domain by its target name as shown in the Intersight GUI Targets page.
      - When O(resources[].sub_targets) is provided, only the specified servers (by serial number) are included instead of the full domain.
      - Multiple entries can be mixed, some with sub-targets and some without.
    type: list
    elements: dict
    suboptions:
      domain_name:
        description:
          - The name of the Intersight-managed UCS domain target.
          - Must match the target name exactly as displayed in the Intersight Targets page.
        type: str
        required: true
      sub_targets:
        description:
          - List of server serial numbers to include as sub-targets within the domain.
          - When specified, only these servers are included instead of the entire domain.
          - Servers are automatically classified as Blades or RackUnits via the Intersight API.
        type: list
        elements: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create Resource Group for full UCS domains
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "ucs-domains-group"
    description: "Resource group for two UCS domains"
    resources:
      - domain_name: "ucs-domain-1"
      - domain_name: "ucs-domain-2"
    state: present

- name: Create Resource Group with sub-targets (specific servers)
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "specific-servers-group"
    description: "Only specific servers from the domain"
    resources:
      - domain_name: "ucs-domain-1"
        sub_targets:
          - "FCH26387BD1"
          - "FCH243974ZD"
          - "WZP26030TAV"
    state: present

- name: Create Resource Group with mixed resources
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "mixed-resources-group"
    description: "Full domain and specific servers from another"
    resources:
      - domain_name: "ucs-domain-1"
      - domain_name: "ucs-domain-2"
        sub_targets:
          - "FCH26387BD1"
          - "WZP26030TAV"
    state: present

- name: Delete Resource Group
  cisco.intersight.intersight_resource_group:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "ucs-domains-group"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "ucs-domains-group",
        "ObjectType": "resource.Group",
        "Description": "Resource group for two UCS domains",
        "Moid": "507f1f77bcf86cd799439099"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def resolve_domain_device_registration(intersight, domain_name):
    """Resolve a domain target name to its DeviceRegistration Moid."""
    intersight.get_resource(
        resource_path='/asset/Targets',
        query_params={
            '$filter': f"Name eq '{domain_name}' and TargetType eq 'UCSFIISM'",
            '$select': 'Name,RegisteredDevice',
            '$expand': 'RegisteredDevice($select=Moid)',
        },
    )

    target = intersight.result['api_response']
    if not target.get('Moid'):
        intersight.module.fail_json(
            msg=f"Intersight-managed UCS domain target '{domain_name}' not found. "
                "Verify the target name matches exactly as shown in the Intersight Targets page."
        )

    registered_device = target.get('RegisteredDevice', {})
    device_reg_moid = registered_device.get('Moid')
    if not device_reg_moid:
        intersight.module.fail_json(
            msg=f"Domain target '{domain_name}' has no associated DeviceRegistration. "
                "Ensure the domain is properly claimed and connected."
        )

    return device_reg_moid


def classify_serial_numbers(intersight, serials):
    """Classify serial numbers as Blade or RackUnit via PhysicalSummaries.

    Returns:
        Tuple of (blade_serials, rack_serials) lists.
    """
    serials_filter = ",".join(f"'{s}'" for s in serials)
    intersight.get_resource(
        resource_path='/compute/PhysicalSummaries',
        query_params={
            '$filter': f"Serial in ({serials_filter}) and ManagementMode eq 'Intersight'",
            '$select': 'Serial,SourceObjectType',
        },
        return_list=True,
    )

    results = intersight.result['api_response']
    if not isinstance(results, list):
        results = [results] if results else []

    found_serials = {}
    for entry in results:
        serial = entry.get('Serial')
        obj_type = entry.get('SourceObjectType', '')
        if serial:
            found_serials[serial] = obj_type

    missing = set(serials) - set(found_serials.keys())
    if missing:
        intersight.module.fail_json(
            msg=f"The following serial numbers were not found as Intersight-managed servers: {sorted(missing)}"
        )

    blade_serials = [s for s in serials if 'Blade' in found_serials[s]]
    rack_serials = [s for s in serials if 'RackUnit' in found_serials[s]]

    return blade_serials, rack_serials


def resolve_resources_to_selectors(intersight, resources):
    """Resolve user-provided resources into API selector strings."""
    device_reg_moids = []
    all_blade_serials = []
    all_rack_serials = []

    for resource in resources:
        domain_name = resource['domain_name']
        sub_targets = resource.get('sub_targets')

        if sub_targets:
            blade_serials, rack_serials = classify_serial_numbers(intersight, sub_targets)
            all_blade_serials.extend(blade_serials)
            all_rack_serials.extend(rack_serials)
        else:
            moid = resolve_domain_device_registration(intersight, domain_name)
            device_reg_moids.append(moid)

    selectors = []

    if device_reg_moids:
        moids_str = ",".join(f"'{m}'" for m in device_reg_moids)
        selectors.append(
            f"/api/v1/asset/DeviceRegistrations?$filter=Moid in ({moids_str})"
        )

    if all_blade_serials:
        serials_str = ",".join(f"'{s}'" for s in all_blade_serials)
        selectors.append(
            f"/api/v1/compute/Blades?$filter=Serial in ({serials_str}) and ManagementMode eq 'Intersight'"
        )

    if all_rack_serials:
        serials_str = ",".join(f"'{s}'" for s in all_rack_serials)
        selectors.append(
            f"/api/v1/compute/RackUnits?$filter=Serial in ({serials_str}) and ManagementMode eq 'Intersight'"
        )

    return selectors


def build_api_body(intersight):
    """Build the API body for Resource Group configuration."""
    params = intersight.module.params
    if params['state'] == 'present':
        selectors = resolve_resources_to_selectors(intersight, params['resources'])

        intersight.api_body = {
            'Name': params['name'],
            'Qualifier': 'Allow-Selectors',
            'Selectors': [{'Selector': s} for s in selectors],
        }

        intersight.set_tags_and_description()


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        resources=dict(type='list', elements='dict', options=dict(
            domain_name=dict(type='str', required=True),
            sub_targets=dict(type='list', elements='str'),
        )),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'present', ['resources']],
        ],
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    build_api_body(intersight)

    resource_path = '/resource/Groups'

    intersight.configure_secondary_resource(
        resource_path=resource_path,
        resource_name=module.params['name'],
        state=module.params['state'],
    )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
