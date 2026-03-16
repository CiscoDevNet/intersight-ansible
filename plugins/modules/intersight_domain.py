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
module: intersight_domain
short_description: Manage UCS Domain Profiles in Cisco Intersight
description:
  - Create, update, and delete UCS Domain Profiles (SwitchClusterProfiles) on Cisco Intersight.
  - Manages the associated SwitchProfiles (A and B), Fabric Interconnect assignments, and policy buckets.
  - Policies are attached to SwitchProfiles via the Intersight bulk API.
  - This module does not manage deployment of the domain profile.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/fabric/SwitchClusterProfiles/post/).
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
      - The name assigned to the UCS Domain Profile.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
      - SwitchProfiles are automatically named C({name}-A) and C({name}-B).
    type: str
    required: true
  description:
    description:
      - The user-defined description of the UCS Domain Profile.
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  assigned_switch_a:
    description:
      - The name of the Fabric Interconnect to assign to SwitchProfile A.
      - Resolved via the C(/network/ElementSummaries) API endpoint.
    type: str
  assigned_switch_b:
    description:
      - The name of the Fabric Interconnect to assign to SwitchProfile B.
      - Resolved via the C(/network/ElementSummaries) API endpoint.
    type: str
  vlan_policy_fi_a:
    description:
      - Name of the VLAN Policy to associate with Fabric Interconnect A.
    type: str
  vlan_policy_fi_b:
    description:
      - Name of the VLAN Policy to associate with Fabric Interconnect B.
    type: str
  vsan_policy_fi_a:
    description:
      - Name of the VSAN Policy to associate with Fabric Interconnect A.
    type: str
  vsan_policy_fi_b:
    description:
      - Name of the VSAN Policy to associate with Fabric Interconnect B.
    type: str
  port_policy_fi_a:
    description:
      - Name of the Port Policy to associate with Fabric Interconnect A.
    type: str
  port_policy_fi_b:
    description:
      - Name of the Port Policy to associate with Fabric Interconnect B.
    type: str
  ntp_policy:
    description:
      - Name of the NTP Policy to associate with both Fabric Interconnects.
    type: str
  syslog_policy:
    description:
      - Name of the Syslog Policy to associate with both Fabric Interconnects.
    type: str
  network_connectivity_policy:
    description:
      - Name of the Network Connectivity (DNS) Policy to associate with both Fabric Interconnects.
    type: str
  snmp_policy:
    description:
      - Name of the SNMP Policy to associate with both Fabric Interconnects.
    type: str
  ldap_policy:
    description:
      - Name of the LDAP Policy to associate with both Fabric Interconnects.
    type: str
  certificate_management_policy:
    description:
      - Name of the Certificate Management Policy to associate with both Fabric Interconnects.
    type: str
  system_qos_policy:
    description:
      - Name of the System QoS Policy to associate with both Fabric Interconnects.
      - This policy is mandatory for UCS Domain Profiles.
    type: str
  auditd_policy:
    description:
      - Name of the Audit Log Policy to associate with both Fabric Interconnects.
    type: str
  switch_control_policy:
    description:
      - Name of the Switch Control Policy to associate with both Fabric Interconnects.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a basic UCS Domain Profile
  cisco.intersight.intersight_domain:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "Domain-01"
    description: "Basic domain profile"
    system_qos_policy: "Default-QoS"
    state: present

- name: Create a UCS Domain Profile with switch assignments and policies
  cisco.intersight.intersight_domain:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "Domain-01"
    description: "Full domain profile"
    assigned_switch_a: "DOMAIN FI-A"
    assigned_switch_b: "DOMAIN FI-B"
    vlan_policy_fi_a: "VLAN-Policy-A"
    vlan_policy_fi_b: "VLAN-Policy-B"
    vsan_policy_fi_a: "VSAN-Policy-A"
    vsan_policy_fi_b: "VSAN-Policy-B"
    port_policy_fi_a: "Port-Policy-A"
    port_policy_fi_b: "Port-Policy-B"
    ntp_policy: "NTP-Corp"
    syslog_policy: "Syslog-Corp"
    snmp_policy: "SNMP-Monitor"
    system_qos_policy: "QoS-Default"
    switch_control_policy: "Switch-Control"
    state: present

- name: Delete a UCS Domain Profile
  cisco.intersight.intersight_domain:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "Domain-01"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the SwitchClusterProfile resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "Domain-01",
        "ObjectType": "fabric.SwitchClusterProfile",
        "Organization": {
            "Moid": "675450ee69726530014753e2",
            "ObjectType": "organization.Organization"
        },
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

PER_FI_A_POLICY_MAPPING = {
    'vlan_policy_fi_a': {'resource_path': '/fabric/EthNetworkPolicies', 'object_type': 'fabric.EthNetworkPolicy'},
    'vsan_policy_fi_a': {'resource_path': '/fabric/FcNetworkPolicies', 'object_type': 'fabric.FcNetworkPolicy'},
    'port_policy_fi_a': {'resource_path': '/fabric/PortPolicies', 'object_type': 'fabric.PortPolicy'},
}

PER_FI_B_POLICY_MAPPING = {
    'vlan_policy_fi_b': {'resource_path': '/fabric/EthNetworkPolicies', 'object_type': 'fabric.EthNetworkPolicy'},
    'vsan_policy_fi_b': {'resource_path': '/fabric/FcNetworkPolicies', 'object_type': 'fabric.FcNetworkPolicy'},
    'port_policy_fi_b': {'resource_path': '/fabric/PortPolicies', 'object_type': 'fabric.PortPolicy'},
}

SHARED_POLICY_MAPPING = {
    'system_qos_policy': {'resource_path': '/fabric/SystemQosPolicies', 'object_type': 'fabric.SystemQosPolicy'},
    'ntp_policy': {'resource_path': '/ntp/Policies', 'object_type': 'ntp.Policy'},
    'syslog_policy': {'resource_path': '/syslog/Policies', 'object_type': 'syslog.Policy'},
    'network_connectivity_policy': {'resource_path': '/networkconfig/Policies', 'object_type': 'networkconfig.Policy'},
    'snmp_policy': {'resource_path': '/snmp/Policies', 'object_type': 'snmp.Policy'},
    'ldap_policy': {'resource_path': '/iam/LdapPolicies', 'object_type': 'iam.LdapPolicy'},
    'certificate_management_policy': {'resource_path': '/certificatemanagement/Policies', 'object_type': 'certificatemanagement.Policy'},
    'auditd_policy': {'resource_path': '/auditd/Policies', 'object_type': 'auditd.Policy'},
    'switch_control_policy': {'resource_path': '/fabric/SwitchControlPolicies', 'object_type': 'fabric.SwitchControlPolicy'},
}


def resolve_switch_moid(intersight, switch_name):
    """Resolve a Fabric Interconnect name to its MOID via /network/ElementSummaries."""
    moid = intersight.get_moid_by_name(
        resource_path='/network/ElementSummaries',
        resource_name=switch_name,
    )
    if not moid:
        intersight.get_resource(
            resource_path='/network/ElementSummaries',
            query_params={'$select': 'Name,SwitchId'},
            return_list=True,
        )
        elements = intersight.result['api_response']
        if not isinstance(elements, list):
            elements = [elements] if elements else []
        intersight.module.fail_json(
            msg=f"Fabric Interconnect '{switch_name}' not found. "
        )
    return moid


def ensure_switch_profile(intersight, domain_name, switch_id, cluster_moid):
    """Ensure a SwitchProfile exists for the given switch ID, return its MOID."""
    profile_name = f"{domain_name}-{switch_id}"
    filter_str = (
        f"Name eq '{profile_name}'"
        f" and SwitchClusterProfile.Moid eq '{cluster_moid}'"
    )

    intersight.get_resource(
        resource_path='/fabric/SwitchProfiles',
        query_params={'$filter': filter_str},
    )

    if intersight.result['api_response'].get('Moid'):
        return intersight.result['api_response']['Moid']

    body = {
        'Name': profile_name,
        'SwitchId': switch_id,
        'SwitchClusterProfile': {'Moid': cluster_moid},
    }
    intersight.configure_resource(
        moid=None,
        resource_path='/fabric/SwitchProfiles',
        body=body,
        query_params={'$filter': filter_str},
    )
    return intersight.result['api_response'].get('Moid')


def configure_switch_profiles(intersight, domain_name, cluster_moid):
    """Create SwitchProfiles A/B and assign Fabric Interconnects if provided.

    Returns a list of (profile_moid, profile_state) tuples for each FI.
    """
    fi_configs = [
        {'switch_id': 'A', 'switch_param': 'assigned_switch_a'},
        {'switch_id': 'B', 'switch_param': 'assigned_switch_b'},
    ]

    profile_results = []
    for fi in fi_configs:
        profile_moid = ensure_switch_profile(intersight, domain_name, fi['switch_id'], cluster_moid)
        profile_state = dict(intersight.result['api_response'])

        switch_name = intersight.module.params.get(fi['switch_param'])
        if switch_name and profile_moid:
            switch_moid = resolve_switch_moid(intersight, switch_name)
            current_switch = (profile_state.get('AssignedSwitch') or {}).get('Moid')
            if current_switch != switch_moid:
                intersight.configure_resource(
                    moid=profile_moid,
                    resource_path='/fabric/SwitchProfiles',
                    body={'AssignedSwitch': {'Moid': switch_moid}},
                    query_params={},
                )

        profile_results.append((profile_moid, profile_state))

    return profile_results


def build_policy_sync_data(intersight, organization, profile_results):
    """Resolve desired vs current PolicyBuckets for each SwitchProfile.

    Returns a list of (profile_moid, desired_bucket, current_bucket) tuples
    ready for sync_domain_policy_buckets.
    """
    per_fi_mappings = [PER_FI_A_POLICY_MAPPING, PER_FI_B_POLICY_MAPPING]
    shared_bucket = resolve_policy_bucket(intersight, organization, SHARED_POLICY_MAPPING)

    profiles_to_sync = []
    for (profile_moid, profile_state), per_fi_mapping in zip(profile_results, per_fi_mappings):
        if not profile_moid:
            continue
        desired_bucket = resolve_policy_bucket(intersight, organization, per_fi_mapping) + shared_bucket
        current_bucket = profile_state.get('PolicyBucket') or []
        profiles_to_sync.append((profile_moid, desired_bucket, current_bucket))

    return profiles_to_sync


def unassign_switches_before_delete(intersight, cluster_moid):
    """Unassign switches from SwitchProfiles before deleting the domain.

    The Intersight API may prevent deletion of a domain profile while
    switches are assigned to its SwitchProfiles.
    """
    intersight.get_resource(
        resource_path='/fabric/SwitchProfiles',
        query_params={
            '$filter': f"SwitchClusterProfile.Moid eq '{cluster_moid}'"
        },
        return_list=True,
    )

    profiles = intersight.result['api_response']
    if not isinstance(profiles, list):
        profiles = [profiles] if profiles else []

    for profile in profiles:
        if not profile.get('Moid'):
            continue
        assigned = profile.get('AssignedSwitch')
        if assigned and assigned.get('Moid'):
            intersight.configure_resource(
                moid=profile['Moid'],
                resource_path='/fabric/SwitchProfiles',
                body={'AssignedSwitch': None},
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
        assigned_switch_a=dict(type='str'),
        assigned_switch_b=dict(type='str'),
        vlan_policy_fi_a=dict(type='str'),
        vlan_policy_fi_b=dict(type='str'),
        vsan_policy_fi_a=dict(type='str'),
        vsan_policy_fi_b=dict(type='str'),
        port_policy_fi_a=dict(type='str'),
        port_policy_fi_b=dict(type='str'),
        ntp_policy=dict(type='str'),
        syslog_policy=dict(type='str'),
        network_connectivity_policy=dict(type='str'),
        snmp_policy=dict(type='str'),
        ldap_policy=dict(type='str'),
        certificate_management_policy=dict(type='str'),
        system_qos_policy=dict(type='str'),
        auditd_policy=dict(type='str'),
        switch_control_policy=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'present', ['system_qos_policy']],
        ],
        required_together=[
            ['assigned_switch_a', 'assigned_switch_b'],
        ],
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    cluster_path = '/fabric/SwitchClusterProfiles'
    name = intersight.module.params['name']
    organization = intersight.module.params['organization']
    state = intersight.module.params['state']

    intersight.api_body = {
        'Organization': {'Name': organization},
        'Name': name,
        'TargetPlatform': 'UCS Domain',
    }

    if state == 'present':
        intersight.set_tags_and_description()

    if state == 'absent':
        organization_moid = intersight.get_moid_by_name(
            resource_path='/organization/Organizations',
            resource_name=organization,
        )
        if organization_moid:
            filter_str = (
                f"Name eq '{name}'"
                f" and Organization.Moid eq '{organization_moid}'"
            )
            intersight.get_resource(
                resource_path=cluster_path,
                query_params={'$filter': filter_str},
            )
            cluster_moid = intersight.result['api_response'].get('Moid')
            if cluster_moid:
                unassign_switches_before_delete(intersight, cluster_moid)

    cluster_moid = intersight.configure_policy_or_profile(resource_path=cluster_path)
    cluster_response = dict(intersight.result['api_response']) if intersight.result['api_response'] else {}

    if cluster_moid and state == 'present':
        profile_results = configure_switch_profiles(intersight, name, cluster_moid)
        profiles_to_sync = build_policy_sync_data(intersight, organization, profile_results)
        for profile_moid, desired_bucket, current_bucket in profiles_to_sync:
            bucket_path = f'/fabric/SwitchProfiles/{profile_moid}/PolicyBucket'
            sync_policy_bucket(intersight, bucket_path, desired_bucket, current_bucket)

    if cluster_response:
        intersight.result['api_response'] = cluster_response

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
