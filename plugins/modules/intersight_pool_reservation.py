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
module: intersight_pool_reservation
short_description: Manage pool identifier reservations in Cisco Intersight
description:
  - Reserve and release identifiers (IP, UUID, MAC, IQN, WWNN, WWPN) from Intersight pools.
  - Handles the Intersight reservation API's one-time-use constraint by performing a pre-flight
    check before attempting to reserve, ensuring idempotent playbook runs.
  - Reserved identifiers are consumed when a policy using them is attached to a server profile
    or when the server profile is deployed.
  - Reservation of identifiers is only supported for Fabric Interconnect-attached servers.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  pool_type:
    description:
      - The type of pool to manage reservations for.
    type: str
    required: true
    choices: [ip, uuid, mac, iqn, wwnn, wwpn]
  pool_name:
    description:
      - Name of the pool to reserve from.
    type: str
    required: true
  organization:
    description:
      - The name of the Organization the pool belongs to.
    type: str
    default: default
  identity:
    description:
      - The specific identifier value to reserve (e.g., an IP address, UUID, MAC address, IQN).
      - Required when C(state) is C(present).
    type: str
  state:
    description:
      - If C(present), will reserve the identifier in the pool.
      - If C(absent), will release the reservation.
    type: str
    choices: [present, absent]
    default: present
  allocation_type:
    description:
      - Whether the reservation is C(static) (specific value) or C(dynamic) (next available from pool).
      - When C(static), C(identity) is required.
      - When C(dynamic), the pool assigns the next available identifier.
    type: str
    choices: [static, dynamic]
    default: static
author:
  - Steve Fulmer (@stevefulme1)
'''

EXAMPLES = r'''
- name: Reserve a specific IP address from a pool
  cisco.intersight.intersight_pool_reservation:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    pool_type: ip
    pool_name: IP-Pool-01
    identity: "10.10.10.100"

- name: Reserve a specific UUID from a pool
  cisco.intersight.intersight_pool_reservation:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    pool_type: uuid
    pool_name: UUID-Pool-01
    identity: "550e8400-e29b-41d4-a716-446655440000"

- name: Reserve a MAC address
  cisco.intersight.intersight_pool_reservation:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    pool_type: mac
    pool_name: MAC-Pool-01
    identity: "00:25:B5:00:00:01"

- name: Release a reservation
  cisco.intersight.intersight_pool_reservation:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    pool_type: ip
    pool_name: IP-Pool-01
    identity: "10.10.10.100"
    state: absent

- name: Reserve next available IP (dynamic)
  cisco.intersight.intersight_pool_reservation:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    pool_type: ip
    pool_name: IP-Pool-01
    allocation_type: dynamic

- name: Reserve an IQN from a pool
  cisco.intersight.intersight_pool_reservation:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    pool_type: iqn
    pool_name: IQN-Pool-01
    identity: "iqn.2010-11.com.flexpod:storage:component:server01"
'''

RETURN = r'''
api_response:
  description: The API response from the reservation operation.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Identity": "10.10.10.100",
        "Moid": "63a1b2c3d4e5f6a7b8c9d0e1",
        "AllocationType": "static"
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


POOL_TYPE_MAP = {
    'ip': {
        'resource_path': '/ippool/Reservations',
        'pool_path': '/ippool/Pools',
        'identity_key': 'Identity',
        'object_type': 'ippool.Reservation',
    },
    'uuid': {
        'resource_path': '/uuidpool/Reservations',
        'pool_path': '/uuidpool/Pools',
        'identity_key': 'Identity',
        'object_type': 'uuidpool.Reservation',
    },
    'mac': {
        'resource_path': '/macpool/Reservations',
        'pool_path': '/macpool/Pools',
        'identity_key': 'Identity',
        'object_type': 'macpool.Reservation',
    },
    'wwnn': {
        'resource_path': '/fcpool/Reservations',
        'pool_path': '/fcpool/Pools',
        'identity_key': 'Identity',
        'object_type': 'fcpool.Reservation',
    },
    'iqn': {
        'resource_path': '/iqnpool/Reservations',
        'pool_path': '/iqnpool/Pools',
        'identity_key': 'Identity',
        'object_type': 'iqnpool.Reservation',
    },
    'wwpn': {
        'resource_path': '/fcpool/Reservations',
        'pool_path': '/fcpool/Pools',
        'identity_key': 'Identity',
        'object_type': 'fcpool.Reservation',
    },
}


def get_pool_moid(intersight, pool_path, pool_name, organization_moid):
    """Look up a pool by name and org."""
    options = {
        'http_method': 'get',
        'resource_path': pool_path,
        'query_params': {
            '$filter': "Name eq '" + pool_name + "' and Organization.Moid eq '" + organization_moid + "'",
        },
    }
    response = intersight.call_api(**options)
    if response.get('Results'):
        return response['Results'][0]['Moid']
    return None


def get_existing_reservation(intersight, resource_path, pool_moid, identity, organization_moid):
    """Check if a reservation already exists for this identity or pool."""
    filter_str = "Organization.Moid eq '" + organization_moid + "'"
    if identity:
        filter_str += " and Identity eq '" + identity + "'"
    else:
        filter_str += " and Pool.Moid eq '" + pool_moid + "'"
    options = {
        'http_method': 'get',
        'resource_path': resource_path,
        'query_params': {
            '$filter': filter_str,
        },
    }
    response = intersight.call_api(**options)
    if response.get('Results'):
        return response['Results'][0]
    return None


def create_reservation(intersight, resource_path, pool_moid, organization_moid, identity, allocation_type, object_type, pool_type):
    """Create a new reservation."""
    body = {
        'ObjectType': object_type,
        'AllocationType': allocation_type,
        'Organization': {
            'Moid': organization_moid,
            'ObjectType': 'organization.Organization',
        },
    }
    if allocation_type == 'dynamic':
        body['Pool'] = {
            'Moid': pool_moid,
            'ObjectType': POOL_TYPE_MAP[pool_type]['object_type'].replace('Reservation', 'Pool'),
        }
    if identity and allocation_type == 'static':
        body['Identity'] = identity

    if pool_type == 'wwnn':
        body['IdPurpose'] = 'WWNN'
    elif pool_type == 'wwpn':
        body['IdPurpose'] = 'WWPN'

    options = {
        'http_method': 'post',
        'resource_path': resource_path,
        'body': body,
    }
    return intersight.call_api(**options)


def delete_reservation(intersight, resource_path, reservation_moid):
    """Delete a reservation."""
    options = {
        'http_method': 'delete',
        'resource_path': resource_path,
        'moid': reservation_moid,
    }
    return intersight.call_api(**options)


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        pool_type=dict(type='str', required=True, choices=['ip', 'uuid', 'mac', 'iqn', 'wwnn', 'wwpn']),
        pool_name=dict(type='str', required=True),
        organization=dict(type='str', default='default'),
        identity=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        allocation_type=dict(type='str', choices=['static', 'dynamic'], default='static'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ['allocation_type', 'static', ['identity']],
            ['state', 'absent', ['identity']],
        ],
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    pool_type = module.params['pool_type']
    pool_name = module.params['pool_name']
    organization_name = module.params['organization']
    identity = module.params['identity']
    state = module.params['state']
    allocation_type = module.params['allocation_type']

    pool_config = POOL_TYPE_MAP[pool_type]

    organization_moid = intersight.get_moid_by_name(
        resource_path='/organization/Organizations',
        resource_name=organization_name,
    )
    if not organization_moid:
        module.fail_json(msg="Organization '%s' not found." % organization_name)

    pool_moid = get_pool_moid(intersight, pool_config['pool_path'], pool_name, organization_moid)
    if not pool_moid:
        module.fail_json(msg="%s pool '%s' not found in organization '%s'." % (pool_type.upper(), pool_name, organization_name))

    existing = None
    if identity:
        existing = get_existing_reservation(intersight, pool_config['resource_path'], pool_moid, identity, organization_moid)

    if state == 'present':
        if existing:
            intersight.result['api_response'] = existing
            module.exit_json(**intersight.result)

        if module.check_mode:
            intersight.result['changed'] = True
            module.exit_json(**intersight.result)

        response = create_reservation(
            intersight,
            pool_config['resource_path'],
            pool_moid,
            organization_moid,
            identity,
            allocation_type,
            pool_config['object_type'],
            pool_type,
        )
        intersight.result['changed'] = True
        intersight.result['api_response'] = response

    elif state == 'absent':
        if not existing:
            module.exit_json(**intersight.result)

        if module.check_mode:
            intersight.result['changed'] = True
            module.exit_json(**intersight.result)

        delete_reservation(intersight, pool_config['resource_path'], existing['Moid'])
        intersight.result['changed'] = True

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
