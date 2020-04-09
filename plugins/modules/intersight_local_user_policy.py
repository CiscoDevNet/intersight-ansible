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
module: intersight_local_user_policy
short_description: Local User Policy configuration for Cisco Intersight
description:
  - Local User Policy configuration for Cisco Intersight.
  - Used to configure local users on endpoint devices.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    choices: [present, absent]
    default: present
  name:
    description:
      - The name assigned to the Local User Policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
  descrption:
    description:
      - The user-defined description of the Local User policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
  enforce_strong_password:
    description:
      - If true, enables a strong password policy.
      - Strong password requirements:.
      - A. The password must have a minimum of 8 and a maximum of 20 characters.
      - B. The password must not contain the User's Name.
      - C. The password must contain characters from three of the following four categories.
      - 1) English uppercase characters (A through Z).
      - 2) English lowercase characters (a through z).
      - 3) Base 10 digits (0 through 9).
      - 4) Non-alphabetic characters (! , @, '#', $, %, ^, &, *, -, _, +, =).
    type: bool
    default: true
  enable_password_expiry:
    description:
      - Enables password expiry on the endpoint.
    type: bool
    default: false
  password_history:
    description:
      - Specifies number of times a password cannot repeat when changed (value between 0 and 5).
      - Entering 0 disables this option.
    type: int
    default: 5
  local_users:
    description:
      - List of local users on the endpoint.
      - An admin user already exists on the endpoint.
      - Add the admin user here only if you want to change the password, or enable or disable the user.
      - To add admin user, provide a username as 'admin', select the admin user role, and then proceed.
    suboptions:
      username:
        description:
          - Name of the user created on the endpoint.
        required: true
      enable:
        description:
          - Enable or disable the user.
        type: bool
        default: true
      role:
        description:
          - Roles associated with the user on the endpoint.
        choices: [admin, readonly, user]
        required: true
      password:
        description:
          - Valid login password of the user.
        required: true
author:
  - David Soper (@dsoper2)
version_added: '2.10'
'''

EXAMPLES = r'''
- name: Configure Local User policy
  intersight_local_user_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: guest-admin
    tags:
      - Key: username
        Value: guest
    description: User named guest with admin role
    local_users:
      - username: guest
        role: admin
        password: vault_guest_password
      - username: reader
        role: readonly
        password: vault_reader_password

- name: Delete Local User policy
  intersight_local_user_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: guest-admin
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Description": "User named guest with admin role",
        "EndPointUserRoles": [
            {
                "ChangePassword": true,
                "Enabled": true,
                ...
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec, compare_values


def main():
    local_user = dict(
        username=dict(type='str', required=True),
        enable=dict(type='bool', default=True),
        role=dict(type='str', choices=['admin', 'readonly', 'user'], required=True),
        password=dict(type='str', required=True, no_log=True),
    )
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr'], default=''),
        tags=dict(type='list', default=[]),
        enforce_strong_password=dict(type='bool', default=True, no_log=False),
        enable_password_expiry=dict(type='bool', default=False, no_log=False),
        password_history=dict(type='int', default=5, no_log=False),
        local_users=dict(type='list', elements='dict', options=local_user, default=[]),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # get the current state of the resource
    intersight.get_resource(
        resource_path='/iam/EndPointUserPolicies',
        query_params={
            '$filter': "Name eq '" + intersight.module.params['name'] + "'",
            '$expand': 'EndPointUserRoles($expand=EndPointRole,EndPointUser)',
        },
    )

    user_policy_moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        user_policy_moid = intersight.result['api_response']['Moid']
        if module.params['state'] == 'present':
            # Create api body used to check current state
            end_point_user_roles = []
            for user in intersight.module.params['local_users']:
                end_point_user_roles.append(
                    {
                        'Enabled': user['enable'],
                        'EndPointRole': [
                            {
                                'Name': user['role'],
                                'Type': 'IMC',
                            },
                        ],
                        'EndPointUser': {
                            'Name': user['username'],
                        },
                    }
                )
            intersight.api_body = {
                'Name': intersight.module.params['name'],
                'Tags': intersight.module.params['tags'],
                'Description': intersight.module.params['description'],
                'PasswordProperties': {
                    'EnforceStrongPassword': intersight.module.params['enforce_strong_password'],
                    'EnablePasswordExpiry': intersight.module.params['enable_password_expiry'],
                    'PasswordHistory': intersight.module.params['password_history'],
                },
                'EndPointUserRoles': end_point_user_roles,
            }
            resource_values_match = compare_values(intersight.api_body, intersight.result['api_response'])
        else:  # state == 'absent'
            intersight.delete_resource(
                moid=user_policy_moid,
                resource_path='/iam/EndPointUserPolicies',
            )

    if module.params['state'] == 'present' and not resource_values_match:
        intersight.api_body = {
            'Name': intersight.module.params['name'],
            'Tags': intersight.module.params['tags'],
            'Description': intersight.module.params['description'],
            'PasswordProperties': {
                'EnforceStrongPassword': intersight.module.params['enforce_strong_password'],
                'EnablePasswordExpiry': intersight.module.params['enable_password_expiry'],
                'PasswordHistory': intersight.module.params['password_history'],
            },
        }
        intersight.configure_resource(
            moid=user_policy_moid,
            resource_path='/iam/EndPointUserPolicies',
            body=intersight.api_body,
            query_params={
                '$filter': "Name eq '" + intersight.module.params['name'] + "'",
            },
        )
        if intersight.result['api_response'].get('Moid'):
            # resource exists and moid was returned
            user_policy_moid = intersight.result['api_response']['Moid']
        # EndPointUser config
        for user in intersight.module.params['local_users']:
            intersight.api_body = {
                'Name': user['username'],
            }
            intersight.configure_resource(
                moid=None,
                resource_path='/iam/EndPointUsers',
                body=intersight.api_body,
                query_params={
                    '$filter': "Name eq '" + user['username'] + "'",
                },
            )
            user_moid = None
            if intersight.result['api_response'].get('Moid'):
                # resource exists and moid was returned
                user_moid = intersight.result['api_response']['Moid']
            # GET EndPointRole Moid
            intersight.get_resource(
                resource_path='/iam/EndPointRoles',
                query_params={
                    '$filter': "Name eq '" + user['role'] + "' and Type eq 'IMC'",
                },
            )
            end_point_role_moid = None
            if intersight.result['api_response'].get('Moid'):
                # resource exists and moid was returned
                end_point_role_moid = intersight.result['api_response']['Moid']
            # EndPointUserRole config
            intersight.api_body = {
                'EndPointUser': {
                    'Moid': user_moid,
                },
                'EndPointRole': [
                    {
                        'Moid': end_point_role_moid,
                    }
                ],
                'Password': user['password'],
                'Enabled': user['enable'],
                'EndPointUserPolicy': {
                    'Moid': user_policy_moid,
                },
            }
            intersight.configure_resource(
                moid=None,
                resource_path='/iam/EndPointUserRoles',
                body=intersight.api_body,
                query_params={
                    '$filter': "EndPointUserPolicy.Moid eq '" + user_policy_moid + "'",
                },
            )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()