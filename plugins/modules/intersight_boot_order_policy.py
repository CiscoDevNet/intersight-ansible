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
module: intersight_boot_order_policy
short_description: Boot Order policy configuration for Cisco Intersight
description:
  - Boot Order policy configuration for Cisco Intersight.
  - Used to configure Boot Order servers and timezone settings on Cisco Intersight managed devices.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    choices: [present, absent]
    default: present
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    default: default
  name:
    description:
      - The name assigned to the Boot Order policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
  descrption:
    description:
      - The user-defined description of the Boot Order policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
  ConfiguredBootMode:
    description:
      - Sets the BIOS boot mode. 
      - UEFI uses the GUID Partition Table (GPT) whereas Legacy mode uses the Master Boot Record (MBR) partitioning scheme.
    type: string [Legacy,Uefi]
    default: legacy
  EnforceUefiSecureBoots:
    description:
      - If UEFI secure boot is enabled, the boot mode is set to UEFI by default.
      - Secure boot enforces that device boots using only software that is trusted by the Original Equipment Manufacturer (OEM).
    type: bool
    default: false
  boot_devices:
    description:
      - List of Boot Order devices configured on the endpoint.
    type: list
    options:
      iSCSI_Boot:
        suboptions: enable, device_name, slot, port
      Local_CDD:
        suboptions: enable, device_name
      Local_Disk:
        suboptions: enable, device_name, slot, bootloader_name(UEFI only), bootloader_description(UEFI only), bootloader_path(UEFI only)
      NVMe:
        suboptions: enable, device_name
      PCH_Storage:
        suboptions: enable, device_name, lun
      PXE_Boot:
        suboptions: enable, device_name, ip_type, pxe_type, slot, [interface_name, port, mac_addresses](depends on pxe_type)
      SAN_Boot:
        suboptions: enable, device_name, lun, slot, bootloader_name(UEFI only), bootloader_description(UEFI only), bootloader_path(UEFI only)
      SD_Card:
        suboptions: enable, device_name, lun, subtype
      UEFI_Shell:
        suboptions: enable, device_name
      USB:
        suboptions: enable, device_name, subtype
      Virtual_Media
        suboptions: enable, device_name, subtype
    all_suboptions:
      enable:
        description:
          - enable or disable the boot device
        type: bool
        default: true
      device_name:
          description: 
            - A name that helps identify a boot device. 
            - It should start and end with an alphanumeric character. 
            - It can have underscores and hyphens. 
            - It cannot be more than 30 characters.
          required: true
      slot:
        description:
          iSCSI_Boot:
            - The slot id of the device. Supported values are (1 - 255, "MLOM", "L", "L1", "L2", "OCP").
          Local_Disk:
            - The slot id of the local disk device. Supported values are (1-255, "M", "HBA", "SAS", "RAID", "MRAID", "MSTOR-RAID").
          PXE_Boot:
            - The slot ID of the adapter on which the underlying virtual ethernet interface is present. Supported values are ( 1 - 255, "MLOM", "L", "L1", "L2", "OCP").
          SAN_Boot:
            - Slot ID of the device. Supported values are ( 1 - 255, "MLOM", "L1", "L2" ).
        required:
          iSCSI_Boot: false
          Local_Disk: false
          PXE_Boot: true
          SAN_Boot: false
      port:
        description:
          iSCSI_Boot:
            - Port ID of the ISCSI boot device.
          PXE_Boot with Port as pxe_type:
            - Deprecated parameter. The port id of the PXE boot device.
        required: false
      lun:
        description:
          PCH_Storage:
            - The Logical Unit Number (LUN) of the device. 
            - It is the Virtual Drive number for Cisco UCS C-Series Servers. 
            - Virtual Drive number is found in storage inventory.
          San_Boot:
            - The Logical Unit Number (LUN) of the device.
          SD_Card:
            - The Logical Unit Number (LUN) of the device.
        required: false
      IpType: (only for PXE_Boot)
        description:
          - The IP Address family type to use during the PXE Boot process.
        supported_choices:
          - [None,IPv4, IPv6]
        required: false 
      interface_name: (only for PXE_Boot with Interface Name as pxe_type)
        description:
          - The name of the underlying virtual ethernet interface used by the PXE boot device.
        required: true
      MacAddress: (only for PXE_Boot with Mac Address as pxe_type)
        description:
          - The name of the underlying virtual ethernet interface used by the PXE boot device.
        required: true
      subtype:
        description:
          - The subtype for the selected device type.
        supported_choices:
          SD_Card:
            - [None, FlexUtil, FlexFlash, SdCard]
          USB:
            - [None, CD, FDD, HDD]
          Virtual_Media:
            - [None, CIMC MAPPED DVD, CIMC MAPPED HDD, KVM MAPPED DVD, KVM MAPPED HDD, KVM MAPPED FDD]
        required: false
    bootloader_name: (only in UEFI mode)
      description: 
        - Name of the bootloader image.
      required: false
    bootloader_description: (only in UEFI mode)
     description:
        - Carries more information about the bootloader.
      required: false
    bootloader_path: (only in UEFI mode)
      description:
        - Path to the bootloader image.
      required: false
author:
  - Tse Kai "Kevin" Chan (@BrightScale)
version_added: '2.10'
'''

EXAMPLES = r'''
- name: Configure Boot Order Policy
  cisco.intersight.intersight_boot_order_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-Boot
    description: Boot Order policy for COS
    tags:
      - Key: Site
        Value: RCDN
    configured_boot_mode: "UEFI"
    enforced_uefi_secure_boot: true
    boot_devices:
      device_type: "boot.LocalDisk"
      sub_options:
        device_name: "lDisk1"
        slot: RAID
        bootloader:
          bootloader_name: "lDiskBL"
          bootloader_description: "Booloader for lDisk1"
          bootloader_path: ""

- name: Delete Boot Order Policy
  cisco.intersight.intersight_boot_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-Boot
    state: absent
'''

RETURN = r'''
api_repsonse:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-Boot",
        "ObjectType": "boot.Policy",
        "Tags": [
            {
                "Key": "Site",
                "Value": "RCDN"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec, compare_values


def main():
    argument_spec = intersight_argument_spec
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        organization=dict(type='str', default='default'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr'], default=''),
        tags=dict(type='list', default=[]),
        enable=dict(type='bool', default=True),
        boot_loader_description=dict(type='str'),
        boot_loader_name=dict(type='str'),
        boot_loader_name=dict(type='str'),
        boot_devices=list(type='dict',options=boot_order_mapping),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''
    # Defined API body used in compares or create
    intersight.api_body = {
        'Organization': {
            'Name': intersight.module.params['organization'],
        },
        'Name': intersight.module.params['name'],
        'Tags': intersight.module.params['tags'],
        'Description': intersight.module.params['description'],
        'ConfiguredBootMode': intersight.module.params['configured_boot_mode'],
        "EnforceUefiSecureBoot": intrersight.module.params['enforced_uefi_secure_boot'],
        'BootDevices': [],
    }
    if intersight.module.params.get('boot_devices'):
      for device in intersight.module.params['boot_devices']:
        if device['device_type'] == 'boot.Iscsi':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.Iscsi",
              "ObjectType": "boot.Iscsi",
              "Enabled" : device['enabled'],
              "Name" : device['name'],
              "Slot" : device['slot'],
              "Port" : device['port'],
            }
          )
        elif device['device_type'] == 'boot.LocalCDD':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.LocalCDD",
              "ObjectType": "boot.LocalCDD",
              "Enabled" : device['enabled']
              "Name" : device['name'],
            }
          )
        elif device['device_type'] == 'boot.LocalDisk':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.LocalDisk",
              "ObjectType": "boot.LocalDisk",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "Slot": device['slot'],
              "Bootloader": {
                "ClassId": "boot.Bootloader",
                "ObjectType": "boot.Bootloader",
                "Description": device['boot_loader_description'],
                "Name": device['boot_loader_name'],
                "Path": device['boot_loader_path'],
              },
            }
          )
         elif device['device_type'] == 'boot.NVMe':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.NVMe",
              "ObjectType": "boot.NVMe",
              "Enabled": device['enabled'],
              "Name": device['name'],
            }
          )
         elif device['device_type'] == 'boot.PchStorage':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.PchStorage",
              "ObjectType": "boot.PchStorage",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "LUN": device['lun'],
            }
          )
        elif device['device_type'] == 'boot.Pxe':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.Pxe",
              "ObjectType": "boot.Pxe",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "IpType" : device['ip_type'],
              "InterfaceSource" : device['interface_source'],
              "Slot": device['slot'],
              "InterfaceName" : device['interface_name'],
              "Port" : device['port'],
              "MacAddress" : device['mac_address'],
            }
          )
        elif device['device_type'] == 'boot.San':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.San",
              "ObjectType": "boot.San",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "LUN" : device['lun'],
              "Slot": device['slot'],
              "Bootloader": {
                "ClassId": "boot.Bootloader",
                "ObjectType": "boot.Bootloader",
                "Description": device['boot_loader_description'],
                "Name": device['boot_loader_name'],
                "Path": device['boot_loader_path'],
              },
            }
          )
        elif device['device_type'] == 'boot.SdCard':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.SdCard",
              "ObjectType": "boot.SdCard",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "LUN": device['lun'],
              "SubType" : device['subtype'],
            }
          )
        elif device['device_type'] == 'boot.UefiShell':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.UefiShell",
              "ObjectType": "boot.UefiShell",
              "Enabled": device['enabled'],
              "Name": device['name'],
            }
          )
        elif device['device_type'] == 'boot.Usb':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.Usb",
              "ObjectType": "boot.Usb",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "SubType" : device['subtype'],
            }
          )
        elif device['device_type'] == 'boot.VirtualMedia':
          intersight.api_body['BootDevices'].append(
            {
              "ClassId": "boot.VirtualMedia",
              "ObjectType": "boot.VirtualMedia",
              "Enabled": device['enabled'],
              "Name": device['name'],
              "SubType" : device['subtype'],
            }
          )
    organization_moid = None
    # GET Organization Moid
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
    # get the current state of the resource
    filter_str = "Name eq '" + intersight.module.params['name'] + "'"
    filter_str += "and Organization.Moid eq '" + organization_moid + "'"
    intersight.get_resource(
        resource_path='/boot/Policies',
        query_params={
            '$filter': filter_str,
            '$expand': 'Organization',
        },
    )

    moid = None
    resource_values_match = False
    if intersight.result['api_response'].get('Moid'):
        # resource exists and moid was returned
        moid = intersight.result['api_response']['Moid']
        if module.params['state'] == 'present':
            resource_values_match = compare_values(intersight.api_body, intersight.result['api_response'])
        else:  # state == 'absent'
            intersight.delete_resource(
                moid=moid,
                resource_path='/boot/Policies',
            )
            moid = None

    if module.params['state'] == 'present' and not resource_values_match:
        # remove read-only Organization key
        intersight.api_body.pop('Organization')
        if not moid:
            # Organization must be set, but can't be changed after initial POST
            intersight.api_body['Organization'] = {
                'Moid': organization_moid,
            }
        intersight.configure_resource(
            moid=moid,
            resource_path='/boot/Policies',
            body=intersight.api_body,
            query_params={
                '$filter': filter_str,
            },
        )

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
