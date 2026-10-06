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
  - Supports deployment of both associated SwitchProfiles, with optional waiting for completion.
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
      - The name must be between 1 and 64 alphanumeric characters, allowing special characters :-_.
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
  action:
    description:
      - Deploy both SwitchProfiles after configuration.
      - With no configuration options, deploy an existing domain without modifying its policies or assignments.
      - Already associated SwitchProfiles are skipped unless configuration changed.
      - Check mode reports whether deployment is needed without submitting or waiting for an action.
    type: str
    choices: [Deploy]
  wait_for_action:
    description:
      - Wait for deployment of both SwitchProfiles to complete.
    type: bool
    default: true
  action_timeout:
    description:
      - Maximum seconds to wait for each SwitchProfile deployment.
    type: int
    default: 1200
  action_poll_interval:
    description:
      - Seconds between deployment status polls.
    type: int
    default: 60
  assigned_switch_a_serial:
    description:
      - The serial number of the Fabric Interconnect to assign to SwitchProfile A.
      - Resolved via the C(/network/ElementSummaries) API endpoint using the C(Serial) field.
    type: str
  assigned_switch_b_serial:
    description:
      - The serial number of the Fabric Interconnect to assign to SwitchProfile B.
      - Resolved via the C(/network/ElementSummaries) API endpoint using the C(Serial) field.
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
      - Required when creating or configuring a domain; optional for deployment of an existing domain.
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
    assigned_switch_a_serial: "FDO23456ABC"
    assigned_switch_b_serial: "FDO23456DEF"
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

- name: Preview deployment of an existing UCS Domain Profile
  cisco.intersight.intersight_domain:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "Domain-01"
    action: Deploy
  check_mode: true

- name: Delete a UCS Domain Profile
  cisco.intersight.intersight_domain:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "Domain-01"
    state: absent
'''

RETURN = r'''
switch_profiles:
  description: Current or final A/B SwitchProfile responses when deployment is requested.
  returned: when action is Deploy
  type: list
  elements: dict
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


import time

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


def resolve_switch_moid_by_serial(intersight, serial):
    """Resolve a Fabric Interconnect serial number to its MOID via /network/ElementSummaries."""
    intersight.get_resource(
        resource_path='/network/ElementSummaries',
        query_params={
            '$filter': f"Serial eq '{serial}'",
            '$select': 'Moid',
        },
    )
    moid = intersight.result['api_response'].get('Moid')
    if not moid:
        intersight.module.fail_json(
            msg=f"Fabric Interconnect with serial '{serial}' not found."
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
        {'switch_id': 'A', 'switch_param': 'assigned_switch_a_serial'},
        {'switch_id': 'B', 'switch_param': 'assigned_switch_b_serial'},
    ]

    profile_results = []
    for fi in fi_configs:
        profile_moid = ensure_switch_profile(intersight, domain_name, fi['switch_id'], cluster_moid)
        profile_state = dict(intersight.result['api_response'])

        switch_serial = intersight.module.params.get(fi['switch_param'])
        if switch_serial and profile_moid:
            switch_moid = resolve_switch_moid_by_serial(intersight, switch_serial)
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


def wait_for_switch_deployment(intersight, profile_moid, timeout, poll_interval):
    """Wait for one SwitchProfile to finish deploying, preserving failure details."""
    deadline = time.monotonic() + timeout
    while True:
        profile = intersight.call_api(
            http_method='get', resource_path='/fabric/SwitchProfiles', moid=profile_moid,
        )
        context = profile.get('ConfigContext') or {}
        if context.get('OperState') == 'Failed' or context.get('ConfigState') == 'Failed':
            intersight.module.fail_json(
                msg="SwitchProfile '%s' deployment failed." % profile.get('Name', profile_moid),
                api_response=profile,
            )
        if context.get('ControlAction') in ('No-op', 'No_op', '', None) and context.get('ConfigState') == 'Associated':
            return profile
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            intersight.module.fail_json(
                msg="Timed out waiting for SwitchProfile '%s' deployment after %d seconds." % (profile_moid, timeout),
                api_response=profile,
            )
        time.sleep(min(poll_interval, remaining))


def deploy_domain_profile(intersight, cluster_moid, configuration_changed=False):
    """Deploy the actual A/B SwitchProfiles belonging to the selected domain."""
    response = intersight.call_api(
        http_method='get', resource_path='/fabric/SwitchProfiles',
        query_params={'$filter': "SwitchClusterProfile.Moid eq '%s'" % cluster_moid},
    )
    profiles = response.get('Results') or []
    if len(profiles) != 2 or {p.get('SwitchId') for p in profiles} != {'A', 'B'}:
        intersight.module.fail_json(msg='Deployment requires both A and B SwitchProfiles.', api_response=response)
    # Validate both assignments before submitting either action.
    for profile in profiles:
        if not (profile.get('AssignedSwitch') or {}).get('Moid'):
            intersight.module.fail_json(msg="SwitchProfile '%s' has no assigned Fabric Interconnect." % profile['Name'])

    wait = intersight.module.params['wait_for_action']
    timeout = intersight.module.params['action_timeout']
    interval = intersight.module.params['action_poll_interval']
    deployed_profiles = []
    for profile in profiles:
        context = profile.get('ConfigContext') or {}
        active_action = context.get('ControlAction') not in ('No-op', 'No_op', '', None)
        needed = configuration_changed or context.get('ConfigState') != 'Associated' or active_action
        if needed and intersight.module.check_mode:
            intersight.result['changed'] = True
        elif active_action:
            if context.get('ControlAction') != 'Deploy':
                intersight.module.fail_json(
                    msg="SwitchProfile '%s' already has action '%s' in progress." % (profile['Name'], context['ControlAction']),
                    api_response=profile,
                )
            if wait:
                profile = wait_for_switch_deployment(intersight, profile['Moid'], timeout, interval)
        elif needed:
            result = intersight.call_api(
                http_method='patch', resource_path='/fabric/SwitchProfiles',
                moid=profile['Moid'], body={'Action': 'Deploy'},
            )
            intersight.result['changed'] = True
            if wait:
                profile = wait_for_switch_deployment(intersight, profile['Moid'], timeout, interval)
            elif result:
                profile = result
        deployed_profiles.append(profile)
    intersight.result['switch_profiles'] = deployed_profiles


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        action=dict(type='str', choices=['Deploy']),
        wait_for_action=dict(type='bool', default=True),
        action_timeout=dict(type='int', default=1200),
        action_poll_interval=dict(type='int', default=60),
        assigned_switch_a_serial=dict(type='str'),
        assigned_switch_b_serial=dict(type='str'),
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
        required_together=[
            ['assigned_switch_a_serial', 'assigned_switch_b_serial'],
        ],
    )

    configuration_options = (
        list(PER_FI_A_POLICY_MAPPING) + list(PER_FI_B_POLICY_MAPPING) + list(SHARED_POLICY_MAPPING)
        + ['assigned_switch_a_serial', 'assigned_switch_b_serial', 'description', 'tags']
    )
    deploy_only = module.params['action'] == 'Deploy' and not any(
        module.params.get(option) is not None for option in configuration_options
    )
    if module.params['action'] and module.params['state'] != 'present':
        module.fail_json(msg='action requires state=present.')
    if module.params['state'] == 'present' and not deploy_only and not module.params['system_qos_policy']:
        module.fail_json(msg='system_qos_policy is required when creating or configuring a domain profile.')
    if module.params['action_timeout'] <= 0 or module.params['action_poll_interval'] <= 0:
        module.fail_json(msg='action_timeout and action_poll_interval must be positive.')

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    cluster_path = '/fabric/SwitchClusterProfiles'
    name = intersight.module.params['name']
    organization = intersight.module.params['organization']
    state = intersight.module.params['state']

    if deploy_only:
        organization_moid = intersight.get_moid_by_name(
            resource_path='/organization/Organizations', resource_name=organization,
        )
        if not organization_moid:
            module.fail_json(msg="Organization '%s' not found." % organization)
        intersight.get_resource(
            resource_path=cluster_path,
            query_params={'$filter': "Name eq '%s' and Organization.Moid eq '%s'" % (name.replace("'", "''"), organization_moid)},
        )
        cluster_response = dict(intersight.result['api_response'])
        cluster_moid = cluster_response.get('Moid')
        if not cluster_moid:
            module.fail_json(msg="Domain profile '%s' not found in organization '%s'." % (name, organization))
        deploy_domain_profile(intersight, cluster_moid)
        intersight.result['api_response'] = cluster_response
        module.exit_json(**intersight.result)

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

    if cluster_moid and state == 'present' and module.params['action'] == 'Deploy':
        deploy_domain_profile(intersight, cluster_moid, configuration_changed=intersight.result['changed'])

    if cluster_response:
        intersight.result['api_response'] = cluster_response

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
