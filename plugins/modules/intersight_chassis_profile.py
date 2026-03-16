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
module: intersight_chassis_profile
short_description: Manage Chassis Profiles in Cisco Intersight
description:
  - Create, update, and delete Chassis Profiles on Cisco Intersight.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/chassis/Profile/post/).
  - This module does not manage deployment of the chassis profile.
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
      - The name assigned to the Chassis Profile.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description of the Chassis Profile.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  assigned_chassis_name:
    description:
      - The name of the chassis to assign to this profile.
      - The module resolves the chassis name to a MOID via the C(/equipment/Chasses) API endpoint.
      - If not provided, the profile will be created without a chassis assignment.
    type: str
  imc_access_policy:
    description:
      - Name of IMC Access Policy to associate with this profile.
    type: str
  power_policy:
    description:
      - Name of Power Policy to associate with this profile.
    type: str
  snmp_policy:
    description:
      - Name of SNMP Policy to associate with this profile.
    type: str
  thermal_policy:
    description:
      - Name of Thermal Policy to associate with this profile.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a basic Chassis Profile
  cisco.intersight.intersight_chassis_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "Chassis-Profile-01"
    description: "Basic chassis profile"
    tags:
      - Key: "Environment"
        Value: "Production"
    state: present

- name: Create a Chassis Profile with chassis assignment and policies
  cisco.intersight.intersight_chassis_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "Chassis-Profile-02"
    description: "Chassis profile with assignment and policies"
    assigned_chassis_name: "FOX2534P0GG"
    imc_access_policy: "IMC-Access-Prod"
    power_policy: "Power-Grid-Redundancy"
    snmp_policy: "SNMP-Monitoring"
    thermal_policy: "Thermal-Balanced"
    state: present

- name: Delete a Chassis Profile
  cisco.intersight.intersight_chassis_profile:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "Chassis-Profile-01"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "Chassis-Profile-02",
        "ObjectType": "chassis.Profile",
        "AssignedChassis": {
            "Moid": "67e3ebbd61767530012e5a93",
            "ObjectType": "equipment.Chassis"
        },
        "PolicyBucket": [
            {
                "Moid": "69b2af9c6275723101974d23",
                "ObjectType": "access.Policy"
            },
            {
                "Moid": "69b2af9c6275723101974d24",
                "ObjectType": "power.Policy"
            }
        ],
        "Tags": [
            {
                "Key": "Environment",
                "Value": "Production"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import (
    IntersightModule,
    intersight_argument_spec,
    resolve_policy_bucket,
    sync_policy_bucket,
)


POLICY_MAPPING = {
    'imc_access_policy': {'resource_path': '/access/Policies', 'object_type': 'access.Policy'},
    'power_policy': {'resource_path': '/power/Policies', 'object_type': 'power.Policy'},
    'snmp_policy': {'resource_path': '/snmp/Policies', 'object_type': 'snmp.Policy'},
    'thermal_policy': {'resource_path': '/thermal/Policies', 'object_type': 'thermal.Policy'},
}


def resolve_assigned_chassis(intersight, chassis_name):
    """Resolve a chassis name to its MOID via the equipment/Chasses endpoint."""
    chassis_moid = intersight.get_moid_by_name(
        resource_path='/equipment/Chasses',
        resource_name=chassis_name,
    )
    if not chassis_moid:
        intersight.module.fail_json(
            msg=f"Chassis '{chassis_name}' not found. Verify the chassis name via GET /equipment/Chasses."
        )
    return chassis_moid


def unassign_chassis_if_needed(intersight, resource_path, profile_name, organization_moid):
    """Unassign the chassis from a profile before deletion.

    The Intersight API forbids deleting a chassis profile while a chassis is
    associated with it. This function checks for an existing assignment and
    PATCHes AssignedChassis to null when one is found.
    """
    filter_str = f"Name eq '{profile_name}' and Organization.Moid eq '{organization_moid}'"
    intersight.get_resource(
        resource_path=resource_path,
        query_params={'$filter': filter_str},
    )

    profile = intersight.result['api_response']
    if not profile.get('Moid'):
        return

    assigned = profile.get('AssignedChassis')
    if assigned and assigned.get('Moid'):
        intersight.configure_resource(
            moid=profile['Moid'],
            resource_path=resource_path,
            body={'AssignedChassis': None},
            query_params={},
        )


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        assigned_chassis_name=dict(type='str'),
        imc_access_policy=dict(type='str'),
        power_policy=dict(type='str'),
        snmp_policy=dict(type='str'),
        thermal_policy=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    resource_path = '/chassis/Profiles'

    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
    }

    if intersight.module.params['state'] == 'present':
        intersight.set_tags_and_description()

        chassis_name = intersight.module.params.get('assigned_chassis_name')
        if chassis_name:
            chassis_moid = resolve_assigned_chassis(intersight, chassis_name)
            intersight.api_body['AssignedChassis'] = {
                'Moid': chassis_moid,
                'ObjectType': 'equipment.Chassis',
            }

    if intersight.module.params['state'] == 'absent':
        organization_moid = intersight.get_moid_by_name(
            resource_path='/organization/Organizations',
            resource_name=intersight.module.params['organization'],
        )
        if organization_moid:
            unassign_chassis_if_needed(intersight, resource_path, intersight.module.params['name'], organization_moid)

    intersight.configure_policy_or_profile(resource_path=resource_path)
    profile_response = intersight.result['api_response']
    profile_moid = profile_response.get('Moid') if profile_response else None

    if profile_moid and intersight.module.params['state'] == 'present':
        organization_name = intersight.module.params['organization']
        desired_bucket = resolve_policy_bucket(intersight, organization_name, POLICY_MAPPING)
        current_bucket = profile_response.get('PolicyBucket') or []
        bucket_path = f'/chassis/Profiles/{profile_moid}/PolicyBucket'
        sync_policy_bucket(intersight, bucket_path, desired_bucket, current_bucket)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
