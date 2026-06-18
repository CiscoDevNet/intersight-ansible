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
      - The name assigned to the Local User Policy.
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
      - The user-defined description of the Local User policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
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
    type: list
    elements: dict
    suboptions:
      username:
        description:
          - Name of the user created on the endpoint.
          - Cisco Intersight currently limits endpoint usernames to 16 characters.
        type: str
        required: true
      enable:
        description:
          - Enable or disable the user.
        type: bool
        default: true
      role:
        description:
          - Roles associated with the user on the endpoint.
        type: str
        choices: [admin, readonly, user]
        required: true
      password:
        description:
          - Valid login password of the user.
        type: str
        required: true
      endpoint_role_type:
        description:
          - The type of endpoint role to assign to the user.
          - IMC is the supported server management role type for local user roles.
          - IPMI access should be expressed through C(account_types) such as C(IPMI).
          - Supplying C(IPMI) here is rejected by the Intersight API for C(iam.EndPointUserRole).
        type: str
        choices: [IMC, IPMI]
        default: IMC
      account_types:
        description:
          - List of account types to assign to the user.
          - Supported values are C(IPMI) and C(Local).
          - For backward compatibility, dictionary entries with C(ObjectType) are still accepted.
          - When provided, the module maps these values to the corresponding Intersight API object types and does not set any separate
          - account-type toggle field.
          - Use this to request IPMI or combined local plus IPMI account access while keeping the endpoint role type at C(IMC).
        type: list
        elements: raw
  purge:
    description:
      - The purge argument instructs the module to consider the resource definition absolute.
      - If true, any previously configured usernames will be removed from the policy with the exception of the `admin` user which cannot be deleted.
    type: bool
    default: false
  always_update_password:
    description:
      - Since passwords are not returned by the API and are encrypted on the endpoint, this option will instruct the module when to change the password.
      - If true, the password for each user will always be updated in the policy.
      - If false, the password will be updated only if the user is created.
    type: bool
    default: false
author:
  - David Soper (@dsoper2)
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

- name: Configure Local User policy with IPMI user
  intersight_local_user_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: ipmi-admin
    description: User with IPMI account type
    local_users:
      - username: ipmi-user
        role: admin
        password: vault_ipmi_password
        account_types:
          - IPMI

- name: Configure Local User policy with local and IPMI access
  intersight_local_user_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: local-ipmi-admin
    description: User with local and IPMI account types
    local_users:
      - username: local-ipmi
        role: admin
        password: vault_local_ipmi_password
        account_types:
          - Local
          - IPMI

- name: Delete Local User policy
  intersight_local_user_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: guest-admin
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Description": "User named guest with admin role",
        "EndPointUserRoles": [
            {
                "ChangePassword": true,
                "Enabled": true
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec, compare_values


ACCOUNT_TYPE_MAP = {
    'IPMI': 'iam.AccountTypeIpmi',
    'LOCAL': 'iam.AccountTypeLocal',
}


def normalize_account_types(module, account_types):
    normalized_account_types = []

    for account_type in account_types:
        if isinstance(account_type, str):
            object_type = ACCOUNT_TYPE_MAP.get(account_type.upper())
            if not object_type:
                module.fail_json(
                    msg=(
                        "Unsupported account_type '{0}'. Supported values are: {1}."
                    ).format(account_type, ', '.join(sorted(ACCOUNT_TYPE_MAP.keys())))
                )
            normalized_account_types.append({
                'ObjectType': object_type,
                'ClassId': object_type,
            })
        elif isinstance(account_type, dict):
            account_type_ref = account_type.copy()
            object_type = account_type_ref.get('ObjectType')
            if not object_type:
                module.fail_json(msg="account_types dict entries must include ObjectType.")
            if 'ClassId' not in account_type_ref:
                account_type_ref['ClassId'] = object_type
            normalized_account_types.append(account_type_ref)
        else:
            module.fail_json(msg="account_types entries must be strings like IPMI or Local.")

    return normalized_account_types


def main():
    local_user = dict(
        username=dict(type='str', required=True),
        enable=dict(type='bool', default=True),
        role=dict(type='str', choices=['admin', 'readonly', 'user'], required=True),
        password=dict(type='str', required=True, no_log=True),
        endpoint_role_type=dict(type='str', choices=['IMC', 'IPMI'], default='IMC'),
        account_types=dict(type='list', elements='raw'),
    )
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        enforce_strong_password=dict(type='bool', default=True, no_log=False),
        enable_password_expiry=dict(type='bool', default=False, no_log=False),
        password_history=dict(type='int', default=5, no_log=False),
        local_users=dict(type='list', elements='dict', options=local_user),
        purge=dict(type='bool', default=False),
        always_update_password=dict(type='bool', default=False, no_log=False),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    organization_moid = None
    # get Organization Moid
    intersight.get_resource(
        resource_path='/organization/Organizations',
        query_params={
            '$filter': "Name eq '" + intersight.module.params['organization'] + "'",
            '$select': 'Moid',
        },
    )
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        organization_moid = intersight.result['api_response']['Moid']
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # get the current state of the resource
    filter_str = "Name eq '" + intersight.module.params['name'] + "'"
    filter_str += "and Organization.Moid eq '" + organization_moid + "'"
    intersight.get_resource(
        resource_path='/iam/EndPointUserPolicies',
        query_params={
            '$filter': filter_str,
            '$expand': 'EndPointUserRoles($expand=EndPointRole,EndPointUser),Organization',
        },
    )

    if module.params['state'] == 'present':
        intersight.api_body = {
            'Name': intersight.module.params['name'],
            'PasswordProperties': {
                'EnforceStrongPassword': intersight.module.params['enforce_strong_password'],
                'EnablePasswordExpiry': intersight.module.params['enable_password_expiry'],
                'PasswordHistory': intersight.module.params['password_history'],
            },
        }
        intersight.set_tags_and_description()

    user_policy_moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        user_policy_moid = intersight.result['api_response']['Moid']
        #
        # always_update_password
        #   false: compare expected vs. actual (won't check passwords)
        #   true: no compare
        #
        if module.params['state'] == 'present' and not module.params['always_update_password']:
            # Create api body used to check current state
            end_point_user_roles = []
            for user in intersight.module.params['local_users']:
                end_point_user_roles.append(
                    {
                        'Enabled': user['enable'],
                        'EndPointRole': [
                            {
                                'Name': user['role'],
                                'Type': user.get('endpoint_role_type', 'IMC'),
                            },
                        ],
                        'EndPointUser': {
                            'Name': user['username'],
                        },
                    }
                )
            intersight.api_body['EndPointUserRoles'] = end_point_user_roles
            intersight.api_body['Organization'] = {
                'Name': intersight.module.params['organization'],
            }
            resource_values_match = compare_values(intersight.api_body, intersight.result['api_response'])
        elif module.params['state'] == 'absent':
            intersight.delete_resource(
                moid=user_policy_moid,
                resource_path='/iam/EndPointUserPolicies',
            )
            user_policy_moid = None

    if module.params['state'] == 'present' and not resource_values_match:
        intersight.api_body['Organization'] = {
            'Moid': organization_moid,
        }

        if module.params['purge']:
            # update existing resource and purge any existing users
            if intersight.result['api_response'].get('EndPointUserRoles'):
                for end_point_user_role in intersight.result['api_response']['EndPointUserRoles']:
                    intersight.delete_resource(
                        moid=end_point_user_role['Moid'],
                        resource_path='/iam/EndPointUserRoles',
                    )
        # configure the top-level policy resource
        intersight.result['api_response'] = {}
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

            # EndPointUser local_users list config
            for user in intersight.module.params['local_users']:
                try:
                    if user.get('endpoint_role_type') == 'IPMI':
                        module.fail_json(
                            msg=(
                                "local_users endpoint_role_type=IPMI is not accepted by the Intersight "
                                "iam.EndPointUserRole API. Leave endpoint_role_type at IMC and use "
                                "account_types such as IPMI instead."
                            )
                        )
                    intersight.result['api_response'] = {}
                    # check for existing user in this organization
                    filter_str = "Name eq '" + user['username'] + "'"
                    filter_str += " and Organization.Moid eq '" + organization_moid + "'"
                    intersight.get_resource(
                        resource_path='/iam/EndPointUsers',
                        query_params={
                            '$filter': filter_str
                        },
                    )
                    user_moid = None
                    if intersight.result['api_response'].get('Moid'):
                        # resource exists and moid was returned
                        user_moid = intersight.result['api_response']['Moid']
                    else:
                        # create user if it doesn't exist
                        intersight.api_body = {
                            'Name': user['username'],
                        }
                        if organization_moid:
                            intersight.api_body['Organization'] = {
                                'Moid': organization_moid,
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
                            '$filter': "Name eq '" + user['role'] + "' and Type eq '" + user.get('endpoint_role_type', 'IMC') + "'",
                        },
                    )
                    end_point_role_moid = None
                    if intersight.result['api_response'].get('Moid'):
                        # resource exists and moid was returned
                        end_point_role_moid = intersight.result['api_response']['Moid']
                    # Check for any existing EndPointUserRole objects for this policy, then
                    # match by expanded username. Filtering on nested user Moid is not
                    # reliable for this endpoint.
                    filter_str = "EndPointUserPolicy.Moid eq '" + user_policy_moid + "'"
                    intersight.get_resource(
                        resource_path='/iam/EndPointUserRoles',
                        query_params={
                            '$filter': filter_str,
                            '$expand': 'EndPointRole,EndPointUser,EndPointUserPolicy',
                        },
                        return_list=True,
                    )
                    existing_user_roles = intersight.result['api_response']
                    if not isinstance(existing_user_roles, list):
                        existing_user_roles = []

                    # EndPointRole relationships are effectively immutable here, so replace any
                    # existing role for this username before creating the desired one.
                    for existing_user_role in existing_user_roles:
                        existing_user = existing_user_role.get('EndPointUser', {})
                        if existing_user.get('Name') == user['username']:
                            intersight.delete_resource(
                                moid=existing_user_role['Moid'],
                                resource_path='/iam/EndPointUserRoles',
                            )

                    # Create a new EndPointUserRole with the required relationships.
                    intersight.api_body = {
                        'EndPointUser': {
                            'Moid': user_moid,
                            'ObjectType': 'iam.EndPointUser',
                        },
                        'EndPointRole': [
                            {
                                'Moid': end_point_role_moid,
                                'ObjectType': 'iam.EndPointRole',
                            }
                        ],
                        'Password': user['password'],
                        'Enabled': user['enable'],
                        'EndPointUserPolicy': {
                            'Moid': user_policy_moid,
                            'ObjectType': 'iam.EndPointUserPolicy',
                        },
                    }
                    if user.get('account_types'):
                        intersight.api_body['AccountTypes'] = normalize_account_types(module, user['account_types'])
                    intersight.configure_resource(
                        moid=None,
                        resource_path='/iam/EndPointUserRoles',
                        body=intersight.api_body,
                        query_params={
                            '$filter': filter_str,
                        },
                    )
                except Exception as exc:
                    module.fail_json(msg="Failed configuring local user '{0}': {1}".format(user['username'], exc))

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
