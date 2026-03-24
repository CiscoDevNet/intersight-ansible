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
module: intersight_server_profile_template
short_description: Manage Server Profile Templates in Cisco Intersight
description:
  - Create, update, and delete Server Profile Templates on Cisco Intersight.
  - Server Profile Templates define a reusable configuration that can be used to derive multiple Server Profiles.
  - Policies are attached to the template via the PolicyBucket sub-resource endpoint.
  - To derive Server Profiles from a template, use the derive_profiles playbook included in this collection.
    See U(https://github.com/CiscoDevNet/intersight-ansible/blob/master/playbooks/derive_profiles.yml) for details.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs/server/ProfileTemplate/post/).
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
      - Templates and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    type: str
    default: default
  name:
    description:
      - The name assigned to the Server Profile Template.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    type: str
    required: true
  description:
    description:
      - The user-defined description of the Server Profile Template.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    type: str
    aliases: [descr]
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  target_platform:
    description:
      - The platform for which the server profile template is applicable.
      - C(standalone) for servers operating in Standalone mode.
      - C(fi-attached) for servers attached to a Fabric Interconnect managed by Intersight.
      - C(unified-edge) for Unified Edge servers.
    type: str
    choices: [standalone, fi-attached, unified-edge]
    default: standalone
  adapter_policy:
    description:
      - Name of Adapter Configuration Policy to associate with this template.
    type: str
  bios_policy:
    description:
      - Name of BIOS Policy to associate with this template.
    type: str
  boot_order_policy:
    description:
      - Name of Boot Order Policy to associate with this template.
    type: str
  certificate_policy:
    description:
      - Name of Certificate Management Policy to associate with this template.
    type: str
  device_connector_policy:
    description:
      - Name of Device Connector Policy to associate with this template.
    type: str
  drive_security_policy:
    description:
      - Name of Drive Security Policy to associate with this template.
    type: str
  firmware_policy:
    description:
      - Name of Firmware Policy to associate with this template.
    type: str
  ipmi_over_lan_policy:
    description:
      - Name of IPMI over LAN Policy to associate with this template.
    type: str
  lan_connectivity_policy:
    description:
      - Name of LAN Connectivity Policy to associate with this template.
    type: str
  ldap_policy:
    description:
      - Name of LDAP Policy to associate with this template.
    type: str
  local_user_policy:
    description:
      - Name of Local User Policy to associate with this template.
    type: str
  memory_policy:
    description:
      - Name of Memory Policy to associate with this template.
    type: str
  network_connectivity_policy:
    description:
      - Name of Network Connectivity Policy to associate with this template.
    type: str
  ntp_policy:
    description:
      - Name of NTP Policy to associate with this template.
    type: str
  persistent_memory_policy:
    description:
      - Name of Persistent Memory Policy to associate with this template.
    type: str
  power_policy:
    description:
      - Name of Power Policy to associate with this template.
    type: str
  san_connectivity_policy:
    description:
      - Name of SAN Connectivity Policy to associate with this template.
    type: str
  sd_card_policy:
    description:
      - Name of SD Card Policy to associate with this template.
    type: str
  serial_over_lan_policy:
    description:
      - Name of Serial over LAN Policy to associate with this template.
    type: str
  smtp_policy:
    description:
      - Name of SMTP Policy to associate with this template.
    type: str
  snmp_policy:
    description:
      - Name of SNMP Policy to associate with this template.
    type: str
  ssh_policy:
    description:
      - Name of SSH Policy to associate with this template.
    type: str
  storage_policy:
    description:
      - Name of Storage Policy to associate with this template.
    type: str
  syslog_policy:
    description:
      - Name of Syslog Policy to associate with this template.
    type: str
  thermal_policy:
    description:
      - Name of Thermal Policy to associate with this template.
    type: str
  virtual_kvm_policy:
    description:
      - Name of Virtual KVM Policy to associate with this template.
    type: str
  virtual_media_policy:
    description:
      - Name of Virtual Media Policy to associate with this template.
    type: str
author:
  - Ron Gershburg (@rgershbu)
'''

EXAMPLES = r'''
- name: Create a basic Server Profile Template
  cisco.intersight.intersight_server_profile_template:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "SPT-Standalone-Basic"
    description: "Basic standalone server profile template"
    target_platform: standalone
    tags:
      - Key: "Environment"
        Value: "Production"
    state: present

- name: Create a Server Profile Template with policies
  cisco.intersight.intersight_server_profile_template:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: "default"
    name: "SPT-FI-Production"
    description: "FI-Attached template with policies"
    target_platform: fi-attached
    bios_policy: "BIOS-Production"
    boot_order_policy: "Boot-UEFI"
    firmware_policy: "FW-Latest"
    ntp_policy: "NTP-Corp"
    power_policy: "Power-Grid-Redundancy"
    storage_policy: "Storage-M2-Boot"
    lan_connectivity_policy: "LAN-Prod"
    san_connectivity_policy: "SAN-Prod"
    state: present

- name: Delete a Server Profile Template
  cisco.intersight.intersight_server_profile_template:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    name: "SPT-Standalone-Basic"
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "SPT-FI-Production",
        "ObjectType": "server.ProfileTemplate",
        "TargetPlatform": "FIAttached",
        "PolicyBucket": [
            {
                "Moid": "6937ec186275723101f63708",
                "ObjectType": "bios.Policy"
            },
            {
                "Moid": "69a42f0770686131014f259c",
                "ObjectType": "firmware.Policy"
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
    'adapter_policy': {'resource_path': '/adapter/ConfigPolicies', 'object_type': 'adapter.ConfigPolicy'},
    'bios_policy': {'resource_path': '/bios/Policies', 'object_type': 'bios.Policy'},
    'boot_order_policy': {'resource_path': '/boot/PrecisionPolicies', 'object_type': 'boot.PrecisionPolicy'},
    'certificate_policy': {'resource_path': '/certificatemanagement/Policies', 'object_type': 'certificatemanagement.Policy'},
    'device_connector_policy': {'resource_path': '/deviceconnector/Policies', 'object_type': 'deviceconnector.Policy'},
    'drive_security_policy': {'resource_path': '/storage/DriveSecurityPolicies', 'object_type': 'storage.DriveSecurityPolicy'},
    'firmware_policy': {'resource_path': '/firmware/Policies', 'object_type': 'firmware.Policy'},
    'ipmi_over_lan_policy': {'resource_path': '/ipmioverlan/Policies', 'object_type': 'ipmioverlan.Policy'},
    'lan_connectivity_policy': {'resource_path': '/vnic/LanConnectivityPolicies', 'object_type': 'vnic.LanConnectivityPolicy'},
    'ldap_policy': {'resource_path': '/iam/LdapPolicies', 'object_type': 'iam.LdapPolicy'},
    'local_user_policy': {'resource_path': '/iam/EndPointUserPolicies', 'object_type': 'iam.EndPointUserPolicy'},
    'memory_policy': {'resource_path': '/memory/Policies', 'object_type': 'memory.Policy'},
    'network_connectivity_policy': {'resource_path': '/networkconfig/Policies', 'object_type': 'networkconfig.Policy'},
    'ntp_policy': {'resource_path': '/ntp/Policies', 'object_type': 'ntp.Policy'},
    'persistent_memory_policy': {'resource_path': '/memory/PersistentMemoryPolicies', 'object_type': 'memory.PersistentMemoryPolicy'},
    'power_policy': {'resource_path': '/power/Policies', 'object_type': 'power.Policy'},
    'san_connectivity_policy': {'resource_path': '/vnic/SanConnectivityPolicies', 'object_type': 'vnic.SanConnectivityPolicy'},
    'sd_card_policy': {'resource_path': '/sdcard/Policies', 'object_type': 'sdcard.Policy'},
    'serial_over_lan_policy': {'resource_path': '/sol/Policies', 'object_type': 'sol.Policy'},
    'smtp_policy': {'resource_path': '/smtp/Policies', 'object_type': 'smtp.Policy'},
    'snmp_policy': {'resource_path': '/snmp/Policies', 'object_type': 'snmp.Policy'},
    'ssh_policy': {'resource_path': '/ssh/Policies', 'object_type': 'ssh.Policy'},
    'storage_policy': {'resource_path': '/storage/StoragePolicies', 'object_type': 'storage.StoragePolicy'},
    'syslog_policy': {'resource_path': '/syslog/Policies', 'object_type': 'syslog.Policy'},
    'thermal_policy': {'resource_path': '/thermal/Policies', 'object_type': 'thermal.Policy'},
    'virtual_kvm_policy': {'resource_path': '/kvm/Policies', 'object_type': 'kvm.Policy'},
    'virtual_media_policy': {'resource_path': '/vmedia/Policies', 'object_type': 'vmedia.Policy'},
}

TARGET_PLATFORM_MAP = {
    'standalone': 'Standalone',
    'fi-attached': 'FIAttached',
    'unified-edge': 'UnifiedEdgeServer',
}


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr']),
        tags=dict(type='list', elements='dict'),
        target_platform=dict(type='str', choices=['standalone', 'fi-attached', 'unified-edge'], default='standalone'),
        adapter_policy=dict(type='str'),
        bios_policy=dict(type='str'),
        boot_order_policy=dict(type='str'),
        certificate_policy=dict(type='str'),
        device_connector_policy=dict(type='str'),
        drive_security_policy=dict(type='str'),
        firmware_policy=dict(type='str'),
        ipmi_over_lan_policy=dict(type='str'),
        lan_connectivity_policy=dict(type='str'),
        ldap_policy=dict(type='str'),
        local_user_policy=dict(type='str'),
        memory_policy=dict(type='str'),
        network_connectivity_policy=dict(type='str'),
        ntp_policy=dict(type='str'),
        persistent_memory_policy=dict(type='str'),
        power_policy=dict(type='str'),
        san_connectivity_policy=dict(type='str'),
        sd_card_policy=dict(type='str'),
        serial_over_lan_policy=dict(type='str'),
        smtp_policy=dict(type='str'),
        snmp_policy=dict(type='str'),
        ssh_policy=dict(type='str'),
        storage_policy=dict(type='str'),
        syslog_policy=dict(type='str'),
        thermal_policy=dict(type='str'),
        virtual_kvm_policy=dict(type='str'),
        virtual_media_policy=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Create/update the template itself
    resource_path = '/server/ProfileTemplates'

    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
    }

    if intersight.module.params['state'] == 'present':
        intersight.set_tags_and_description()
        api_target_platform = TARGET_PLATFORM_MAP[intersight.module.params['target_platform']]
        intersight.api_body['TargetPlatform'] = api_target_platform

    intersight.configure_policy_or_profile(resource_path=resource_path)
    template_response = intersight.result['api_response']
    template_moid = template_response.get('Moid') if template_response else None

    # Sync PolicyBucket via the sub-resource endpoint
    if template_moid and intersight.module.params['state'] == 'present':
        organization_name = intersight.module.params['organization']
        desired_bucket = resolve_policy_bucket(intersight, organization_name, POLICY_MAPPING)
        current_bucket = template_response.get('PolicyBucket') or []
        bucket_path = f'/server/ProfileTemplates/{template_moid}/PolicyBucket'
        sync_policy_bucket(intersight, bucket_path, desired_bucket, current_bucket)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
