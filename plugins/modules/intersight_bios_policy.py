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
module: intersight_bios_policy
short_description: BIOS policy configuration for Cisco Intersight
description:
  - BIOS policy configuration for Cisco Intersight.
  - Used to configure BIOS settings on Cisco Intersight managed devices.
  - For more information see L(Cisco Intersight,https://intersight.com/apidocs).
extends_documentation_fragment: intersight
options:
  state:
    description:
      - If C(present), will verify the resource is present and will create if needed.
      - If C(absent), will verify the resource is absent and will delete if needed.
    choices: [present, absent]
    default: present
    type: str
  organization:
    description:
      - The name of the Organization this resource is assigned to.
      - Profiles and Policies that are created within a Custom Organization are applicable only to devices in the same Organization.
    default: default
    type: str
  name:
    description:
      - The name assigned to the BIOS policy.
      - The name must be between 1 and 62 alphanumeric characters, allowing special characters :-_.
    required: true
    type: str
  tags:
    description:
      - List of tags in Key:<user-defined key> Value:<user-defined value> format.
    type: list
    elements: dict
  description:
    description:
      - The user-defined description of the BIOS policy.
      - Description can contain letters(a-z, A-Z), numbers(0-9), hyphen(-), period(.), colon(:), or an underscore(_).
    aliases: [descr]
    type: str
  acs_control_gpu1state:
    description:
      -  BIOS Token for setting ACS Control GPU 1 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu2state:
    description:
      -  BIOS Token for setting ACS Control GPU 2 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu3state:
    description:
      -  BIOS Token for setting ACS Control GPU 3 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu4state:
    description:
      -  BIOS Token for setting ACS Control GPU 4 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu5state:
    description:
      -  BIOS Token for setting ACS Control GPU 5 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu6state:
    description:
      -  BIOS Token for setting ACS Control GPU 6 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu7state:
    description:
      -  BIOS Token for setting ACS Control GPU 7 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_gpu8state:
    description:
      -  BIOS Token for setting ACS Control GPU 8 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_slot11state:
    description:
      -  BIOS Token for setting ACS Control Slot 11 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_slot12state:
    description:
      -  BIOS Token for setting ACS Control Slot 12 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_slot13state:
    description:
      -  BIOS Token for setting ACS Control Slot 13 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  acs_control_slot14state:
    description:
      -  BIOS Token for setting ACS Control Slot 14 configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  adaptive_refresh_mgmt_level:
    description:
      -  BIOS Token for setting Adaptive Refresh Management Level configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Default - Value - Default for configuring adaptive_refresh_mgmt_level token.
      -  Level A - Value - Level A for configuring adaptive_refresh_mgmt_level token.
      -  Level B - Value - Level B for configuring adaptive_refresh_mgmt_level token.
      -  Level C - Value - Level C for configuring adaptive_refresh_mgmt_level token.
    choices: ['platform-default' , 'Default' , 'Level A' , 'Level B' , 'Level C']
    type: str
  adjacent_cache_line_prefetch:
    description:
      -  BIOS Token for setting Adjacent Cache Line Prefetcher configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  advanced_mem_test:
    description:
      -  BIOS Token for setting Enhanced Memory Test configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring advanced_mem_test token.
      -  disabled - Value - disabled for configuring advanced_mem_test token.
      -  enabled - Value - enabled for configuring advanced_mem_test token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  all_usb_devices:
    description:
      -  BIOS Token for setting All USB Devices configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  altitude:
    description:
      -  BIOS Token for setting altitude configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  300-m - Value - 300-m for configuring altitude token.
      -  900-m - Value - 900-m for configuring altitude token.
      -  1500-m - Value - 1500-m for configuring altitude token.
      -  3000-m - Value - 3000-m for configuring altitude token.
      -  auto - Value - auto for configuring altitude token.
    choices: ['platform-default' , '300-m' , '900-m' , '1500-m' , '3000-m' , 'auto']
    type: str
  aspm_support:
    description:
      -  BIOS Token for setting ASPM Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring aspm_support token.
      -  Disabled - Value - Disabled for configuring aspm_support token.
      -  Force L0s - Value - Force L0s for configuring aspm_support token.
      -  L1 Only - Value - L1 Only for configuring aspm_support token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'Force L0s' , 'L1 Only']
    type: str
  assert_nmi_on_perr:
    description:
      -  BIOS Token for setting Assert NMI on PERR configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  assert_nmi_on_serr:
    description:
      -  BIOS Token for setting Assert NMI on SERR configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  auto_cc_state:
    description:
      -  BIOS Token for setting Autonomous Core C State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  autonumous_cstate_enable:
    description:
      -  BIOS Token for setting CPU Autonomous C State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  baud_rate:
    description:
      -  BIOS Token for setting Baud Rate configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  9600 - Value - 9600 for configuring baud_rate token.
      -  19200 - Value - 19200 for configuring baud_rate token.
      -  38400 - Value - 38400 for configuring baud_rate token.
      -  57600 - Value - 57600 for configuring baud_rate token.
      -  115200 - Value - 115200 for configuring baud_rate token.
    choices: ['platform-default' , '9600' , '19200' , '38400' , '57600' , '115200']
    type: str
  bme_dma_mitigation:
    description:
      -  BIOS Token for setting BME DMA Mitigation configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  boot_option_num_retry:
    description:
      -  BIOS Token for setting Number of Retries configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  5 - Value - 5 for configuring boot_option_num_retry token.
      -  13 - Value - 13 for configuring boot_option_num_retry token.
      -  Infinite - Value - Infinite for configuring boot_option_num_retry token.
    choices: ['platform-default' , '5' , '13' , 'Infinite']
    type: str
  boot_option_re_cool_down:
    description:
      -  BIOS Token for setting Cool Down Time  (sec) configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  15 - Value - 15 for configuring boot_option_re_cool_down token.
      -  45 - Value - 45 for configuring boot_option_re_cool_down token.
      -  90 - Value - 90 for configuring boot_option_re_cool_down token.
    choices: ['platform-default' , '15' , '45' , '90']
    type: str
  boot_option_retry:
    description:
      -  BIOS Token for setting Boot Option Retry configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  boot_performance_mode:
    description:
      -  BIOS Token for setting Boot Performance Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Max Efficient - Value - Max Efficient for configuring boot_performance_mode token.
      -  Max Performance - Value - Max Performance for configuring boot_performance_mode token.
      -  Set by Intel NM - Value - Set by Intel NM for configuring boot_performance_mode token.
    choices: ['platform-default' , 'Max Efficient' , 'Max Performance' , 'Set by Intel NM']
    type: str
  burst_and_postponed_refresh:
    description:
      -  BIOS Token for setting Burst and Postponed Refresh configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  c1auto_demotion:
    description:
      -  BIOS Token for setting C1 Auto Demotion configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  c1auto_un_demotion:
    description:
      -  BIOS Token for setting C1 Auto UnDemotion configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cbs_cmn_apbdis:
    description:
      -  BIOS Token for setting APBDIS configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  0 - Value - 0 for configuring cbs_cmn_apbdis token.
      -  1 - Value - 1 for configuring cbs_cmn_apbdis token.
      -  Auto - Value - Auto for configuring cbs_cmn_apbdis token.
    choices: ['platform-default' , '0' , '1' , 'Auto']
    type: str
  cbs_cmn_cpu_cpb:
    description:
      -  BIOS Token for setting Core Performance Boost configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_cpb token.
      -  disabled - Value - disabled for configuring cbs_cmn_cpu_cpb token.
    choices: ['platform-default' , 'Auto' , 'disabled']
    type: str
  cbs_cmn_cpu_gen_downcore_ctrl:
    description:
      -  BIOS Token for setting Downcore Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
      -  FOUR (2 + 2) - Value - FOUR (2 + 2) for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
      -  FOUR (4 + 0) - Value - FOUR (4 + 0) for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
      -  SIX (3 + 3) - Value - SIX (3 + 3) for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
      -  THREE (3 + 0) - Value - THREE (3 + 0) for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
      -  TWO (1 + 1) - Value - TWO (1 + 1) for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
      -  TWO (2 + 0) - Value - TWO (2 + 0) for configuring cbs_cmn_cpu_gen_downcore_ctrl token.
    choices: ['platform-default' , 'Auto' , 'FOUR (2 + 2)' , 'FOUR (4 + 0)' , 'SIX (3 + 3)' , 'THREE (3 + 0)' , 'TWO (1 + 1)' , 'TWO (2 + 0)']
    type: str
  cbs_cmn_cpu_global_cstate_ctrl:
    description:
      -  BIOS Token for setting Global C State Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_global_cstate_ctrl token.
      -  disabled - Value - disabled for configuring cbs_cmn_cpu_global_cstate_ctrl token.
      -  enabled - Value - enabled for configuring cbs_cmn_cpu_global_cstate_ctrl token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_cpu_l1stream_hw_prefetcher:
    description:
      -  BIOS Token for setting L1 Stream HW Prefetcher configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_l1stream_hw_prefetcher token.
      -  disabled - Value - disabled for configuring cbs_cmn_cpu_l1stream_hw_prefetcher token.
      -  enabled - Value - enabled for configuring cbs_cmn_cpu_l1stream_hw_prefetcher token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_cpu_l2stream_hw_prefetcher:
    description:
      -  BIOS Token for setting L2 Stream HW Prefetcher configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_l2stream_hw_prefetcher token.
      -  disabled - Value - disabled for configuring cbs_cmn_cpu_l2stream_hw_prefetcher token.
      -  enabled - Value - enabled for configuring cbs_cmn_cpu_l2stream_hw_prefetcher token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_cpu_smee:
    description:
      -  BIOS Token for setting CPU SMEE configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_smee token.
      -  disabled - Value - disabled for configuring cbs_cmn_cpu_smee token.
      -  enabled - Value - enabled for configuring cbs_cmn_cpu_smee token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_cpu_streaming_stores_ctrl:
    description:
      -  BIOS Token for setting Streaming Stores Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_cpu_streaming_stores_ctrl token.
      -  disabled - Value - disabled for configuring cbs_cmn_cpu_streaming_stores_ctrl token.
      -  enabled - Value - enabled for configuring cbs_cmn_cpu_streaming_stores_ctrl token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmnc_tdp_ctl:
    description:
      -  BIOS Token for setting cTDP Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmnc_tdp_ctl token.
      -  Manual - Value - Manual for configuring cbs_cmnc_tdp_ctl token.
    choices: ['platform-default' , 'Auto' , 'Manual']
    type: str
  cbs_cmn_determinism_slider:
    description:
      -  BIOS Token for setting Determinism Slider configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_determinism_slider token.
      -  Performance - Value - Performance for configuring cbs_cmn_determinism_slider token.
      -  Power - Value - Power for configuring cbs_cmn_determinism_slider token.
    choices: ['platform-default' , 'Auto' , 'Performance' , 'Power']
    type: str
  cbs_cmn_efficiency_mode_en:
    description:
      -  BIOS Token for setting Efficiency Mode Enable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_efficiency_mode_en token.
      -  Enabled - Value - Enabled for configuring cbs_cmn_efficiency_mode_en token.
    choices: ['platform-default' , 'Auto' , 'Enabled']
    type: str
  cbs_cmn_fixed_soc_pstate:
    description:
      -  BIOS Token for setting Fixed SOC P-State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_fixed_soc_pstate token.
      -  P0 - Value - P0 for configuring cbs_cmn_fixed_soc_pstate token.
      -  P1 - Value - P1 for configuring cbs_cmn_fixed_soc_pstate token.
      -  P2 - Value - P2 for configuring cbs_cmn_fixed_soc_pstate token.
      -  P3 - Value - P3 for configuring cbs_cmn_fixed_soc_pstate token.
    choices: ['platform-default' , 'Auto' , 'P0' , 'P1' , 'P2' , 'P3']
    type: str
  cbs_cmn_gnb_nb_iommu:
    description:
      -  BIOS Token for setting IOMMU configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_gnb_nb_iommu token.
      -  disabled - Value - disabled for configuring cbs_cmn_gnb_nb_iommu token.
      -  enabled - Value - enabled for configuring cbs_cmn_gnb_nb_iommu token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_gnb_smucppc:
    description:
      -  BIOS Token for setting CPPC configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_gnb_smucppc token.
      -  disabled - Value - disabled for configuring cbs_cmn_gnb_smucppc token.
      -  enabled - Value - enabled for configuring cbs_cmn_gnb_smucppc token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_gnb_smu_df_cstates:
    description:
      -  BIOS Token for setting DF C-States configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_gnb_smu_df_cstates token.
      -  disabled - Value - disabled for configuring cbs_cmn_gnb_smu_df_cstates token.
      -  enabled - Value - enabled for configuring cbs_cmn_gnb_smu_df_cstates token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_mem_ctrl_bank_group_swap_ddr4:
    description:
      -  BIOS Token for setting Bank Group Swap configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_mem_ctrl_bank_group_swap_ddr4 token.
      -  disabled - Value - disabled for configuring cbs_cmn_mem_ctrl_bank_group_swap_ddr4 token.
      -  enabled - Value - enabled for configuring cbs_cmn_mem_ctrl_bank_group_swap_ddr4 token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_cmn_mem_map_bank_interleave_ddr4:
    description:
      -  BIOS Token for setting Chipset Interleave configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cmn_mem_map_bank_interleave_ddr4 token.
      -  disabled - Value - disabled for configuring cbs_cmn_mem_map_bank_interleave_ddr4 token.
    choices: ['platform-default' , 'Auto' , 'disabled']
    type: str
  cbs_cpu_ccd_ctrl_ssp:
    description:
      -  BIOS Token for setting CCD Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  2 CCDs - Value - 2 CCDs for configuring cbs_cpu_ccd_ctrl_ssp token.
      -  3 CCDs - Value - 3 CCDs for configuring cbs_cpu_ccd_ctrl_ssp token.
      -  4 CCDs - Value - 4 CCDs for configuring cbs_cpu_ccd_ctrl_ssp token.
      -  6 CCDs - Value - 6 CCDs for configuring cbs_cpu_ccd_ctrl_ssp token.
      -  Auto - Value - Auto for configuring cbs_cpu_ccd_ctrl_ssp token.
    choices: ['platform-default' , '2 CCDs' , '3 CCDs' , '4 CCDs' , '6 CCDs' , 'Auto']
    type: str
  cbs_cpu_core_ctrl:
    description:
      -  BIOS Token for setting CPU Downcore control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cpu_core_ctrl token.
      -  FIVE (5 + 0) - Value - FIVE (5 + 0) for configuring cbs_cpu_core_ctrl token.
      -  FOUR (4 + 0) - Value - FOUR (4 + 0) for configuring cbs_cpu_core_ctrl token.
      -  ONE (1 + 0) - Value - ONE (1 + 0) for configuring cbs_cpu_core_ctrl token.
      -  SEVEN (7 + 0) - Value - SEVEN (7 + 0) for configuring cbs_cpu_core_ctrl token.
      -  SIX (6 + 0) - Value - SIX (6 + 0) for configuring cbs_cpu_core_ctrl token.
      -  THREE (3 + 0) - Value - THREE (3 + 0) for configuring cbs_cpu_core_ctrl token.
      -  TWO (2 + 0) - Value - TWO (2 + 0) for configuring cbs_cpu_core_ctrl token.
    choices: ['platform-default' , 'Auto' , 'FIVE (5 + 0)' , 'FOUR (4 + 0)' , 'ONE (1 + 0)' , 'SEVEN (7 + 0)' , 'SIX (6 + 0)' , 'THREE (3 + 0)' , 'TWO (2 + 0)']
    type: str
  cbs_cpu_smt_ctrl:
    description:
      -  BIOS Token for setting CPU SMT Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_cpu_smt_ctrl token.
      -  disabled - Value - disabled for configuring cbs_cpu_smt_ctrl token.
      -  enabled - Value - enabled for configuring cbs_cpu_smt_ctrl token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_dbg_cpu_snp_mem_cover:
    description:
      -  BIOS Token for setting SNP Memory Coverage configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_dbg_cpu_snp_mem_cover token.
      -  Custom - Value - Custom for configuring cbs_dbg_cpu_snp_mem_cover token.
      -  disabled - Value - disabled for configuring cbs_dbg_cpu_snp_mem_cover token.
      -  enabled - Value - enabled for configuring cbs_dbg_cpu_snp_mem_cover token.
    choices: ['platform-default' , 'Auto' , 'Custom' , 'disabled' , 'enabled']
    type: str
  cbs_dbg_cpu_snp_mem_size_cover:
    description:
      -  BIOS Token for setting SNP Memory Size to Cover in MiB configuration (0 - 1048576 MiB).
    type: str
  cbs_df_cmn_acpi_srat_l3numa:
    description:
      -  BIOS Token for setting ACPI SRAT L3 Cache As NUMA Domain configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_df_cmn_acpi_srat_l3numa token.
      -  disabled - Value - disabled for configuring cbs_df_cmn_acpi_srat_l3numa token.
      -  enabled - Value - enabled for configuring cbs_df_cmn_acpi_srat_l3numa token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  cbs_df_cmn_dram_nps:
    description:
      -  BIOS Token for setting NUMA Nodes per Socket configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_df_cmn_dram_nps token.
      -  NPS0 - Value - NPS0 for configuring cbs_df_cmn_dram_nps token.
      -  NPS1 - Value - NPS1 for configuring cbs_df_cmn_dram_nps token.
      -  NPS2 - Value - NPS2 for configuring cbs_df_cmn_dram_nps token.
      -  NPS4 - Value - NPS4 for configuring cbs_df_cmn_dram_nps token.
    choices: ['platform-default' , 'Auto' , 'NPS0' , 'NPS1' , 'NPS2' , 'NPS4']
    type: str
  cbs_df_cmn_mem_intlv:
    description:
      -  BIOS Token for setting AMD Memory Interleaving configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cbs_df_cmn_mem_intlv token.
      -  Channel - Value - Channel for configuring cbs_df_cmn_mem_intlv token.
      -  Die - Value - Die for configuring cbs_df_cmn_mem_intlv token.
      -  None - Value - None for configuring cbs_df_cmn_mem_intlv token.
      -  Socket - Value - Socket for configuring cbs_df_cmn_mem_intlv token.
    choices: ['platform-default' , 'Auto' , 'Channel' , 'Die' , 'None' , 'Socket']
    type: str
  cbs_df_cmn_mem_intlv_size:
    description:
      -  BIOS Token for setting AMD Memory Interleaving Size configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  256 Bytes - Value - 256 Bytes for configuring cbs_df_cmn_mem_intlv_size token.
      -  512 Bytes - Value - 512 Bytes for configuring cbs_df_cmn_mem_intlv_size token.
      -  1 KB - Value - 1 KiB for configuring cbs_df_cmn_mem_intlv_size token.
      -  2 KB - Value - 2 KiB for configuring cbs_df_cmn_mem_intlv_size token.
      -  4 KB - Value - 4 KiB for configuring cbs_df_cmn_mem_intlv_size token.
      -  Auto - Value - Auto for configuring cbs_df_cmn_mem_intlv_size token.
    choices: ['platform-default' , '256 Bytes' , '512 Bytes' , '1 KB' , '2 KB' , '4 KB' , 'Auto']
    type: str
  cbs_sev_snp_support:
    description:
      -  BIOS Token for setting SEV-SNP Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cdn_enable:
    description:
      -  BIOS Token for setting Consistent Device Naming configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cdn_support:
    description:
      -  BIOS Token for setting CDN Support for LOM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring cdn_support token.
      -  enabled - Value - enabled for configuring cdn_support token.
      -  LOMs Only - Value - LOMs Only for configuring cdn_support token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'LOMs Only']
    type: str
  channel_inter_leave:
    description:
      -  BIOS Token for setting Channel Interleaving configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1-way - Value - 1-way for configuring channel_inter_leave token.
      -  2-way - Value - 2-way for configuring channel_inter_leave token.
      -  3-way - Value - 3-way for configuring channel_inter_leave token.
      -  4-way - Value - 4-way for configuring channel_inter_leave token.
      -  auto - Value - auto for configuring channel_inter_leave token.
    choices: ['platform-default' , '1-way' , '2-way' , '3-way' , '4-way' , 'auto']
    type: str
  cisco_adaptive_mem_training:
    description:
      -  BIOS Token for setting Adaptive Memory Training configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cisco_debug_level:
    description:
      -  BIOS Token for setting BIOS Techlog Level configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Maximum - Value - Maximum for configuring cisco_debug_level token.
      -  Minimum - Value - Minimum for configuring cisco_debug_level token.
      -  Normal - Value - Normal for configuring cisco_debug_level token.
    choices: ['platform-default' , 'Maximum' , 'Minimum' , 'Normal']
    type: str
  cisco_oprom_launch_optimization:
    description:
      -  BIOS Token for setting OptionROM Launch Optimization configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cisco_xgmi_max_speed:
    description:
      -  BIOS Token for setting Cisco xGMI Max Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cke_low_policy:
    description:
      -  BIOS Token for setting CKE Low Policy configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  auto - Value - auto for configuring cke_low_policy token.
      -  disabled - Value - disabled for configuring cke_low_policy token.
      -  fast - Value - fast for configuring cke_low_policy token.
      -  slow - Value - slow for configuring cke_low_policy token.
    choices: ['platform-default' , 'auto' , 'disabled' , 'fast' , 'slow']
    type: str
  closed_loop_therm_throtl:
    description:
      -  BIOS Token for setting Closed Loop Thermal Throttling configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cmci_enable:
    description:
      -  BIOS Token for setting Processor CMCI configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  config_tdp:
    description:
      -  BIOS Token for setting Config TDP configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  config_tdp_level:
    description:
      -  BIOS Token for setting Configurable TDP Level configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Level 1 - Value - Level 1 for configuring config_tdp_level token.
      -  Level 2 - Value - Level 2 for configuring config_tdp_level token.
      -  Normal - Value - Normal for configuring config_tdp_level token.
    choices: ['platform-default' , 'Level 1' , 'Level 2' , 'Normal']
    type: str
  console_redirection:
    description:
      -  BIOS Token for setting Console Redirection configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  com-0 - Value - com-0 for configuring console_redirection token.
      -  com-1 - Value - com-1 for configuring console_redirection token.
      -  disabled - Value - disabled for configuring console_redirection token.
      -  enabled - Value - enabled for configuring console_redirection token.
      -  serial-port-a - Value - serial-port-a for configuring console_redirection token.
    choices: ['platform-default' , 'com-0' , 'com-1' , 'disabled' , 'enabled' , 'serial-port-a']
    type: str
  core_multi_processing:
    description:
      -  BIOS Token for setting Core Multi Processing configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1 - Value - 1 for configuring core_multi_processing token.
      -  2 - Value - 2 for configuring core_multi_processing token.
      -  3 - Value - 3 for configuring core_multi_processing token.
      -  4 - Value - 4 for configuring core_multi_processing token.
      -  5 - Value - 5 for configuring core_multi_processing token.
      -  6 - Value - 6 for configuring core_multi_processing token.
      -  7 - Value - 7 for configuring core_multi_processing token.
      -  8 - Value - 8 for configuring core_multi_processing token.
      -  9 - Value - 9 for configuring core_multi_processing token.
      -  10 - Value - 10 for configuring core_multi_processing token.
      -  11 - Value - 11 for configuring core_multi_processing token.
      -  12 - Value - 12 for configuring core_multi_processing token.
      -  13 - Value - 13 for configuring core_multi_processing token.
      -  14 - Value - 14 for configuring core_multi_processing token.
      -  15 - Value - 15 for configuring core_multi_processing token.
      -  16 - Value - 16 for configuring core_multi_processing token.
      -  17 - Value - 17 for configuring core_multi_processing token.
      -  18 - Value - 18 for configuring core_multi_processing token.
      -  19 - Value - 19 for configuring core_multi_processing token.
      -  20 - Value - 20 for configuring core_multi_processing token.
      -  21 - Value - 21 for configuring core_multi_processing token.
      -  22 - Value - 22 for configuring core_multi_processing token.
      -  23 - Value - 23 for configuring core_multi_processing token.
      -  24 - Value - 24 for configuring core_multi_processing token.
      -  25 - Value - 25 for configuring core_multi_processing token.
      -  26 - Value - 26 for configuring core_multi_processing token.
      -  27 - Value - 27 for configuring core_multi_processing token.
      -  28 - Value - 28 for configuring core_multi_processing token.
      -  29 - Value - 29 for configuring core_multi_processing token.
      -  30 - Value - 30 for configuring core_multi_processing token.
      -  31 - Value - 31 for configuring core_multi_processing token.
      -  32 - Value - 32 for configuring core_multi_processing token.
      -  33 - Value - 33 for configuring core_multi_processing token.
      -  34 - Value - 34 for configuring core_multi_processing token.
      -  35 - Value - 35 for configuring core_multi_processing token.
      -  36 - Value - 36 for configuring core_multi_processing token.
      -  37 - Value - 37 for configuring core_multi_processing token.
      -  38 - Value - 38 for configuring core_multi_processing token.
      -  39 - Value - 39 for configuring core_multi_processing token.
      -  40 - Value - 40 for configuring core_multi_processing token.
      -  41 - Value - 41 for configuring core_multi_processing token.
      -  42 - Value - 42 for configuring core_multi_processing token.
      -  43 - Value - 43 for configuring core_multi_processing token.
      -  44 - Value - 44 for configuring core_multi_processing token.
      -  45 - Value - 45 for configuring core_multi_processing token.
      -  46 - Value - 46 for configuring core_multi_processing token.
      -  47 - Value - 47 for configuring core_multi_processing token.
      -  48 - Value - 48 for configuring core_multi_processing token.
      -  49 - Value - 49 for configuring core_multi_processing token.
      -  50 - Value - 50 for configuring core_multi_processing token.
      -  51 - Value - 51 for configuring core_multi_processing token.
      -  52 - Value - 52 for configuring core_multi_processing token.
      -  53 - Value - 53 for configuring core_multi_processing token.
      -  54 - Value - 54 for configuring core_multi_processing token.
      -  55 - Value - 55 for configuring core_multi_processing token.
      -  56 - Value - 56 for configuring core_multi_processing token.
      -  57 - Value - 57 for configuring core_multi_processing token.
      -  58 - Value - 58 for configuring core_multi_processing token.
      -  59 - Value - 59 for configuring core_multi_processing token.
      -  60 - Value - 60 for configuring core_multi_processing token.
      -  61 - Value - 61 for configuring core_multi_processing token.
      -  62 - Value - 62 for configuring core_multi_processing token.
      -  63 - Value - 63 for configuring core_multi_processing token.
      -  64 - Value - 64 for configuring core_multi_processing token.
      -  all - Value - all for configuring core_multi_processing token.
    choices: ['platform-default' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '10' , '11' , '12' , '13' , '14' , '15' , '16' , '17' , '18',
              '19' , '20' , '21' , '22' , '23' , '24' , '25' , '26' , '27' , '28' , '29' , '30' , '31' , '32' , '33' , '34' , '35' , '36' , '37',
              '38' , '39' , '40' , '41' , '42' , '43' , '44' , '45' , '46' , '47' , '48' , '49' , '50' , '51' , '52' , '53' , '54' , '55' , '56' , '57',
              '58' , '59' , '60' , '61' , '62' , '63' , '64' , 'all']
    type: str
  cpu_energy_performance:
    description:
      -  BIOS Token for setting Energy Performance configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  balanced-energy - Value - balanced-energy for configuring cpu_energy_performance token.
      -  balanced-performance - Value - balanced-performance for configuring cpu_energy_performance token.
      -  balanced-power - Value - balanced-power for configuring cpu_energy_performance token.
      -  energy-efficient - Value - energy-efficient for configuring cpu_energy_performance token.
      -  performance - Value - performance for configuring cpu_energy_performance token.
      -  power - Value - power for configuring cpu_energy_performance token.
    choices: ['platform-default' , 'balanced-energy' , 'balanced-performance' , 'balanced-power' , 'energy-efficient' , 'performance' , 'power']
    type: str
  cpu_frequency_floor:
    description:
      -  BIOS Token for setting Frequency Floor Override configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cpu_pa_limit:
    description:
      -  BIOS Token for setting Limit CPU PA to 46 Bits configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  cpu_perf_enhancement:
    description:
      -  BIOS Token for setting Enhanced CPU Performance configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring cpu_perf_enhancement token.
      -  Disabled - Value - Disabled for configuring cpu_perf_enhancement token.
    choices: ['platform-default' , 'Auto' , 'Disabled']
    type: str
  cpu_performance:
    description:
      -  BIOS Token for setting CPU Performance configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  custom - Value - custom for configuring cpu_performance token.
      -  enterprise - Value - enterprise for configuring cpu_performance token.
      -  high-throughput - Value - high-throughput for configuring cpu_performance token.
      -  hpc - Value - hpc for configuring cpu_performance token.
    choices: ['platform-default' , 'custom' , 'enterprise' , 'high-throughput' , 'hpc']
    type: str
  cpu_power_management:
    description:
      -  BIOS Token for setting Power Technology configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  custom - Value - custom for configuring cpu_power_management token.
      -  disabled - Value - disabled for configuring cpu_power_management token.
      -  energy-efficient - Value - energy-efficient for configuring cpu_power_management token.
      -  performance - Value - performance for configuring cpu_power_management token.
    choices: ['platform-default' , 'custom' , 'disabled' , 'energy-efficient' , 'performance']
    type: str
  crfastgo_config:
    description:
      -  BIOS Token for setting CR FastGo Config configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring crfastgo_config token.
      -  Default - Value - Default for configuring crfastgo_config token.
      -  Disable optimization - Value - Disable optimization for configuring crfastgo_config token.
      -  Enable optimization - Value - Enable optimization for configuring crfastgo_config token.
      -  Option 1 - Value - Option 1 for configuring crfastgo_config token.
      -  Option 2 - Value - Option 2 for configuring crfastgo_config token.
      -  Option 3 - Value - Option 3 for configuring crfastgo_config token.
      -  Option 4 - Value - Option 4 for configuring crfastgo_config token.
      -  Option 5 - Value - Option 5 for configuring crfastgo_config token.
    choices: ['platform-default' , 'Auto' , 'Default' , 'Disable optimization' , 'Enable optimization' , 'Option 1' , 'Option 2' , 'Option 3',
              'Option 4' , 'Option 5']
    type: str
  cr_qos:
    description:
      -  BIOS Token for setting CR QoS configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Disabled - Value - Disabled for configuring cr_qos token.
      -  Mode 0 - Disable the PMem QoS Feature - Value - Mode 0 - Disable the PMem QoS Feature for configuring cr_qos token.
      -  Mode 1 - M2M QoS Enable and CHA QoS Disable - Value - Mode 1 - M2M QoS Enable and CHA QoS Disable for configuring cr_qos token.
      -  Mode 2 - M2M QoS Enable and CHA QoS Enable - Value - Mode 2 - M2M QoS Enable and CHA QoS Enable for configuring cr_qos token.
      -  Profile 1 - Value - Profile 1 for configuring cr_qos token.
      -  Recipe 1 - Value - Recipe 1 for configuring cr_qos token.
      -  Recipe 2 - Value - Recipe 2 for configuring cr_qos token.
      -  Recipe 3 - Value - Recipe 3 for configuring cr_qos token.
    choices: ['platform-default' , 'Disabled' , 'Mode 0 - Disable the PMem QoS Feature' , 'Mode 1 - M2M QoS Enable and CHA QoS Disable' ,
              'Mode 2 - M2M QoS Enable and CHA QoS Enable' , 'Profile 1' , 'Recipe 1' , 'Recipe 2' , 'Recipe 3']
    type: str
  dcpmm_firmware_downgrade:
    description:
      -  BIOS Token for setting DCPMM Firmware Downgrade configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  demand_scrub:
    description:
      -  BIOS Token for setting Demand Scrub configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  direct_cache_access:
    description:
      -  BIOS Token for setting Direct Cache Access Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  auto - Value - auto for configuring direct_cache_access token.
      -  disabled - Value - disabled for configuring direct_cache_access token.
      -  enabled - Value - enabled for configuring direct_cache_access token.
    choices: ['platform-default' , 'auto' , 'disabled' , 'enabled']
    type: str
  dma_ctrl_opt_in:
    description:
      -  BIOS Token for setting DMA Control Opt-In Flag configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  dram_clock_throttling:
    description:
      -  BIOS Token for setting DRAM Clock Throttling configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring dram_clock_throttling token.
      -  Balanced - Value - Balanced for configuring dram_clock_throttling token.
      -  Energy Efficient - Value - Energy Efficient for configuring dram_clock_throttling token.
      -  Performance - Value - Performance for configuring dram_clock_throttling token.
    choices: ['platform-default' , 'Auto' , 'Balanced' , 'Energy Efficient' , 'Performance']
    type: str
  dram_refresh_rate:
    description:
      -  BIOS Token for setting DRAM Refresh Rate configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1x - Value - 1x for configuring dram_refresh_rate token.
      -  2x - Value - 2x for configuring dram_refresh_rate token.
      -  3x - Value - 3x for configuring dram_refresh_rate token.
      -  4x - Value - 4x for configuring dram_refresh_rate token.
      -  Auto - Value - Auto for configuring dram_refresh_rate token.
    choices: ['platform-default' , '1x' , '2x' , '3x' , '4x' , 'Auto']
    type: str
  dram_sw_thermal_throttling:
    description:
      -  BIOS Token for setting DRAM SW Thermal Throttling configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  eadr_support:
    description:
      -  BIOS Token for setting eADR Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring eadr_support token.
      -  disabled - Value - disabled for configuring eadr_support token.
      -  enabled - Value - enabled for configuring eadr_support token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  edpc_en:
    description:
      -  BIOS Token for setting IIO eDPC Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Disabled - Value - Disabled for configuring edpc_en token.
      -  On Fatal Error - Value - On Fatal Error for configuring edpc_en token.
      -  On Fatal and Non-Fatal Errors - Value - On Fatal and Non-Fatal Errors for configuring edpc_en token.
    choices: ['platform-default' , 'Disabled' , 'On Fatal Error' , 'On Fatal and Non-Fatal Errors']
    type: str
  enable_clock_spread_spec:
    description:
      -  BIOS Token for setting External SSC Enable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  0P3_Percent - Value - 0P3_Percent for configuring enable_clock_spread_spec token.
      -  0P5_Percent - Value - 0P5_Percent for configuring enable_clock_spread_spec token.
      -  disabled - Value - disabled for configuring enable_clock_spread_spec token.
      -  enabled - Value - enabled for configuring enable_clock_spread_spec token.
      -  Hardware - Value - Hardware for configuring enable_clock_spread_spec token.
      -  Off - Value - Off for configuring enable_clock_spread_spec token.
    choices: ['platform-default' , '0P3_Percent' , '0P5_Percent' , 'disabled' , 'enabled' , 'Hardware' , 'Off']
    type: str
  enable_mktme:
    description:
      -  BIOS Token for setting Multikey Total Memory Encryption  (MK-TME) configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  enable_rmt:
    description:
      -  BIOS Token for setting Rank Margin Tool configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  enable_sgx:
    description:
      -  BIOS Token for setting Software Guard Extensions  (SGX) configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  enable_tme:
    description:
      -  BIOS Token for setting Total Memory Encryption  (TME) configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  energy_efficient_turbo:
    description:
      -  BIOS Token for setting Energy Efficient Turbo configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  eng_perf_tuning:
    description:
      -  BIOS Token for setting Energy Performance Tuning configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  BIOS - Value - BIOS for configuring eng_perf_tuning token.
      -  OS - Value - OS for configuring eng_perf_tuning token.
    choices: ['platform-default' , 'BIOS' , 'OS']
    type: str
  enhanced_intel_speed_step_tech:
    description:
      -  BIOS Token for setting Enhanced Intel Speedstep (R) Technology configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  epoch_update:
    description:
      -  BIOS Token for setting Select Owner EPOCH Input Type configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Change to New Random Owner EPOCHs - Value - Change to New Random Owner EPOCHs for configuring epoch_update token.
      -  Manual User Defined Owner EPOCHs - Value - Manual User Defined Owner EPOCHs for configuring epoch_update token.
      -  SGX Owner EPOCH activated - Value - SGX Owner EPOCH activated for configuring epoch_update token.
    choices: ['platform-default' , 'Change to New Random Owner EPOCHs' , 'Manual User Defined Owner EPOCHs' , 'SGX Owner EPOCH activated']
    type: str
  epp_enable:
    description:
      -  BIOS Token for setting Processor EPP Enable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  epp_profile:
    description:
      -  BIOS Token for setting EPP Profile configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Balanced Performance - Value - Balanced Performance for configuring epp_profile token.
      -  Balanced Power - Value - Balanced Power for configuring epp_profile token.
      -  Performance - Value - Performance for configuring epp_profile token.
      -  Power - Value - Power for configuring epp_profile token.
    choices: ['platform-default' , 'Balanced Performance' , 'Balanced Power' , 'Performance' , 'Power']
    type: str
  error_check_scrub:
    description:
      -  BIOS Token for setting Error Check Scrub configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Disabled - Value - Disabled for configuring error_check_scrub token.
      -  Enabled with Result Collection - Value - Enabled with Result Collection for configuring error_check_scrub token.
      -  Enabled without Result Collection - Value - Enabled without Result Collection for configuring error_check_scrub token.
    choices: ['platform-default' , 'Disabled' , 'Enabled with Result Collection' , 'Enabled without Result Collection']
    type: str
  execute_disable_bit:
    description:
      -  BIOS Token for setting Execute Disable Bit configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  extended_apic:
    description:
      -  BIOS Token for setting Local X2 Apic configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring extended_apic token.
      -  enabled - Value - enabled for configuring extended_apic token.
      -  X2APIC - Value - X2APIC for configuring extended_apic token.
      -  XAPIC - Value - XAPIC for configuring extended_apic token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'X2APIC' , 'XAPIC']
    type: str
  flow_control:
    description:
      -  BIOS Token for setting Flow Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  none - Value - none for configuring flow_control token.
      -  rts-cts - Value - rts-cts for configuring flow_control token.
    choices: ['platform-default' , 'none' , 'rts-cts']
    type: str
  frb2enable:
    description:
      -  BIOS Token for setting FRB-2 Timer configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  hardware_prefetch:
    description:
      -  BIOS Token for setting Hardware Prefetcher configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  hwpm_enable:
    description:
      -  BIOS Token for setting CPU Hardware Power Management configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Disabled - Value - Disabled for configuring hwpm_enable token.
      -  HWPM Native Mode - Value - HWPM Native Mode for configuring hwpm_enable token.
      -  HWPM OOB Mode - Value - HWPM OOB Mode for configuring hwpm_enable token.
      -  NATIVE MODE - Value - NATIVE MODE for configuring hwpm_enable token.
      -  Native Mode with no Legacy - Value - Native Mode with no Legacy for configuring hwpm_enable token.
      -  OOB MODE - Value - OOB MODE for configuring hwpm_enable token.
    choices: ['platform-default' , 'Disabled' , 'HWPM Native Mode' , 'HWPM OOB Mode' , 'NATIVE MODE' , 'Native Mode with no Legacy' , 'OOB MODE']
    type: str
  imc_interleave:
    description:
      -  BIOS Token for setting IMC Interleaving configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1-way Interleave - Value - 1-way Interleave for configuring imc_interleave token.
      -  2-way Interleave - Value - 2-way Interleave for configuring imc_interleave token.
      -  Auto - Value - Auto for configuring imc_interleave token.
    choices: ['platform-default' , '1-way Interleave' , '2-way Interleave' , 'Auto']
    type: str
  intel_dynamic_speed_select:
    description:
      -  BIOS Token for setting Intel Dynamic Speed Select configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_hyper_threading_tech:
    description:
      -  BIOS Token for setting Intel HyperThreading Tech configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_speed_select:
    description:
      -  BIOS Token for setting Intel Speed Select configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring intel_speed_select token.
      -  Base - Value - Base for configuring intel_speed_select token.
      -  Config 1 - Value - Config 1 for configuring intel_speed_select token.
      -  Config 2 - Value - Config 2 for configuring intel_speed_select token.
      -  Config 3 - Value - Config 3 for configuring intel_speed_select token.
      -  Config 4 - Value - Config 4 for configuring intel_speed_select token.
    choices: ['platform-default' , 'Auto' , 'Base' , 'Config 1' , 'Config 2' , 'Config 3' , 'Config 4']
    type: str
  intel_turbo_boost_tech:
    description:
      -  BIOS Token for setting Intel Turbo Boost Tech configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_virtualization_technology:
    description:
      -  BIOS Token for setting Intel (R) VT configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_vtdats_support:
    description:
      -  BIOS Token for setting Intel VTD ATS Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_vtd_coherency_support:
    description:
      -  BIOS Token for setting Intel (R) VT-d Coherency Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_vtd_interrupt_remapping:
    description:
      -  BIOS Token for setting Intel (R) VT-d Interrupt Remapping configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_vtd_pass_through_dma_support:
    description:
      -  BIOS Token for setting Intel (R) VT-d PassThrough DMA Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  intel_vt_for_directed_io:
    description:
      -  BIOS Token for setting Intel VT for Directed IO configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  ioh_error_enable:
    description:
      -  BIOS Token for setting IIO Error Enable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  No - Value - No for configuring ioh_error_enable token.
      -  Yes - Value - Yes for configuring ioh_error_enable token.
    choices: ['platform-default' , 'No' , 'Yes']
    type: str
  ioh_resource:
    description:
      -  BIOS Token for setting IOH Resource Allocation configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  IOH0 24k IOH1 40k - Value - IOH0 24k IOH1 40k for configuring ioh_resource token.
      -  IOH0 32k IOH1 32k - Value - IOH0 32k IOH1 32k for configuring ioh_resource token.
      -  IOH0 40k IOH1 24k - Value - IOH0 40k IOH1 24k for configuring ioh_resource token.
      -  IOH0 48k IOH1 16k - Value - IOH0 48k IOH1 16k for configuring ioh_resource token.
      -  IOH0 56k IOH1 8k - Value - IOH0 56k IOH1 8k for configuring ioh_resource token.
    choices: ['platform-default' , 'IOH0 24k IOH1 40k' , 'IOH0 32k IOH1 32k' , 'IOH0 40k IOH1 24k' , 'IOH0 48k IOH1 16k' , 'IOH0 56k IOH1 8k']
    type: str
  ip_prefetch:
    description:
      -  BIOS Token for setting DCU IP Prefetcher configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  ipv4http:
    description:
      -  BIOS Token for setting IPV4 HTTP Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  ipv4pxe:
    description:
      -  BIOS Token for setting IPv4 PXE Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  ipv6http:
    description:
      -  BIOS Token for setting IPV6 HTTP Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  ipv6pxe:
    description:
      -  BIOS Token for setting IPV6 PXE Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  kti_prefetch:
    description:
      -  BIOS Token for setting KTI Prefetch configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring kti_prefetch token.
      -  disabled - Value - disabled for configuring kti_prefetch token.
      -  enabled - Value - enabled for configuring kti_prefetch token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  legacy_os_redirection:
    description:
      -  BIOS Token for setting Legacy OS Redirection configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  legacy_usb_support:
    description:
      -  BIOS Token for setting Legacy USB Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  auto - Value - auto for configuring legacy_usb_support token.
      -  disabled - Value - disabled for configuring legacy_usb_support token.
      -  enabled - Value - enabled for configuring legacy_usb_support token.
    choices: ['platform-default' , 'auto' , 'disabled' , 'enabled']
    type: str
  llc_alloc:
    description:
      -  BIOS Token for setting LLC Dead Line configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring llc_alloc token.
      -  disabled - Value - disabled for configuring llc_alloc token.
      -  enabled - Value - enabled for configuring llc_alloc token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  llc_prefetch:
    description:
      -  BIOS Token for setting LLC Prefetch configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  lom_port0state:
    description:
      -  BIOS Token for setting LOM Port 0 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring lom_port0state token.
      -  enabled - Value - enabled for configuring lom_port0state token.
      -  Legacy Only - Value - Legacy Only for configuring lom_port0state token.
      -  UEFI Only - Value - UEFI Only for configuring lom_port0state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  lom_port1state:
    description:
      -  BIOS Token for setting LOM Port 1 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring lom_port1state token.
      -  enabled - Value - enabled for configuring lom_port1state token.
      -  Legacy Only - Value - Legacy Only for configuring lom_port1state token.
      -  UEFI Only - Value - UEFI Only for configuring lom_port1state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  lom_port2state:
    description:
      -  BIOS Token for setting LOM Port 2 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring lom_port2state token.
      -  enabled - Value - enabled for configuring lom_port2state token.
      -  Legacy Only - Value - Legacy Only for configuring lom_port2state token.
      -  UEFI Only - Value - UEFI Only for configuring lom_port2state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  lom_port3state:
    description:
      -  BIOS Token for setting LOM Port 3 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring lom_port3state token.
      -  enabled - Value - enabled for configuring lom_port3state token.
      -  Legacy Only - Value - Legacy Only for configuring lom_port3state token.
      -  UEFI Only - Value - UEFI Only for configuring lom_port3state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  lom_ports_all_state:
    description:
      -  BIOS Token for setting All Onboard LOM Ports configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  lv_ddr_mode:
    description:
      -  BIOS Token for setting Low Voltage DDR Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  auto - Value - auto for configuring lv_ddr_mode token.
      -  performance-mode - Value - performance-mode for configuring lv_ddr_mode token.
      -  power-saving-mode - Value - power-saving-mode for configuring lv_ddr_mode token.
    choices: ['platform-default' , 'auto' , 'performance-mode' , 'power-saving-mode']
    type: str
  make_device_non_bootable:
    description:
      -  BIOS Token for setting Make Device Non Bootable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  memory_bandwidth_boost:
    description:
      -  BIOS Token for setting Memory Bandwidth Boost configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  memory_inter_leave:
    description:
      -  BIOS Token for setting Intel Memory Interleaving configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1 Way Node Interleave - Value - 1 Way Node Interleave for configuring memory_inter_leave token.
      -  2 Way Node Interleave - Value - 2 Way Node Interleave for configuring memory_inter_leave token.
      -  4 Way Node Interleave - Value - 4 Way Node Interleave for configuring memory_inter_leave token.
      -  8 Way Node Interleave - Value - 8 Way Node Interleave for configuring memory_inter_leave token.
      -  disabled - Value - disabled for configuring memory_inter_leave token.
      -  enabled - Value - enabled for configuring memory_inter_leave token.
    choices: ['platform-default' , '1 Way Node Interleave' , '2 Way Node Interleave' , '4 Way Node Interleave' , '8 Way Node Interleave' ,
              'disabled' , 'enabled']
    type: str
  memory_mapped_io_above4gb:
    description:
      -  BIOS Token for setting Memory Mapped IO above 4GiB configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  memory_refresh_rate:
    description:
      -  BIOS Token for setting Memory Refresh Rate configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1x Refresh - Value - 1x Refresh for configuring memory_refresh_rate token.
      -  2x Refresh - Value - 2x Refresh for configuring memory_refresh_rate token.
    choices: ['platform-default' , '1x Refresh' , '2x Refresh']
    type: str
  memory_size_limit:
    description:
      -  BIOS Token for setting Memory Size Limit in GiB configuration (0 - 65535 GiB).
    type: str
  memory_thermal_throttling:
    description:
      -  BIOS Token for setting Memory Thermal Throttling Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  CLTT with PECI - Value - CLTT with PECI for configuring memory_thermal_throttling token.
      -  Disabled - Value - Disabled for configuring memory_thermal_throttling token.
    choices: ['platform-default' , 'CLTT with PECI' , 'Disabled']
    type: str
  mirroring_mode:
    description:
      -  BIOS Token for setting Mirroring Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  inter-socket - Value - inter-socket for configuring mirroring_mode token.
      -  intra-socket - Value - intra-socket for configuring mirroring_mode token.
    choices: ['platform-default' , 'inter-socket' , 'intra-socket']
    type: str
  mmcfg_base:
    description:
      -  BIOS Token for setting MMCFG BASE configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1 GB - Value - 1 GiB for configuring mmcfg_base token.
      -  2 GB - Value - 2 GiB for configuring mmcfg_base token.
      -  2.5 GB - Value - 2.5 GiB for configuring mmcfg_base token.
      -  3 GB - Value - 3 GiB for configuring mmcfg_base token.
      -  Auto - Value - Auto for configuring mmcfg_base token.
    choices: ['platform-default' , '1 GB' , '2 GB' , '2.5 GB' , '3 GB' , 'Auto']
    type: str
  network_stack:
    description:
      -  BIOS Token for setting Network Stack configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  numa_optimized:
    description:
      -  BIOS Token for setting NUMA Optimized configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  nvmdimm_perform_config:
    description:
      -  BIOS Token for setting NVM Performance Setting configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  BW Optimized - Value - BW Optimized for configuring nvmdimm_perform_config token.
      -  Balanced Profile - Value - Balanced Profile for configuring nvmdimm_perform_config token.
      -  Latency Optimized - Value - Latency Optimized for configuring nvmdimm_perform_config token.
    choices: ['platform-default' , 'BW Optimized' , 'Balanced Profile' , 'Latency Optimized']
    type: str
  onboard10gbit_lom:
    description:
      -  BIOS Token for setting Onboard 10Gbit LOM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  onboard_gbit_lom:
    description:
      -  BIOS Token for setting Onboard Gbit LOM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  onboard_scu_storage_support:
    description:
      -  BIOS Token for setting Onboard SCU Storage Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  onboard_scu_storage_sw_stack:
    description:
      -  BIOS Token for setting Onboard SCU Storage SW Stack configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Intel RSTe - Value - Intel RSTe for configuring onboard_scu_storage_sw_stack token.
      -  LSI SW RAID - Value - LSI SW RAID for configuring onboard_scu_storage_sw_stack token.
    choices: ['platform-default' , 'Intel RSTe' , 'LSI SW RAID']
    type: str
  operation_mode:
    description:
      -  BIOS Token for setting Operation Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Test Only - Value - Test Only for configuring operation_mode token.
      -  Test and Repair - Value - Test and Repair for configuring operation_mode token.
    choices: ['platform-default' , 'Test Only' , 'Test and Repair']
    type: str
  os_boot_watchdog_timer:
    description:
      -  BIOS Token for setting OS Boot Watchdog Timer configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  os_boot_watchdog_timer_policy:
    description:
      -  BIOS Token for setting OS Boot Watchdog Timer Policy configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  do-nothing - Value - do-nothing for configuring os_boot_watchdog_timer_policy token.
      -  power-off - Value - power-off for configuring os_boot_watchdog_timer_policy token.
      -  reset - Value - reset for configuring os_boot_watchdog_timer_policy token.
    choices: ['platform-default' , 'do-nothing' , 'power-off' , 'reset']
    type: str
  os_boot_watchdog_timer_timeout:
    description:
      -  BIOS Token for setting OS Boot Watchdog Timer Timeout configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  5-minutes - Value - 5-minutes for configuring os_boot_watchdog_timer_timeout token.
      -  10-minutes - Value - 10-minutes for configuring os_boot_watchdog_timer_timeout token.
      -  15-minutes - Value - 15-minutes for configuring os_boot_watchdog_timer_timeout token.
      -  20-minutes - Value - 20-minutes for configuring os_boot_watchdog_timer_timeout token.
    choices: ['platform-default' , '5-minutes' , '10-minutes' , '15-minutes' , '20-minutes']
    type: str
  out_of_band_mgmt_port:
    description:
      -  BIOS Token for setting Out-of-Band Mgmt Port configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  package_cstate_limit:
    description:
      -  BIOS Token for setting Package C State Limit configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring package_cstate_limit token.
      -  C0 C1 State - Value - C0 C1 State for configuring package_cstate_limit token.
      -  C0/C1 - Value - C0/C1 for configuring package_cstate_limit token.
      -  C2 - Value - C2 for configuring package_cstate_limit token.
      -  C6 Non Retention - Value - C6 Non Retention for configuring package_cstate_limit token.
      -  C6 Retention - Value - C6 Retention for configuring package_cstate_limit token.
      -  No Limit - Value - No Limit for configuring package_cstate_limit token.
    choices: ['platform-default' , 'Auto' , 'C0 C1 State' , 'C0/C1' , 'C2' , 'C6 Non Retention' , 'C6 Retention' , 'No Limit']
    type: str
  panic_high_watermark:
    description:
      -  BIOS Token for setting Panic and High Watermark configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  High - Value - High for configuring panic_high_watermark token.
      -  Low - Value - Low for configuring panic_high_watermark token.
    choices: ['platform-default' , 'High' , 'Low']
    type: str
  partial_cache_line_sparing:
    description:
      -  BIOS Token for setting Partial Cache Line Sparing configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  partial_mirror_mode_config:
    description:
      -  BIOS Token for setting Partial Memory Mirror Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring partial_mirror_mode_config token.
      -  Percentage - Value - Percentage for configuring partial_mirror_mode_config token.
      -  Value in GB - Value - Value in GiB for configuring partial_mirror_mode_config token.
    choices: ['platform-default' , 'disabled' , 'Percentage' , 'Value in GB']
    type: str
  partial_mirror_percent:
    description:
      -  BIOS Token for setting Partial Mirror Percentage configuration (0.00 - 50.00 Percentage).
    type: str
  partial_mirror_value1:
    description:
      -  BIOS Token for setting Partial Mirror1 Size in GiB configuration (0 - 65535 GiB).
    type: str
  partial_mirror_value2:
    description:
      -  BIOS Token for setting Partial Mirror2 Size in GiB configuration (0 - 65535 GiB).
    type: str
  partial_mirror_value3:
    description:
      -  BIOS Token for setting Partial Mirror3 Size in GiB configuration (0 - 65535 GiB).
    type: str
  partial_mirror_value4:
    description:
      -  BIOS Token for setting Partial Mirror4 Size in GiB configuration (0 - 65535 GiB).
    type: str
  patrol_scrub:
    description:
      -  BIOS Token for setting Patrol Scrub configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring patrol_scrub token.
      -  Enable at End of POST - Value - Enable at End of POST for configuring patrol_scrub token.
      -  enabled - Value - enabled for configuring patrol_scrub token.
    choices: ['platform-default' , 'disabled' , 'Enable at End of POST' , 'enabled']
    type: str
  patrol_scrub_duration:
    description:
      -  BIOS Token for setting Patrol Scrub Interval configuration (5 - 23 Hour).
    type: str
  pch_pcie_pll_ssc:
    description:
      -  BIOS Token for setting PCIe PLL SSC Percent configuration (0 - 255 (n/10)%).
    type: str
  pch_usb30mode:
    description:
      -  BIOS Token for setting xHCI Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_ari_support:
    description:
      -  BIOS Token for setting PCIe ARI Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_ari_support token.
      -  disabled - Value - disabled for configuring pcie_ari_support token.
      -  enabled - Value - enabled for configuring pcie_ari_support token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  pcie_pll_ssc:
    description:
      -  BIOS Token for setting PCIe PLL SSC configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_pll_ssc token.
      -  Disabled - Value - Disabled for configuring pcie_pll_ssc token.
      -  ZeroPointFive - Value - ZeroPointFive for configuring pcie_pll_ssc token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'ZeroPointFive']
    type: str
  pc_ie_ras_support:
    description:
      -  BIOS Token for setting PCIe RAS Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_mraid1link_speed:
    description:
      -  BIOS Token for setting MRAID1 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_mraid1link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_mraid1link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_mraid1link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_mraid1link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_mraid1link_speed token.
      -  GEN4 - Value - GEN4 for configuring pcie_slot_mraid1link_speed token.
      -  GEN5 - Value - GEN5 for configuring pcie_slot_mraid1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  pcie_slot_mraid1option_rom:
    description:
      -  BIOS Token for setting MRAID1 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_mraid2link_speed:
    description:
      -  BIOS Token for setting MRAID2 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_mraid2link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_mraid2link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_mraid2link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_mraid2link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_mraid2link_speed token.
      -  GEN4 - Value - GEN4 for configuring pcie_slot_mraid2link_speed token.
      -  GEN5 - Value - GEN5 for configuring pcie_slot_mraid2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  pcie_slot_mraid2option_rom:
    description:
      -  BIOS Token for setting MRAID2 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_mstorraid_link_speed:
    description:
      -  BIOS Token for setting PCIe Slot MSTOR Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_mstorraid_link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_mstorraid_link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_mstorraid_link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_mstorraid_link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_mstorraid_link_speed token.
      -  GEN4 - Value - GEN4 for configuring pcie_slot_mstorraid_link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4']
    type: str
  pcie_slot_mstorraid_option_rom:
    description:
      -  BIOS Token for setting PCIe Slot MSTOR RAID OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_nvme1link_speed:
    description:
      -  BIOS Token for setting NVME 1 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_nvme1link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_nvme1link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_nvme1link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_nvme1link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_nvme1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  pcie_slot_nvme1option_rom:
    description:
      -  BIOS Token for setting NVME 1 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_nvme2link_speed:
    description:
      -  BIOS Token for setting NVME 2 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_nvme2link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_nvme2link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_nvme2link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_nvme2link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_nvme2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  pcie_slot_nvme2option_rom:
    description:
      -  BIOS Token for setting NVME 2 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_nvme3link_speed:
    description:
      -  BIOS Token for setting NVME 3 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_nvme3link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_nvme3link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_nvme3link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_nvme3link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_nvme3link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  pcie_slot_nvme3option_rom:
    description:
      -  BIOS Token for setting NVME 3 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_nvme4link_speed:
    description:
      -  BIOS Token for setting NVME 4 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_nvme4link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_nvme4link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_nvme4link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_nvme4link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_nvme4link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  pcie_slot_nvme4option_rom:
    description:
      -  BIOS Token for setting NVME 4 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_nvme5link_speed:
    description:
      -  BIOS Token for setting NVME 5 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_nvme5link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_nvme5link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_nvme5link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_nvme5link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_nvme5link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  pcie_slot_nvme5option_rom:
    description:
      -  BIOS Token for setting NVME 5 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slot_nvme6link_speed:
    description:
      -  BIOS Token for setting NVME 6 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring pcie_slot_nvme6link_speed token.
      -  Disabled - Value - Disabled for configuring pcie_slot_nvme6link_speed token.
      -  GEN1 - Value - GEN1 for configuring pcie_slot_nvme6link_speed token.
      -  GEN2 - Value - GEN2 for configuring pcie_slot_nvme6link_speed token.
      -  GEN3 - Value - GEN3 for configuring pcie_slot_nvme6link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  pcie_slot_nvme6option_rom:
    description:
      -  BIOS Token for setting NVME 6 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pcie_slots_cdn_enable:
    description:
      -  BIOS Token for setting PCIe Slots CDN Control configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pc_ie_ssd_hot_plug_support:
    description:
      -  BIOS Token for setting NVMe SSD Hot-Plug Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pci_option_ro_ms:
    description:
      -  BIOS Token for setting All PCIe Slots OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring pci_option_ro_ms token.
      -  enabled - Value - enabled for configuring pci_option_ro_ms token.
      -  Legacy Only - Value - Legacy Only for configuring pci_option_ro_ms token.
      -  UEFI Only - Value - UEFI Only for configuring pci_option_ro_ms token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  pci_rom_clp:
    description:
      -  BIOS Token for setting PCI ROM CLP configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  pop_support:
    description:
      -  BIOS Token for setting Power ON Password configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  post_error_pause:
    description:
      -  BIOS Token for setting POST Error Pause configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  post_package_repair:
    description:
      -  BIOS Token for setting Post Package Repair configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Disabled - Value - Disabled for configuring post_package_repair token.
      -  Hard PPR - Value - Hard PPR for configuring post_package_repair token.
    choices: ['platform-default' , 'Disabled' , 'Hard PPR']
    type: str
  processor_c1e:
    description:
      -  BIOS Token for setting Processor C1E configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  processor_c3report:
    description:
      -  BIOS Token for setting Processor C3 Report configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  processor_c6report:
    description:
      -  BIOS Token for setting Processor C6 Report configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  processor_cstate:
    description:
      -  BIOS Token for setting CPU C State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  psata:
    description:
      -  BIOS Token for setting P-SATA Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  AHCI - Value - AHCI for configuring psata token.
      -  Disabled - Value - Disabled for configuring psata token.
      -  LSI SW RAID - Value - LSI SW RAID for configuring psata token.
    choices: ['platform-default' , 'AHCI' , 'Disabled' , 'LSI SW RAID']
    type: str
  pstate_coord_type:
    description:
      -  BIOS Token for setting P-STATE Coordination configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  HW ALL - Value - HW ALL for configuring pstate_coord_type token.
      -  SW ALL - Value - SW ALL for configuring pstate_coord_type token.
      -  SW ANY - Value - SW ANY for configuring pstate_coord_type token.
    choices: ['platform-default' , 'HW ALL' , 'SW ALL' , 'SW ANY']
    type: str
  putty_key_pad:
    description:
      -  BIOS Token for setting Putty KeyPad configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  ESCN - Value - ESCN for configuring putty_key_pad token.
      -  LINUX - Value - LINUX for configuring putty_key_pad token.
      -  SCO - Value - SCO for configuring putty_key_pad token.
      -  VT100 - Value - VT100 for configuring putty_key_pad token.
      -  VT400 - Value - VT400 for configuring putty_key_pad token.
      -  XTERMR6 - Value - XTERMR6 for configuring putty_key_pad token.
    choices: ['platform-default' , 'ESCN' , 'LINUX' , 'SCO' , 'VT100' , 'VT400' , 'XTERMR6']
    type: str
  pwr_perf_tuning:
    description:
      -  BIOS Token for setting Power Performance Tuning configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  bios - Value - BIOS for configuring pwr_perf_tuning token.
      -  os - Value - os for configuring pwr_perf_tuning token.
      -  peci - Value - peci for configuring pwr_perf_tuning token.
    choices: ['platform-default' , 'bios' , 'os' , 'peci']
    type: str
  qpi_link_frequency:
    description:
      -  BIOS Token for setting QPI Link Frequency Select configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  6.4-gt/s - Value - 6.4-gt/s for configuring qpi_link_frequency token.
      -  7.2-gt/s - Value - 7.2-gt/s for configuring qpi_link_frequency token.
      -  8.0-gt/s - Value - 8.0-gt/s for configuring qpi_link_frequency token.
      -  9.6-gt/s - Value - 9.6-gt/s for configuring qpi_link_frequency token.
      -  auto - Value - auto for configuring qpi_link_frequency token.
    choices: ['platform-default' , '6.4-gt/s' , '7.2-gt/s' , '8.0-gt/s' , '9.6-gt/s' , 'auto']
    type: str
  qpi_link_speed:
    description:
      -  BIOS Token for setting UPI Link Frequency Select configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  10.4GT/s - Value - 10.4GT/s for configuring qpi_link_speed token.
      -  11.2GT/s - Value - 11.2GT/s for configuring qpi_link_speed token.
      -  12.8GT/s - Value - 12.8GT/s for configuring qpi_link_speed token.
      -  14.4GT/s - Value - 14.4GT/s for configuring qpi_link_speed token.
      -  16.0GT/s - Value - 16.0GT/s for configuring qpi_link_speed token.
      -  9.6GT/s - Value - 9.6GT/s for configuring qpi_link_speed token.
      -  Auto - Value - Auto for configuring qpi_link_speed token.
    choices: ['platform-default' , '10.4GT/s' , '11.2GT/s' , '12.8GT/s' , '14.4GT/s' , '16.0GT/s' , '9.6GT/s' , 'Auto']
    type: str
  qpi_snoop_mode:
    description:
      -  BIOS Token for setting QPI Snoop Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  auto - Value - auto for configuring qpi_snoop_mode token.
      -  cluster-on-die - Value - cluster-on-die for configuring qpi_snoop_mode token.
      -  early-snoop - Value - early-snoop for configuring qpi_snoop_mode token.
      -  home-directory-snoop - Value - home-directory-snoop for configuring qpi_snoop_mode token.
      -  home-directory-snoop-with-osb - Value - home-directory-snoop-with-osb for configuring qpi_snoop_mode token.
      -  home-snoop - Value - home-snoop for configuring qpi_snoop_mode token.
    choices: ['platform-default' , 'auto' , 'cluster-on-die' , 'early-snoop' , 'home-directory-snoop' , 'home-directory-snoop-with-osb' , 'home-snoop']
    type: str
  rank_inter_leave:
    description:
      -  BIOS Token for setting Rank Interleaving configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1-way - Value - 1-way for configuring rank_inter_leave token.
      -  2-way - Value - 2-way for configuring rank_inter_leave token.
      -  4-way - Value - 4-way for configuring rank_inter_leave token.
      -  8-way - Value - 8-way for configuring rank_inter_leave token.
      -  auto - Value - auto for configuring rank_inter_leave token.
    choices: ['platform-default' , '1-way' , '2-way' , '4-way' , '8-way' , 'auto']
    type: str
  redirection_after_post:
    description:
      -  BIOS Token for setting Redirection After BIOS POST configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Always Enable - Value - Always Enable for configuring redirection_after_post token.
      -  Bootloader - Value - Bootloader for configuring redirection_after_post token.
    choices: ['platform-default' , 'Always Enable' , 'Bootloader']
    type: str
  sata_mode_select:
    description:
      -  BIOS Token for setting SATA Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  AHCI - Value - AHCI for configuring sata_mode_select token.
      -  Disabled - Value - Disabled for configuring sata_mode_select token.
      -  LSI SW RAID - Value - LSI SW RAID for configuring sata_mode_select token.
    choices: ['platform-default' , 'AHCI' , 'Disabled' , 'LSI SW RAID']
    type: str
  select_memory_ras_configuration:
    description:
      -  BIOS Token for setting Memory RAS Configuration configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  adddc-sparing - Value - adddc-sparing for configuring select_memory_ras_configuration token.
      -  lockstep - Value - lockstep for configuring select_memory_ras_configuration token.
      -  maximum-performance - Value - maximum-performance for configuring select_memory_ras_configuration token.
      -  mirror-mode-1lm - Value - mirror-mode-1lm for configuring select_memory_ras_configuration token.
      -  mirroring - Value - mirroring for configuring select_memory_ras_configuration token.
      -  partial-mirror-mode-1lm - Value - partial-mirror-mode-1lm for configuring select_memory_ras_configuration token.
      -  sparing - Value - sparing for configuring select_memory_ras_configuration token.
    choices: ['platform-default' , 'adddc-sparing' , 'lockstep' , 'maximum-performance' , 'mirror-mode-1lm' , 'mirroring' ,
              'partial-mirror-mode-1lm' , 'sparing']
    type: str
  select_ppr_type:
    description:
      -  BIOS Token for setting PPR Type configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring select_ppr_type token.
      -  Hard PPR - Value - Hard PPR for configuring select_ppr_type token.
      -  Soft PPR - Value - Soft PPR for configuring select_ppr_type token.
    choices: ['platform-default' , 'disabled' , 'Hard PPR' , 'Soft PPR']
    type: str
  serial_port_aenable:
    description:
      -  BIOS Token for setting Serial A Enable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sev:
    description:
      -  BIOS Token for setting Secured Encrypted Virtualization configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  253 ASIDs - Value - 253 ASIDs for configuring sev token.
      -  509 ASIDs - Value - 509 ASIDs for configuring sev token.
      -  Auto - Value - Auto for configuring sev token.
    choices: ['platform-default' , '253 ASIDs' , '509 ASIDs' , 'Auto']
    type: str
  sgx_auto_registration_agent:
    description:
      -  BIOS Token for setting SGX Auto MP Registration Agent configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sgx_epoch0:
    description:
      -  BIOS Token for setting SGX Epoch 0 configuration (0 - ffffffffffffffff Hash byte 7-0).
    type: str
  sgx_epoch1:
    description:
      -  BIOS Token for setting SGX Epoch 1 configuration (0 - ffffffffffffffff Hash byte 7-0).
    type: str
  sgx_factory_reset:
    description:
      -  BIOS Token for setting SGX Factory Reset configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sgx_le_pub_key_hash0:
    description:
      -  BIOS Token for setting SGX PubKey Hash0 configuration (0 - ffffffffffffffff Hash byte 7-0).
    type: str
  sgx_le_pub_key_hash1:
    description:
      -  BIOS Token for setting SGX PubKey Hash1 configuration (0 - ffffffffffffffff Hash byte 15-8).
    type: str
  sgx_le_pub_key_hash2:
    description:
      -  BIOS Token for setting SGX PubKey Hash2 configuration (0 - ffffffffffffffff Hash byte 23-16).
    type: str
  sgx_le_pub_key_hash3:
    description:
      -  BIOS Token for setting SGX PubKey Hash3 configuration (0 - ffffffffffffffff Hash byte 31-24).
    type: str
  sgx_le_wr:
    description:
      -  BIOS Token for setting SGX Write Enable configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sgx_package_info_in_band_access:
    description:
      -  BIOS Token for setting SGX Package Information In-Band Access configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sgx_qos:
    description:
      -  BIOS Token for setting SGX QoS configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sha1pcr_bank:
    description:
      -  BIOS Token for setting SHA-1 PCR Bank configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sha256pcr_bank:
    description:
      -  BIOS Token for setting SHA256 PCR Bank configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  single_pctl_enable:
    description:
      -  BIOS Token for setting Single PCTL configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  No - Value - No for configuring single_pctl_enable token.
      -  Yes - Value - Yes for configuring single_pctl_enable token.
    choices: ['platform-default' , 'No' , 'Yes']
    type: str
  slot10link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:10 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot10link_speed token.
      -  Disabled - Value - Disabled for configuring slot10link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot10link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot10link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot10link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot10state:
    description:
      -  BIOS Token for setting Slot 10 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot10state token.
      -  enabled - Value - enabled for configuring slot10state token.
      -  Legacy Only - Value - Legacy Only for configuring slot10state token.
      -  UEFI Only - Value - UEFI Only for configuring slot10state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot11link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:11 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot11link_speed token.
      -  Disabled - Value - Disabled for configuring slot11link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot11link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot11link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot11link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot11state:
    description:
      -  BIOS Token for setting Slot 11 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot12link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:12 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot12link_speed token.
      -  Disabled - Value - Disabled for configuring slot12link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot12link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot12link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot12link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot12state:
    description:
      -  BIOS Token for setting Slot 12 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot13state:
    description:
      -  BIOS Token for setting Slot 13 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot14state:
    description:
      -  BIOS Token for setting Slot 14 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot1link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot1link_speed token.
      -  Disabled - Value - Disabled for configuring slot1link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot1link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot1link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot1link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot1link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot1state:
    description:
      -  BIOS Token for setting Slot 1 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot1state token.
      -  enabled - Value - enabled for configuring slot1state token.
      -  Legacy Only - Value - Legacy Only for configuring slot1state token.
      -  UEFI Only - Value - UEFI Only for configuring slot1state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot2link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot2link_speed token.
      -  Disabled - Value - Disabled for configuring slot2link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot2link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot2link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot2link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot2link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot2state:
    description:
      -  BIOS Token for setting Slot 2 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot2state token.
      -  enabled - Value - enabled for configuring slot2state token.
      -  Legacy Only - Value - Legacy Only for configuring slot2state token.
      -  UEFI Only - Value - UEFI Only for configuring slot2state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot3link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 3 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot3link_speed token.
      -  Disabled - Value - Disabled for configuring slot3link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot3link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot3link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot3link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot3link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot3link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot3state:
    description:
      -  BIOS Token for setting Slot 3 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot3state token.
      -  enabled - Value - enabled for configuring slot3state token.
      -  Legacy Only - Value - Legacy Only for configuring slot3state token.
      -  UEFI Only - Value - UEFI Only for configuring slot3state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot4link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 4 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot4link_speed token.
      -  Disabled - Value - Disabled for configuring slot4link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot4link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot4link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot4link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot4link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot4link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot4state:
    description:
      -  BIOS Token for setting Slot 4 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot4state token.
      -  enabled - Value - enabled for configuring slot4state token.
      -  Legacy Only - Value - Legacy Only for configuring slot4state token.
      -  UEFI Only - Value - UEFI Only for configuring slot4state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot5link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 5 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot5link_speed token.
      -  Disabled - Value - Disabled for configuring slot5link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot5link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot5link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot5link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot5link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot5link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot5state:
    description:
      -  BIOS Token for setting Slot 5 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot5state token.
      -  enabled - Value - enabled for configuring slot5state token.
      -  Legacy Only - Value - Legacy Only for configuring slot5state token.
      -  UEFI Only - Value - UEFI Only for configuring slot5state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot6link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 6 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot6link_speed token.
      -  Disabled - Value - Disabled for configuring slot6link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot6link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot6link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot6link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot6link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot6link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot6state:
    description:
      -  BIOS Token for setting Slot 6 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot6state token.
      -  enabled - Value - enabled for configuring slot6state token.
      -  Legacy Only - Value - Legacy Only for configuring slot6state token.
      -  UEFI Only - Value - UEFI Only for configuring slot6state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot7link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 7 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot7link_speed token.
      -  Disabled - Value - Disabled for configuring slot7link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot7link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot7link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot7link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot7link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot7link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot7state:
    description:
      -  BIOS Token for setting Slot 7 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot7state token.
      -  enabled - Value - enabled for configuring slot7state token.
      -  Legacy Only - Value - Legacy Only for configuring slot7state token.
      -  UEFI Only - Value - UEFI Only for configuring slot7state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot8link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 8 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot8link_speed token.
      -  Disabled - Value - Disabled for configuring slot8link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot8link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot8link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot8link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot8link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot8link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot8state:
    description:
      -  BIOS Token for setting Slot 8 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot8state token.
      -  enabled - Value - enabled for configuring slot8state token.
      -  Legacy Only - Value - Legacy Only for configuring slot8state token.
      -  UEFI Only - Value - UEFI Only for configuring slot8state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot9link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot: 9 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot9link_speed token.
      -  Disabled - Value - Disabled for configuring slot9link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot9link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot9link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot9link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot9link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4']
    type: str
  slot9state:
    description:
      -  BIOS Token for setting Slot 9 State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot9state token.
      -  enabled - Value - enabled for configuring slot9state token.
      -  Legacy Only - Value - Legacy Only for configuring slot9state token.
      -  UEFI Only - Value - UEFI Only for configuring slot9state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_flom_link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:FLOM Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_flom_link_speed token.
      -  Disabled - Value - Disabled for configuring slot_flom_link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_flom_link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_flom_link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_flom_link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_front_nvme10link_speed:
    description:
      -  BIOS Token for setting Front NVME 10 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme10link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme10link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme10link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme10link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme10link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme10link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme10link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme10option_rom:
    description:
      -  BIOS Token for setting Front NVME 10 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme11link_speed:
    description:
      -  BIOS Token for setting Front NVME 11 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme11link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme11link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme11link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme11link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme11link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme11link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme11link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme11option_rom:
    description:
      -  BIOS Token for setting Front NVME 11 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme12link_speed:
    description:
      -  BIOS Token for setting Front NVME 12 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme12link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme12link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme12link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme12link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme12link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme12link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme12link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme12option_rom:
    description:
      -  BIOS Token for setting Front NVME 12 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme13link_speed:
    description:
      -  BIOS Token for setting Front NVME 13 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme13link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme13link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme13link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme13link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme13link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme13link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme13link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme13option_rom:
    description:
      -  BIOS Token for setting Front NVME 13 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme14link_speed:
    description:
      -  BIOS Token for setting Front NVME 14 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme14link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme14link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme14link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme14link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme14link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme14link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme14link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme14option_rom:
    description:
      -  BIOS Token for setting Front NVME 14 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme15link_speed:
    description:
      -  BIOS Token for setting Front NVME 15 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme15link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme15link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme15link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme15link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme15link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme15link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme15link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme15option_rom:
    description:
      -  BIOS Token for setting Front NVME 15 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme16link_speed:
    description:
      -  BIOS Token for setting Front NVME 16 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme16link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme16link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme16link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme16link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme16link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme16link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme16link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme16option_rom:
    description:
      -  BIOS Token for setting Front NVME 16 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme17link_speed:
    description:
      -  BIOS Token for setting Front NVME 17 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme17link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme17link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme17link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme17link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme17link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme17link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme17link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme17option_rom:
    description:
      -  BIOS Token for setting Front NVME 17 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme18link_speed:
    description:
      -  BIOS Token for setting Front NVME 18 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme18link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme18link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme18link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme18link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme18link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme18link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme18link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme18option_rom:
    description:
      -  BIOS Token for setting Front NVME 18 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme19link_speed:
    description:
      -  BIOS Token for setting Front NVME 19 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme19link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme19link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme19link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme19link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme19link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme19link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme19link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme19option_rom:
    description:
      -  BIOS Token for setting Front NVME 19 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme1link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Front NVME 1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme1link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme1link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme1link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme1link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme1link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme1link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme1option_rom:
    description:
      -  BIOS Token for setting Front NVME 1 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme20link_speed:
    description:
      -  BIOS Token for setting Front NVME 20 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme20link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme20link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme20link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme20link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme20link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme20link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme20link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme20option_rom:
    description:
      -  BIOS Token for setting Front NVME 20 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme21link_speed:
    description:
      -  BIOS Token for setting Front NVME 21 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme21link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme21link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme21link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme21link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme21link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme21link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme21link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme21option_rom:
    description:
      -  BIOS Token for setting Front NVME 21 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme22link_speed:
    description:
      -  BIOS Token for setting Front NVME 22 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme22link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme22link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme22link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme22link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme22link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme22link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme22link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme22option_rom:
    description:
      -  BIOS Token for setting Front NVME 22 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme23link_speed:
    description:
      -  BIOS Token for setting Front NVME 23 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme23link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme23link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme23link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme23link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme23link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme23link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme23link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme23option_rom:
    description:
      -  BIOS Token for setting Front NVME 23 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme24link_speed:
    description:
      -  BIOS Token for setting Front NVME 24 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme24link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme24link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme24link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme24link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme24link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme24link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme24link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme24option_rom:
    description:
      -  BIOS Token for setting Front NVME 24 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme2link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Front NVME 2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme2link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme2link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme2link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme2link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme2link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme2link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme2option_rom:
    description:
      -  BIOS Token for setting Front NVME 2 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme3link_speed:
    description:
      -  BIOS Token for setting Front NVME 3 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme3link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme3link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme3link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme3link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme3link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme3link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme3link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme3option_rom:
    description:
      -  BIOS Token for setting Front NVME 3 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme4link_speed:
    description:
      -  BIOS Token for setting Front NVME 4 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme4link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme4link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme4link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme4link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme4link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme4link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme4link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme4option_rom:
    description:
      -  BIOS Token for setting Front NVME 4 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme5link_speed:
    description:
      -  BIOS Token for setting Front NVME 5 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme5link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme5link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme5link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme5link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme5link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme5link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme5link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme5option_rom:
    description:
      -  BIOS Token for setting Front NVME 5 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme6link_speed:
    description:
      -  BIOS Token for setting Front NVME 6 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme6link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme6link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme6link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme6link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme6link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme6link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme6link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme6option_rom:
    description:
      -  BIOS Token for setting Front NVME 6 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme7link_speed:
    description:
      -  BIOS Token for setting Front NVME 7 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme7link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme7link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme7link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme7link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme7link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme7link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme7link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme7option_rom:
    description:
      -  BIOS Token for setting Front NVME 7 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme8link_speed:
    description:
      -  BIOS Token for setting Front NVME 8 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme8link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme8link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme8link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme8link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme8link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme8link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme8link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme8option_rom:
    description:
      -  BIOS Token for setting Front NVME 8 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_nvme9link_speed:
    description:
      -  BIOS Token for setting Front NVME 9 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_nvme9link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_nvme9link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_nvme9link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_nvme9link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_nvme9link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_front_nvme9link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_front_nvme9link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_front_nvme9option_rom:
    description:
      -  BIOS Token for setting Front NVME 9 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_front_slot5link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Front1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_slot5link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_slot5link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_slot5link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_slot5link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_slot5link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_front_slot6link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Front2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_front_slot6link_speed token.
      -  Disabled - Value - Disabled for configuring slot_front_slot6link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_front_slot6link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_front_slot6link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_front_slot6link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_gpu1state:
    description:
      -  BIOS Token for setting GPU 1 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu2state:
    description:
      -  BIOS Token for setting GPU 2 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu3state:
    description:
      -  BIOS Token for setting GPU 3 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu4state:
    description:
      -  BIOS Token for setting GPU 4 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu5state:
    description:
      -  BIOS Token for setting GPU 5 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu6state:
    description:
      -  BIOS Token for setting GPU 6 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu7state:
    description:
      -  BIOS Token for setting GPU 7 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_gpu8state:
    description:
      -  BIOS Token for setting GPU 8 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_hba_link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:HBA Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_hba_link_speed token.
      -  Disabled - Value - Disabled for configuring slot_hba_link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_hba_link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_hba_link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_hba_link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_hba_state:
    description:
      - 'BIOS Token for setting PCIe Slot:HBA OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot_hba_state token.
      -  enabled - Value - enabled for configuring slot_hba_state token.
      -  Legacy Only - Value - Legacy Only for configuring slot_hba_state token.
      -  UEFI Only - Value - UEFI Only for configuring slot_hba_state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_lom1link:
    description:
      - 'BIOS Token for setting PCIe LOM:1 Link configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_lom2link:
    description:
      - 'BIOS Token for setting PCIe LOM:2 Link configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_mezz_state:
    description:
      -  BIOS Token for setting Slot Mezz State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot_mezz_state token.
      -  enabled - Value - enabled for configuring slot_mezz_state token.
      -  Legacy Only - Value - Legacy Only for configuring slot_mezz_state token.
      -  UEFI Only - Value - UEFI Only for configuring slot_mezz_state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_mlom_link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:MLOM Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_mlom_link_speed token.
      -  Disabled - Value - Disabled for configuring slot_mlom_link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_mlom_link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_mlom_link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_mlom_link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_mlom_link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_mlom_link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_mlom_state:
    description:
      -  BIOS Token for setting PCIe Slot MLOM OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot_mlom_state token.
      -  enabled - Value - enabled for configuring slot_mlom_state token.
      -  Legacy Only - Value - Legacy Only for configuring slot_mlom_state token.
      -  UEFI Only - Value - UEFI Only for configuring slot_mlom_state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_mraid_link_speed:
    description:
      -  BIOS Token for setting MRAID Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_mraid_link_speed token.
      -  Disabled - Value - Disabled for configuring slot_mraid_link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_mraid_link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_mraid_link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_mraid_link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_mraid_link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_mraid_link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_mraid_state:
    description:
      -  BIOS Token for setting PCIe Slot MRAID OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n10state:
    description:
      -  BIOS Token for setting PCIe Slot N10 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n11state:
    description:
      -  BIOS Token for setting PCIe Slot N11 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n12state:
    description:
      -  BIOS Token for setting PCIe Slot N12 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n13state:
    description:
      -  BIOS Token for setting PCIe Slot N13 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n14state:
    description:
      -  BIOS Token for setting PCIe Slot N14 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n15state:
    description:
      -  BIOS Token for setting PCIe Slot N15 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n16state:
    description:
      -  BIOS Token for setting PCIe Slot N16 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n17state:
    description:
      -  BIOS Token for setting PCIe Slot N17 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n18state:
    description:
      -  BIOS Token for setting PCIe Slot N18 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n19state:
    description:
      -  BIOS Token for setting PCIe Slot N19 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n1state:
    description:
      -  BIOS Token for setting PCIe Slot N1 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot_n1state token.
      -  enabled - Value - enabled for configuring slot_n1state token.
      -  Legacy Only - Value - Legacy Only for configuring slot_n1state token.
      -  UEFI Only - Value - UEFI Only for configuring slot_n1state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_n20state:
    description:
      -  BIOS Token for setting PCIe Slot N20 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n21state:
    description:
      -  BIOS Token for setting PCIe Slot N21 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n22state:
    description:
      -  BIOS Token for setting PCIe Slot N22 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n23state:
    description:
      -  BIOS Token for setting PCIe Slot N23 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n24state:
    description:
      -  BIOS Token for setting PCIe Slot N24 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n2state:
    description:
      -  BIOS Token for setting PCIe Slot N2 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot_n2state token.
      -  enabled - Value - enabled for configuring slot_n2state token.
      -  Legacy Only - Value - Legacy Only for configuring slot_n2state token.
      -  UEFI Only - Value - UEFI Only for configuring slot_n2state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_n3state:
    description:
      -  BIOS Token for setting PCIe Slot N3 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n4state:
    description:
      -  BIOS Token for setting PCIe Slot N4 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n5state:
    description:
      -  BIOS Token for setting PCIe Slot N5 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n6state:
    description:
      -  BIOS Token for setting PCIe Slot N6 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n7state:
    description:
      -  BIOS Token for setting PCIe Slot N7 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n8state:
    description:
      -  BIOS Token for setting PCIe Slot N8 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_n9state:
    description:
      -  BIOS Token for setting PCIe Slot N9 OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_raid_link_speed:
    description:
      -  BIOS Token for setting RAID Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_raid_link_speed token.
      -  Disabled - Value - Disabled for configuring slot_raid_link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_raid_link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_raid_link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_raid_link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_raid_state:
    description:
      -  BIOS Token for setting PCIe Slot RAID OptionROM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme1link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_rear_nvme1link_speed token.
      -  Disabled - Value - Disabled for configuring slot_rear_nvme1link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_rear_nvme1link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_rear_nvme1link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_rear_nvme1link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_rear_nvme1link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_rear_nvme1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_rear_nvme1state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 1 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme2link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_rear_nvme2link_speed token.
      -  Disabled - Value - Disabled for configuring slot_rear_nvme2link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_rear_nvme2link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_rear_nvme2link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_rear_nvme2link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_rear_nvme2link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_rear_nvme2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_rear_nvme2state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 2 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme3link_speed:
    description:
      -  BIOS Token for setting Rear NVME 3 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_rear_nvme3link_speed token.
      -  Disabled - Value - Disabled for configuring slot_rear_nvme3link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_rear_nvme3link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_rear_nvme3link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_rear_nvme3link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_rear_nvme3link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_rear_nvme3link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_rear_nvme3state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 3 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme4link_speed:
    description:
      -  BIOS Token for setting Rear NVME 4 Link Speed configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_rear_nvme4link_speed token.
      -  Disabled - Value - Disabled for configuring slot_rear_nvme4link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_rear_nvme4link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_rear_nvme4link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_rear_nvme4link_speed token.
      -  GEN4 - Value - GEN4 for configuring slot_rear_nvme4link_speed token.
      -  GEN5 - Value - GEN5 for configuring slot_rear_nvme4link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3' , 'GEN4' , 'GEN5']
    type: str
  slot_rear_nvme4state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 4 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme5state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 5 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme6state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 6 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme7state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 7 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_rear_nvme8state:
    description:
      - 'BIOS Token for setting PCIe Slot:Rear NVME 8 OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  slot_riser1link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser1link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser1link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser1link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser1link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser1slot1link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser1 Slot1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser1slot1link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser1slot1link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser1slot1link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser1slot1link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser1slot1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser1slot2link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser1 Slot2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser1slot2link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser1slot2link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser1slot2link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser1slot2link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser1slot2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser1slot3link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser1 Slot3 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser1slot3link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser1slot3link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser1slot3link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser1slot3link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser1slot3link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser2link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser2link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser2link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser2link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser2link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser2slot4link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser2 Slot4 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser2slot4link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser2slot4link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser2slot4link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser2slot4link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser2slot4link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser2slot5link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser2 Slot5 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser2slot5link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser2slot5link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser2slot5link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser2slot5link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser2slot5link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_riser2slot6link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:Riser2 Slot6 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_riser2slot6link_speed token.
      -  Disabled - Value - Disabled for configuring slot_riser2slot6link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_riser2slot6link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_riser2slot6link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_riser2slot6link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_sas_state:
    description:
      - 'BIOS Token for setting PCIe Slot:SAS OptionROM configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  disabled - Value - disabled for configuring slot_sas_state token.
      -  enabled - Value - enabled for configuring slot_sas_state token.
      -  Legacy Only - Value - Legacy Only for configuring slot_sas_state token.
      -  UEFI Only - Value - UEFI Only for configuring slot_sas_state token.
    choices: ['platform-default' , 'disabled' , 'enabled' , 'Legacy Only' , 'UEFI Only']
    type: str
  slot_ssd_slot1link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:FrontSSD1 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_ssd_slot1link_speed token.
      -  Disabled - Value - Disabled for configuring slot_ssd_slot1link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_ssd_slot1link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_ssd_slot1link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_ssd_slot1link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  slot_ssd_slot2link_speed:
    description:
      - 'BIOS Token for setting PCIe Slot:FrontSSD2 Link Speed configuration.'
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring slot_ssd_slot2link_speed token.
      -  Disabled - Value - Disabled for configuring slot_ssd_slot2link_speed token.
      -  GEN1 - Value - GEN1 for configuring slot_ssd_slot2link_speed token.
      -  GEN2 - Value - GEN2 for configuring slot_ssd_slot2link_speed token.
      -  GEN3 - Value - GEN3 for configuring slot_ssd_slot2link_speed token.
    choices: ['platform-default' , 'Auto' , 'Disabled' , 'GEN1' , 'GEN2' , 'GEN3']
    type: str
  smee:
    description:
      -  BIOS Token for setting SMEE configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  smt_mode:
    description:
      -  BIOS Token for setting SMT Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring smt_mode token.
      -  Off - Value - Off for configuring smt_mode token.
    choices: ['platform-default' , 'Auto' , 'Off']
    type: str
  snc:
    description:
      -  BIOS Token for setting Sub Numa Clustering configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring snc token.
      -  disabled - Value - disabled for configuring snc token.
      -  enabled - Value - enabled for configuring snc token.
      -  SNC2 - Value - SNC2 for configuring snc token.
      -  SNC4 - Value - SNC4 for configuring snc token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled' , 'SNC2' , 'SNC4']
    type: str
  snoopy_mode_for2lm:
    description:
      -  BIOS Token for setting Snoopy Mode for 2LM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  snoopy_mode_for_ad:
    description:
      -  BIOS Token for setting Snoopy Mode for AD configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  sparing_mode:
    description:
      -  BIOS Token for setting Sparing Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  dimm-sparing - Value - dimm-sparing for configuring sparing_mode token.
      -  rank-sparing - Value - rank-sparing for configuring sparing_mode token.
    choices: ['platform-default' , 'dimm-sparing' , 'rank-sparing']
    type: str
  sr_iov:
    description:
      -  BIOS Token for setting SR-IOV Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  streamer_prefetch:
    description:
      -  BIOS Token for setting DCU Streamer Prefetch configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  svm_mode:
    description:
      -  BIOS Token for setting SVM Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  terminal_type:
    description:
      -  BIOS Token for setting Terminal Type configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  pc-ansi - Value - pc-ansi for configuring terminal_type token.
      -  vt100 - Value - vt100 for configuring terminal_type token.
      -  vt100-plus - Value - vt100-plus for configuring terminal_type token.
      -  vt-utf8 - Value - vt-utf8 for configuring terminal_type token.
    choices: ['platform-default' , 'pc-ansi' , 'vt100' , 'vt100-plus' , 'vt-utf8']
    type: str
  tpm_control:
    description:
      -  BIOS Token for setting Trusted Platform Module State configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  tpm_pending_operation:
    description:
      -  BIOS Token for setting TPM Pending Operation configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  None - Value - None for configuring tpm_pending_operation token.
      -  TpmClear - Value - TpmClear for configuring tpm_pending_operation token.
    choices: ['platform-default' , 'None' , 'TpmClear']
    type: str
  tpm_ppi_required:
    description:
      -  BIOS Token for setting TPM Minimal Physical Presence configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  tpm_support:
    description:
      -  BIOS Token for setting Security Device Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  tsme:
    description:
      -  BIOS Token for setting Transparent Secure Memory Encryption configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring tsme token.
      -  disabled - Value - disabled for configuring tsme token.
      -  enabled - Value - enabled for configuring tsme token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  txt_support:
    description:
      -  BIOS Token for setting Intel Trusted Execution Technology Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  ucsm_boot_order_rule:
    description:
      -  BIOS Token for setting Boot Order Rules configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Loose - Value - Loose for configuring ucsm_boot_order_rule token.
      -  Strict - Value - Strict for configuring ucsm_boot_order_rule token.
    choices: ['platform-default' , 'Loose' , 'Strict']
    type: str
  ufs_disable:
    description:
      -  BIOS Token for setting Uncore Frequency Scaling configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  uma_based_clustering:
    description:
      -  BIOS Token for setting UMA Based Clustering configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Disable (All2All) - Value - Disable (All2All) for configuring uma_based_clustering token.
      -  Hemisphere (2-clusters) - Value - Hemisphere (2-clusters) for configuring uma_based_clustering token.
      -  Quadrant (4-clusters) - Value - Quadrant (4-clusters) for configuring uma_based_clustering token.
    choices: ['platform-default' , 'Disable (All2All)' , 'Hemisphere (2-clusters)' , 'Quadrant (4-clusters)']
    type: str
  upi_link_enablement:
    description:
      -  BIOS Token for setting UPI Link Enablement configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1 - Value - 1 for configuring upi_link_enablement token.
      -  2 - Value - 2 for configuring upi_link_enablement token.
      -  3 - Value - 3 for configuring upi_link_enablement token.
      -  Auto - Value - Auto for configuring upi_link_enablement token.
    choices: ['platform-default' , '1' , '2' , '3' , 'Auto']
    type: str
  upi_power_management:
    description:
      -  BIOS Token for setting UPI Power Manangement configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_emul6064:
    description:
      -  BIOS Token for setting Port 60/64 Emulation configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_port_front:
    description:
      -  BIOS Token for setting USB Port Front configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_port_internal:
    description:
      -  BIOS Token for setting USB Port Internal configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_port_kvm:
    description:
      -  BIOS Token for setting USB Port KVM configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_port_rear:
    description:
      -  BIOS Token for setting USB Port Rear configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_port_sd_card:
    description:
      -  BIOS Token for setting USB Port SD Card configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_port_vmedia:
    description:
      -  BIOS Token for setting USB Port VMedia configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  usb_xhci_support:
    description:
      -  BIOS Token for setting XHCI Legacy Support configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  vga_priority:
    description:
      -  BIOS Token for setting VGA Priority configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Offboard - Value - Offboard for configuring vga_priority token.
      -  Onboard - Value - Onboard for configuring vga_priority token.
      -  Onboard VGA Disabled - Value - Onboard VGA Disabled for configuring vga_priority token.
    choices: ['platform-default' , 'Offboard' , 'Onboard' , 'Onboard VGA Disabled']
    type: str
  virtual_numa:
    description:
      -  BIOS Token for setting Virtual NUMA configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  vmd_enable:
    description:
      -  BIOS Token for setting VMD Enablement configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  vol_memory_mode:
    description:
      -  BIOS Token for setting Volatile Memory Mode configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  1LM - Value - 1LM for configuring vol_memory_mode token.
      -  2LM - Value - 2LM for configuring vol_memory_mode token.
    choices: ['platform-default' , '1LM' , '2LM']
    type: str
  work_load_config:
    description:
      -  BIOS Token for setting Workload Configuration configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Balanced - Value - Balanced for configuring work_load_config token.
      -  I/O Sensitive - Value - I/O Sensitive for configuring work_load_config token.
      -  NUMA - Value - NUMA for configuring work_load_config token.
      -  UMA - Value - UMA for configuring work_load_config token.
    choices: ['platform-default' , 'Balanced' , 'I/O Sensitive' , 'NUMA' , 'UMA']
    type: str
  x2apic_opt_out:
    description:
      -  BIOS Token for setting X2APIC Opt-Out Flag configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  enabled - Enables the BIOS setting.
      -  disabled - Disables the BIOS setting.
    choices: ['platform-default' , 'enabled' , 'disabled']
    type: str
  xpt_prefetch:
    description:
      -  BIOS Token for setting XPT Prefetch configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring xpt_prefetch token.
      -  disabled - Value - disabled for configuring xpt_prefetch token.
      -  enabled - Value - enabled for configuring xpt_prefetch token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
  xpt_remote_prefetch:
    description:
      -  BIOS Token for setting XPT Remote Prefetch configuration.
      -  platform-default - Default value used by the platform for the BIOS setting.
      -  Auto - Value - Auto for configuring xpt_remote_prefetch token.
      -  disabled - Value - disabled for configuring xpt_remote_prefetch token.
      -  enabled - Value - enabled for configuring xpt_remote_prefetch token.
    choices: ['platform-default' , 'Auto' , 'disabled' , 'enabled']
    type: str
author:
  - Surendra Ramarao (@CRSurendra)
'''

EXAMPLES = r'''
- name: Configure BIOS Policy
  cisco.intersight.intersight_bios_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-BIOS
    description: Boot Order policy for COS
    tags:
      - Key: Site
        Value: RCDN
    processor_cstate: enabled

- name: Delete BIOS Policy
  cisco.intersight.intersight_bios_policy:
    api_private_key: "{{ api_private_key }}"
    api_key_id: "{{ api_key_id }}"
    organization: DevNet
    name: COS-BIOS
    state: absent
'''

RETURN = r'''
api_response:
  description: The API response output returned by the specified resource.
  returned: always
  type: dict
  sample:
    "api_response": {
        "Name": "COS-BIOS",
        "ObjectType": "bios.Policy",
        "Tags": [
            {
                "Key": "Site",
                "Value": "RCDN"
            }
        ]
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.intersight.plugins.module_utils.intersight import IntersightModule, intersight_argument_spec


def check_and_add_prop(prop, propKey, params, api_body):
    if propKey in params.keys():
        api_body[prop] = params[propKey]


def apply_bios_properties(params, api_body):
    """
    Apply BIOS properties from module parameters to API body.
    Maps snake_case parameter names to PascalCase API property names.

    Args:
        params: Module parameters dictionary
        api_body: API request body dictionary to update
    """
    # Mapping of snake_case parameter names to PascalCase API property names
    bios_property_map = {
        'acs_control_gpu1state': 'AcsControlGpu1state',
        'acs_control_gpu2state': 'AcsControlGpu2state',
        'acs_control_gpu3state': 'AcsControlGpu3state',
        'acs_control_gpu4state': 'AcsControlGpu4state',
        'acs_control_gpu5state': 'AcsControlGpu5state',
        'acs_control_gpu6state': 'AcsControlGpu6state',
        'acs_control_gpu7state': 'AcsControlGpu7state',
        'acs_control_gpu8state': 'AcsControlGpu8state',
        'acs_control_slot11state': 'AcsControlSlot11state',
        'acs_control_slot12state': 'AcsControlSlot12state',
        'acs_control_slot13state': 'AcsControlSlot13state',
        'acs_control_slot14state': 'AcsControlSlot14state',
        'adaptive_refresh_mgmt_level': 'AdaptiveRefreshMgmtLevel',
        'adjacent_cache_line_prefetch': 'AdjacentCacheLinePrefetch',
        'advanced_mem_test': 'AdvancedMemTest',
        'all_usb_devices': 'AllUsbDevices',
        'altitude': 'Altitude',
        'aspm_support': 'AspmSupport',
        'assert_nmi_on_perr': 'AssertNmiOnPerr',
        'assert_nmi_on_serr': 'AssertNmiOnSerr',
        'auto_cc_state': 'AutoCcState',
        'autonumous_cstate_enable': 'AutonumousCstateEnable',
        'baud_rate': 'BaudRate',
        'bme_dma_mitigation': 'BmeDmaMitigation',
        'boot_option_num_retry': 'BootOptionNumRetry',
        'boot_option_re_cool_down': 'BootOptionReCoolDown',
        'boot_option_retry': 'BootOptionRetry',
        'boot_performance_mode': 'BootPerformanceMode',
        'burst_and_postponed_refresh': 'BurstAndPostponedRefresh',
        'c1auto_demotion': 'C1autoDemotion',
        'c1auto_un_demotion': 'C1autoUnDemotion',
        'cbs_cmn_apbdis': 'CbsCmnApbdis',
        'cbs_cmn_cpu_cpb': 'CbsCmnCpuCpb',
        'cbs_cmn_cpu_gen_downcore_ctrl': 'CbsCmnCpuGenDowncoreCtrl',
        'cbs_cmn_cpu_global_cstate_ctrl': 'CbsCmnCpuGlobalCstateCtrl',
        'cbs_cmn_cpu_l1stream_hw_prefetcher': 'CbsCmnCpuL1streamHwPrefetcher',
        'cbs_cmn_cpu_l2stream_hw_prefetcher': 'CbsCmnCpuL2streamHwPrefetcher',
        'cbs_cmn_cpu_smee': 'CbsCmnCpuSmee',
        'cbs_cmn_cpu_streaming_stores_ctrl': 'CbsCmnCpuStreamingStoresCtrl',
        'cbs_cmnc_tdp_ctl': 'CbsCmncTdpCtl',
        'cbs_cmn_determinism_slider': 'CbsCmnDeterminismSlider',
        'cbs_cmn_efficiency_mode_en': 'CbsCmnEfficiencyModeEn',
        'cbs_cmn_fixed_soc_pstate': 'CbsCmnFixedSocPstate',
        'cbs_cmn_gnb_nb_iommu': 'CbsCmnGnbNbIommu',
        'cbs_cmn_gnb_smucppc': 'CbsCmnGnbSmucppc',
        'cbs_cmn_gnb_smu_df_cstates': 'CbsCmnGnbSmuDfCstates',
        'cbs_cmn_mem_ctrl_bank_group_swap_ddr4': 'CbsCmnMemCtrlBankGroupSwapDdr4',
        'cbs_cmn_mem_map_bank_interleave_ddr4': 'CbsCmnMemMapBankInterleaveDdr4',
        'cbs_cpu_ccd_ctrl_ssp': 'CbsCpuCcdCtrlSsp',
        'cbs_cpu_core_ctrl': 'CbsCpuCoreCtrl',
        'cbs_cpu_smt_ctrl': 'CbsCpuSmtCtrl',
        'cbs_dbg_cpu_snp_mem_cover': 'CbsDbgCpuSnpMemCover',
        'cbs_dbg_cpu_snp_mem_size_cover': 'CbsDbgCpuSnpMemSizeCover',
        'cbs_df_cmn_acpi_srat_l3numa': 'CbsDfCmnAcpiSratL3numa',
        'cbs_df_cmn_dram_nps': 'CbsDfCmnDramNps',
        'cbs_df_cmn_mem_intlv': 'CbsDfCmnMemIntlv',
        'cbs_df_cmn_mem_intlv_size': 'CbsDfCmnMemIntlvSize',
        'cbs_sev_snp_support': 'CbsSevSnpSupport',
        'cdn_enable': 'CdnEnable',
        'cdn_support': 'CdnSupport',
        'channel_inter_leave': 'ChannelInterLeave',
        'cisco_adaptive_mem_training': 'CiscoAdaptiveMemTraining',
        'cisco_debug_level': 'CiscoDebugLevel',
        'cisco_oprom_launch_optimization': 'CiscoOpromLaunchOptimization',
        'cisco_xgmi_max_speed': 'CiscoXgmiMaxSpeed',
        'cke_low_policy': 'CkeLowPolicy',
        'closed_loop_therm_throtl': 'ClosedLoopThermThrotl',
        'cmci_enable': 'CmciEnable',
        'config_tdp': 'ConfigTdp',
        'config_tdp_level': 'ConfigTdpLevel',
        'console_redirection': 'ConsoleRedirection',
        'core_multi_processing': 'CoreMultiProcessing',
        'cpu_energy_performance': 'CpuEnergyPerformance',
        'cpu_frequency_floor': 'CpuFrequencyFloor',
        'cpu_pa_limit': 'CpuPaLimit',
        'cpu_perf_enhancement': 'CpuPerfEnhancement',
        'cpu_performance': 'CpuPerformance',
        'cpu_power_management': 'CpuPowerManagement',
        'crfastgo_config': 'CrfastgoConfig',
        'cr_qos': 'CrQos',
        'dcpmm_firmware_downgrade': 'DcpmmFirmwareDowngrade',
        'demand_scrub': 'DemandScrub',
        'direct_cache_access': 'DirectCacheAccess',
        'dma_ctrl_opt_in': 'DmaCtrlOptIn',
        'dram_clock_throttling': 'DramClockThrottling',
        'dram_refresh_rate': 'DramRefreshRate',
        'dram_sw_thermal_throttling': 'DramSwThermalThrottling',
        'eadr_support': 'EadrSupport',
        'edpc_en': 'EdpcEn',
        'enable_clock_spread_spec': 'EnableClockSpreadSpec',
        'enable_mktme': 'EnableMktme',
        'enable_rmt': 'EnableRmt',
        'enable_sgx': 'EnableSgx',
        'enable_tme': 'EnableTme',
        'energy_efficient_turbo': 'EnergyEfficientTurbo',
        'eng_perf_tuning': 'EngPerfTuning',
        'enhanced_intel_speed_step_tech': 'EnhancedIntelSpeedStepTech',
        'epoch_update': 'EpochUpdate',
        'epp_enable': 'EppEnable',
        'epp_profile': 'EppProfile',
        'error_check_scrub': 'ErrorCheckScrub',
        'execute_disable_bit': 'ExecuteDisableBit',
        'extended_apic': 'ExtendedApic',
        'flow_control': 'FlowControl',
        'frb2enable': 'Frb2enable',
        'hardware_prefetch': 'HardwarePrefetch',
        'hwpm_enable': 'HwpmEnable',
        'imc_interleave': 'ImcInterleave',
        'intel_dynamic_speed_select': 'IntelDynamicSpeedSelect',
        'intel_hyper_threading_tech': 'IntelHyperThreadingTech',
        'intel_speed_select': 'IntelSpeedSelect',
        'intel_turbo_boost_tech': 'IntelTurboBoostTech',
        'intel_virtualization_technology': 'IntelVirtualizationTechnology',
        'intel_vtdats_support': 'IntelVtdatsSupport',
        'intel_vtd_coherency_support': 'IntelVtdCoherencySupport',
        'intel_vtd_interrupt_remapping': 'IntelVtdInterruptRemapping',
        'intel_vtd_pass_through_dma_support': 'IntelVtdPassThroughDmaSupport',
        'intel_vt_for_directed_io': 'IntelVtForDirectedIo',
        'ioh_error_enable': 'IohErrorEnable',
        'ioh_resource': 'IohResource',
        'ip_prefetch': 'IpPrefetch',
        'ipv4http': 'Ipv4http',
        'ipv4pxe': 'Ipv4pxe',
        'ipv6http': 'Ipv6http',
        'ipv6pxe': 'Ipv6pxe',
        'kti_prefetch': 'KtiPrefetch',
        'legacy_os_redirection': 'LegacyOsRedirection',
        'legacy_usb_support': 'LegacyUsbSupport',
        'llc_alloc': 'LlcAlloc',
        'llc_prefetch': 'LlcPrefetch',
        'lom_port0state': 'LomPort0state',
        'lom_port1state': 'LomPort1state',
        'lom_port2state': 'LomPort2state',
        'lom_port3state': 'LomPort3state',
        'lom_ports_all_state': 'LomPortsAllState',
        'lv_ddr_mode': 'LvDdrMode',
        'make_device_non_bootable': 'MakeDeviceNonBootable',
        'memory_bandwidth_boost': 'MemoryBandwidthBoost',
        'memory_inter_leave': 'MemoryInterLeave',
        'memory_mapped_io_above4gb': 'MemoryMappedIoAbove4gb',
        'memory_refresh_rate': 'MemoryRefreshRate',
        'memory_size_limit': 'MemorySizeLimit',
        'memory_thermal_throttling': 'MemoryThermalThrottling',
        'mirroring_mode': 'MirroringMode',
        'mmcfg_base': 'MmcfgBase',
        'network_stack': 'NetworkStack',
        'numa_optimized': 'NumaOptimized',
        'nvmdimm_perform_config': 'NvmdimmPerformConfig',
        'onboard10gbit_lom': 'Onboard10gbitLom',
        'onboard_gbit_lom': 'OnboardGbitLom',
        'onboard_scu_storage_support': 'OnboardScuStorageSupport',
        'onboard_scu_storage_sw_stack': 'OnboardScuStorageSwStack',
        'operation_mode': 'OperationMode',
        'organization': 'Organization',
        'os_boot_watchdog_timer': 'OsBootWatchdogTimer',
        'os_boot_watchdog_timer_policy': 'OsBootWatchdogTimerPolicy',
        'os_boot_watchdog_timer_timeout': 'OsBootWatchdogTimerTimeout',
        'out_of_band_mgmt_port': 'OutOfBandMgmtPort',
        'package_cstate_limit': 'PackageCstateLimit',
        'panic_high_watermark': 'PanicHighWatermark',
        'partial_cache_line_sparing': 'PartialCacheLineSparing',
        'partial_mirror_mode_config': 'PartialMirrorModeConfig',
        'partial_mirror_percent': 'PartialMirrorPercent',
        'partial_mirror_value1': 'PartialMirrorValue1',
        'partial_mirror_value2': 'PartialMirrorValue2',
        'partial_mirror_value3': 'PartialMirrorValue3',
        'partial_mirror_value4': 'PartialMirrorValue4',
        'patrol_scrub': 'PatrolScrub',
        'patrol_scrub_duration': 'PatrolScrubDuration',
        'pch_pcie_pll_ssc': 'PchPciePllSsc',
        'pch_usb30mode': 'PchUsb30mode',
        'pcie_ari_support': 'PcieAriSupport',
        'pcie_pll_ssc': 'PciePllSsc',
        'pc_ie_ras_support': 'PcIeRasSupport',
        'pcie_slot_mraid1link_speed': 'PcieSlotMraid1linkSpeed',
        'pcie_slot_mraid1option_rom': 'PcieSlotMraid1optionRom',
        'pcie_slot_mraid2link_speed': 'PcieSlotMraid2linkSpeed',
        'pcie_slot_mraid2option_rom': 'PcieSlotMraid2optionRom',
        'pcie_slot_mstorraid_link_speed': 'PcieSlotMstorraidLinkSpeed',
        'pcie_slot_mstorraid_option_rom': 'PcieSlotMstorraidOptionRom',
        'pcie_slot_nvme1link_speed': 'PcieSlotNvme1linkSpeed',
        'pcie_slot_nvme1option_rom': 'PcieSlotNvme1optionRom',
        'pcie_slot_nvme2link_speed': 'PcieSlotNvme2linkSpeed',
        'pcie_slot_nvme2option_rom': 'PcieSlotNvme2optionRom',
        'pcie_slot_nvme3link_speed': 'PcieSlotNvme3linkSpeed',
        'pcie_slot_nvme3option_rom': 'PcieSlotNvme3optionRom',
        'pcie_slot_nvme4link_speed': 'PcieSlotNvme4linkSpeed',
        'pcie_slot_nvme4option_rom': 'PcieSlotNvme4optionRom',
        'pcie_slot_nvme5link_speed': 'PcieSlotNvme5linkSpeed',
        'pcie_slot_nvme5option_rom': 'PcieSlotNvme5optionRom',
        'pcie_slot_nvme6link_speed': 'PcieSlotNvme6linkSpeed',
        'pcie_slot_nvme6option_rom': 'PcieSlotNvme6optionRom',
        'pcie_slots_cdn_enable': 'PcieSlotsCdnEnable',
        'pc_ie_ssd_hot_plug_support': 'PcIeSsdHotPlugSupport',
        'pci_option_ro_ms': 'PciOptionRoMs',
        'pci_rom_clp': 'PciRomClp',
        'pop_support': 'PopSupport',
        'post_error_pause': 'PostErrorPause',
        'post_package_repair': 'PostPackageRepair',
        'processor_c1e': 'ProcessorC1e',
        'processor_c3report': 'ProcessorC3report',
        'processor_c6report': 'ProcessorC6report',
        'processor_cstate': 'ProcessorCstate',
        'profiles': 'Profiles',
        'psata': 'Psata',
        'pstate_coord_type': 'PstateCoordType',
        'putty_key_pad': 'PuttyKeyPad',
        'pwr_perf_tuning': 'PwrPerfTuning',
        'qpi_link_frequency': 'QpiLinkFrequency',
        'qpi_link_speed': 'QpiLinkSpeed',
        'qpi_snoop_mode': 'QpiSnoopMode',
        'rank_inter_leave': 'RankInterLeave',
        'redirection_after_post': 'RedirectionAfterPost',
        'sata_mode_select': 'SataModeSelect',
        'select_memory_ras_configuration': 'SelectMemoryRasConfiguration',
        'select_ppr_type': 'SelectPprType',
        'serial_port_aenable': 'SerialPortAenable',
        'sev': 'Sev',
        'sgx_auto_registration_agent': 'SgxAutoRegistrationAgent',
        'sgx_epoch0': 'SgxEpoch0',
        'sgx_epoch1': 'SgxEpoch1',
        'sgx_factory_reset': 'SgxFactoryReset',
        'sgx_le_pub_key_hash0': 'SgxLePubKeyHash0',
        'sgx_le_pub_key_hash1': 'SgxLePubKeyHash1',
        'sgx_le_pub_key_hash2': 'SgxLePubKeyHash2',
        'sgx_le_pub_key_hash3': 'SgxLePubKeyHash3',
        'sgx_le_wr': 'SgxLeWr',
        'sgx_package_info_in_band_access': 'SgxPackageInfoInBandAccess',
        'sgx_qos': 'SgxQos',
        'sha1pcr_bank': 'Sha1pcrBank',
        'sha256pcr_bank': 'Sha256pcrBank',
        'single_pctl_enable': 'SinglePctlEnable',
        'slot10link_speed': 'Slot10linkSpeed',
        'slot10state': 'Slot10state',
        'slot11link_speed': 'Slot11linkSpeed',
        'slot11state': 'Slot11state',
        'slot12link_speed': 'Slot12linkSpeed',
        'slot12state': 'Slot12state',
        'slot13state': 'Slot13state',
        'slot14state': 'Slot14state',
        'slot1link_speed': 'Slot1linkSpeed',
        'slot1state': 'Slot1state',
        'slot2link_speed': 'Slot2linkSpeed',
        'slot2state': 'Slot2state',
        'slot3link_speed': 'Slot3linkSpeed',
        'slot3state': 'Slot3state',
        'slot4link_speed': 'Slot4linkSpeed',
        'slot4state': 'Slot4state',
        'slot5link_speed': 'Slot5linkSpeed',
        'slot5state': 'Slot5state',
        'slot6link_speed': 'Slot6linkSpeed',
        'slot6state': 'Slot6state',
        'slot7link_speed': 'Slot7linkSpeed',
        'slot7state': 'Slot7state',
        'slot8link_speed': 'Slot8linkSpeed',
        'slot8state': 'Slot8state',
        'slot9link_speed': 'Slot9linkSpeed',
        'slot9state': 'Slot9state',
        'slot_flom_link_speed': 'SlotFlomLinkSpeed',
        'slot_front_nvme10link_speed': 'SlotFrontNvme10linkSpeed',
        'slot_front_nvme10option_rom': 'SlotFrontNvme10optionRom',
        'slot_front_nvme11link_speed': 'SlotFrontNvme11linkSpeed',
        'slot_front_nvme11option_rom': 'SlotFrontNvme11optionRom',
        'slot_front_nvme12link_speed': 'SlotFrontNvme12linkSpeed',
        'slot_front_nvme12option_rom': 'SlotFrontNvme12optionRom',
        'slot_front_nvme13link_speed': 'SlotFrontNvme13linkSpeed',
        'slot_front_nvme13option_rom': 'SlotFrontNvme13optionRom',
        'slot_front_nvme14link_speed': 'SlotFrontNvme14linkSpeed',
        'slot_front_nvme14option_rom': 'SlotFrontNvme14optionRom',
        'slot_front_nvme15link_speed': 'SlotFrontNvme15linkSpeed',
        'slot_front_nvme15option_rom': 'SlotFrontNvme15optionRom',
        'slot_front_nvme16link_speed': 'SlotFrontNvme16linkSpeed',
        'slot_front_nvme16option_rom': 'SlotFrontNvme16optionRom',
        'slot_front_nvme17link_speed': 'SlotFrontNvme17linkSpeed',
        'slot_front_nvme17option_rom': 'SlotFrontNvme17optionRom',
        'slot_front_nvme18link_speed': 'SlotFrontNvme18linkSpeed',
        'slot_front_nvme18option_rom': 'SlotFrontNvme18optionRom',
        'slot_front_nvme19link_speed': 'SlotFrontNvme19linkSpeed',
        'slot_front_nvme19option_rom': 'SlotFrontNvme19optionRom',
        'slot_front_nvme1link_speed': 'SlotFrontNvme1linkSpeed',
        'slot_front_nvme1option_rom': 'SlotFrontNvme1optionRom',
        'slot_front_nvme20link_speed': 'SlotFrontNvme20linkSpeed',
        'slot_front_nvme20option_rom': 'SlotFrontNvme20optionRom',
        'slot_front_nvme21link_speed': 'SlotFrontNvme21linkSpeed',
        'slot_front_nvme21option_rom': 'SlotFrontNvme21optionRom',
        'slot_front_nvme22link_speed': 'SlotFrontNvme22linkSpeed',
        'slot_front_nvme22option_rom': 'SlotFrontNvme22optionRom',
        'slot_front_nvme23link_speed': 'SlotFrontNvme23linkSpeed',
        'slot_front_nvme23option_rom': 'SlotFrontNvme23optionRom',
        'slot_front_nvme24link_speed': 'SlotFrontNvme24linkSpeed',
        'slot_front_nvme24option_rom': 'SlotFrontNvme24optionRom',
        'slot_front_nvme2link_speed': 'SlotFrontNvme2linkSpeed',
        'slot_front_nvme2option_rom': 'SlotFrontNvme2optionRom',
        'slot_front_nvme3link_speed': 'SlotFrontNvme3linkSpeed',
        'slot_front_nvme3option_rom': 'SlotFrontNvme3optionRom',
        'slot_front_nvme4link_speed': 'SlotFrontNvme4linkSpeed',
        'slot_front_nvme4option_rom': 'SlotFrontNvme4optionRom',
        'slot_front_nvme5link_speed': 'SlotFrontNvme5linkSpeed',
        'slot_front_nvme5option_rom': 'SlotFrontNvme5optionRom',
        'slot_front_nvme6link_speed': 'SlotFrontNvme6linkSpeed',
        'slot_front_nvme6option_rom': 'SlotFrontNvme6optionRom',
        'slot_front_nvme7link_speed': 'SlotFrontNvme7linkSpeed',
        'slot_front_nvme7option_rom': 'SlotFrontNvme7optionRom',
        'slot_front_nvme8link_speed': 'SlotFrontNvme8linkSpeed',
        'slot_front_nvme8option_rom': 'SlotFrontNvme8optionRom',
        'slot_front_nvme9link_speed': 'SlotFrontNvme9linkSpeed',
        'slot_front_nvme9option_rom': 'SlotFrontNvme9optionRom',
        'slot_front_slot5link_speed': 'SlotFrontSlot5linkSpeed',
        'slot_front_slot6link_speed': 'SlotFrontSlot6linkSpeed',
        'slot_gpu1state': 'SlotGpu1state',
        'slot_gpu2state': 'SlotGpu2state',
        'slot_gpu3state': 'SlotGpu3state',
        'slot_gpu4state': 'SlotGpu4state',
        'slot_gpu5state': 'SlotGpu5state',
        'slot_gpu6state': 'SlotGpu6state',
        'slot_gpu7state': 'SlotGpu7state',
        'slot_gpu8state': 'SlotGpu8state',
        'slot_hba_link_speed': 'SlotHbaLinkSpeed',
        'slot_hba_state': 'SlotHbaState',
        'slot_lom1link': 'SlotLom1link',
        'slot_lom2link': 'SlotLom2link',
        'slot_mezz_state': 'SlotMezzState',
        'slot_mlom_link_speed': 'SlotMlomLinkSpeed',
        'slot_mlom_state': 'SlotMlomState',
        'slot_mraid_link_speed': 'SlotMraidLinkSpeed',
        'slot_mraid_state': 'SlotMraidState',
        'slot_n10state': 'SlotN10state',
        'slot_n11state': 'SlotN11state',
        'slot_n12state': 'SlotN12state',
        'slot_n13state': 'SlotN13state',
        'slot_n14state': 'SlotN14state',
        'slot_n15state': 'SlotN15state',
        'slot_n16state': 'SlotN16state',
        'slot_n17state': 'SlotN17state',
        'slot_n18state': 'SlotN18state',
        'slot_n19state': 'SlotN19state',
        'slot_n1state': 'SlotN1state',
        'slot_n20state': 'SlotN20state',
        'slot_n21state': 'SlotN21state',
        'slot_n22state': 'SlotN22state',
        'slot_n23state': 'SlotN23state',
        'slot_n24state': 'SlotN24state',
        'slot_n2state': 'SlotN2state',
        'slot_n3state': 'SlotN3state',
        'slot_n4state': 'SlotN4state',
        'slot_n5state': 'SlotN5state',
        'slot_n6state': 'SlotN6state',
        'slot_n7state': 'SlotN7state',
        'slot_n8state': 'SlotN8state',
        'slot_n9state': 'SlotN9state',
        'slot_raid_link_speed': 'SlotRaidLinkSpeed',
        'slot_raid_state': 'SlotRaidState',
        'slot_rear_nvme1link_speed': 'SlotRearNvme1linkSpeed',
        'slot_rear_nvme1state': 'SlotRearNvme1state',
        'slot_rear_nvme2link_speed': 'SlotRearNvme2linkSpeed',
        'slot_rear_nvme2state': 'SlotRearNvme2state',
        'slot_rear_nvme3link_speed': 'SlotRearNvme3linkSpeed',
        'slot_rear_nvme3state': 'SlotRearNvme3state',
        'slot_rear_nvme4link_speed': 'SlotRearNvme4linkSpeed',
        'slot_rear_nvme4state': 'SlotRearNvme4state',
        'slot_rear_nvme5state': 'SlotRearNvme5state',
        'slot_rear_nvme6state': 'SlotRearNvme6state',
        'slot_rear_nvme7state': 'SlotRearNvme7state',
        'slot_rear_nvme8state': 'SlotRearNvme8state',
        'slot_riser1link_speed': 'SlotRiser1linkSpeed',
        'slot_riser1slot1link_speed': 'SlotRiser1slot1linkSpeed',
        'slot_riser1slot2link_speed': 'SlotRiser1slot2linkSpeed',
        'slot_riser1slot3link_speed': 'SlotRiser1slot3linkSpeed',
        'slot_riser2link_speed': 'SlotRiser2linkSpeed',
        'slot_riser2slot4link_speed': 'SlotRiser2slot4linkSpeed',
        'slot_riser2slot5link_speed': 'SlotRiser2slot5linkSpeed',
        'slot_riser2slot6link_speed': 'SlotRiser2slot6linkSpeed',
        'slot_sas_state': 'SlotSasState',
        'slot_ssd_slot1link_speed': 'SlotSsdSlot1linkSpeed',
        'slot_ssd_slot2link_speed': 'SlotSsdSlot2linkSpeed',
        'smee': 'Smee',
        'smt_mode': 'SmtMode',
        'snc': 'Snc',
        'snoopy_mode_for2lm': 'SnoopyModeFor2lm',
        'snoopy_mode_for_ad': 'SnoopyModeForAd',
        'sparing_mode': 'SparingMode',
        'sr_iov': 'SrIov',
        'streamer_prefetch': 'StreamerPrefetch',
        'svm_mode': 'SvmMode',
        'terminal_type': 'TerminalType',
        'tpm_control': 'TpmControl',
        'tpm_pending_operation': 'TpmPendingOperation',
        'tpm_ppi_required': 'TpmPpiRequired',
        'tpm_support': 'TpmSupport',
        'tsme': 'Tsme',
        'txt_support': 'TxtSupport',
        'ucsm_boot_order_rule': 'UcsmBootOrderRule',
        'ufs_disable': 'UfsDisable',
        'uma_based_clustering': 'UmaBasedClustering',
        'upi_link_enablement': 'UpiLinkEnablement',
        'upi_power_management': 'UpiPowerManagement',
        'usb_emul6064': 'UsbEmul6064',
        'usb_port_front': 'UsbPortFront',
        'usb_port_internal': 'UsbPortInternal',
        'usb_port_kvm': 'UsbPortKvm',
        'usb_port_rear': 'UsbPortRear',
        'usb_port_sd_card': 'UsbPortSdCard',
        'usb_port_vmedia': 'UsbPortVmedia',
        'usb_xhci_support': 'UsbXhciSupport',
        'vga_priority': 'VgaPriority',
        'virtual_numa': 'VirtualNuma',
        'vmd_enable': 'VmdEnable',
        'vol_memory_mode': 'VolMemoryMode',
        'work_load_config': 'WorkLoadConfig',
        'x2apic_opt_out': 'X2apicOptOut',
        'xpt_prefetch': 'XptPrefetch',
        'xpt_remote_prefetch': 'XptRemotePrefetch',
    }

    # Only include parameters explicitly set by the user (non-None).
    # Unspecified BIOS parameters default to None and are omitted from the
    # API body, avoiding a full 430+ parameter payload on every request.
    for param_name, api_property in bios_property_map.items():
        if params.get(param_name) is not None:
            api_body[api_property] = params[param_name]


def main():
    argument_spec = intersight_argument_spec.copy()
    argument_spec.update(
        state={"type": "str", "choices": ['present', 'absent'], "default": "present"},
        organization={"type": "str", "default": "default"},
        name={"type": "str", "required": True},
        description={"type": "str", "aliases": ['descr']},
        tags={"type": "list", "elements": "dict"},
        acs_control_gpu1state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu2state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu3state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu4state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu5state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu6state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu7state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_gpu8state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_slot11state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_slot12state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_slot13state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        acs_control_slot14state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        adaptive_refresh_mgmt_level={
            "type": "str",
            "choices": [
                'platform-default',
                'Default',
                'Level A',
                'Level B',
                'Level C'
            ],
        },
        adjacent_cache_line_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        advanced_mem_test={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        all_usb_devices={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        altitude={
            "type": "str",
            "choices": [
                'platform-default',
                '300-m',
                '900-m',
                '1500-m',
                '3000-m',
                'auto'
            ],
        },
        aspm_support={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'Force L0s',
                'L1 Only'
            ],
        },
        assert_nmi_on_perr={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        assert_nmi_on_serr={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        auto_cc_state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        autonumous_cstate_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        baud_rate={
            "type": "str",
            "choices": [
                'platform-default',
                '9600',
                '19200',
                '38400',
                '57600',
                '115200'
            ],
        },
        bme_dma_mitigation={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        boot_option_num_retry={
            "type": "str",
            "choices": [
                'platform-default',
                '5',
                '13',
                'Infinite'
            ],
        },
        boot_option_re_cool_down={
            "type": "str",
            "choices": [
                'platform-default',
                '15',
                '45',
                '90'
            ],
        },
        boot_option_retry={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        boot_performance_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'Max Efficient',
                'Max Performance',
                'Set by Intel NM'
            ],
        },
        burst_and_postponed_refresh={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        c1auto_demotion={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        c1auto_un_demotion={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cbs_cmn_apbdis={
            "type": "str",
            "choices": [
                'platform-default',
                '0',
                '1',
                'Auto'
            ],
        },
        cbs_cmn_cpu_cpb={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled'
            ],
        },
        cbs_cmn_cpu_gen_downcore_ctrl={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'FOUR (2 + 2)',
                'FOUR (4 + 0)',
                'SIX (3 + 3)',
                'THREE (3 + 0)',
                'TWO (1 + 1)',
                'TWO (2 + 0)'
            ],
        },
        cbs_cmn_cpu_global_cstate_ctrl={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_cpu_l1stream_hw_prefetcher={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_cpu_l2stream_hw_prefetcher={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_cpu_smee={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_cpu_streaming_stores_ctrl={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmnc_tdp_ctl={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Manual'
            ],
        },
        cbs_cmn_determinism_slider={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Performance',
                'Power'
            ],
        },
        cbs_cmn_efficiency_mode_en={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Enabled'
            ],
        },
        cbs_cmn_fixed_soc_pstate={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'P0',
                'P1',
                'P2',
                'P3'
            ],
        },
        cbs_cmn_gnb_nb_iommu={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_gnb_smucppc={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_gnb_smu_df_cstates={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_mem_ctrl_bank_group_swap_ddr4={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_cmn_mem_map_bank_interleave_ddr4={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled'
            ],
        },
        cbs_cpu_ccd_ctrl_ssp={
            "type": "str",
            "choices": [
                'platform-default',
                '2 CCDs',
                '3 CCDs',
                '4 CCDs',
                '6 CCDs',
                'Auto'
            ],
        },
        cbs_cpu_core_ctrl={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'FIVE (5 + 0)',
                'FOUR (4 + 0)',
                'ONE (1 + 0)',
                'SEVEN (7 + 0)',
                'SIX (6 + 0)',
                'THREE (3 + 0)',
                'TWO (2 + 0)'
            ],
        },
        cbs_cpu_smt_ctrl={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_dbg_cpu_snp_mem_cover={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Custom',
                'disabled',
                'enabled'
            ],
        },
        cbs_dbg_cpu_snp_mem_size_cover={
            "type": "str",
        },
        cbs_df_cmn_acpi_srat_l3numa={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        cbs_df_cmn_dram_nps={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'NPS0',
                'NPS1',
                'NPS2',
                'NPS4'
            ],
        },
        cbs_df_cmn_mem_intlv={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Channel',
                'Die',
                'None',
                'Socket'
            ],
        },
        cbs_df_cmn_mem_intlv_size={
            "type": "str",
            "choices": [
                'platform-default',
                '256 Bytes',
                '512 Bytes',
                '1 KB',
                '2 KB',
                '4 KB',
                'Auto'
            ],
        },
        cbs_sev_snp_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cdn_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cdn_support={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'LOMs Only'
            ],
        },
        channel_inter_leave={
            "type": "str",
            "choices": [
                'platform-default',
                '1-way',
                '2-way',
                '3-way',
                '4-way',
                'auto'
            ],
        },
        cisco_adaptive_mem_training={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cisco_debug_level={
            "type": "str",
            "choices": [
                'platform-default',
                'Maximum',
                'Minimum',
                'Normal'
            ],
        },
        cisco_oprom_launch_optimization={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cisco_xgmi_max_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cke_low_policy={
            "type": "str",
            "choices": [
                'platform-default',
                'auto',
                'disabled',
                'fast',
                'slow'
            ],
        },
        closed_loop_therm_throtl={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cmci_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        config_tdp={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        config_tdp_level={
            "type": "str",
            "choices": [
                'platform-default',
                'Level 1',
                'Level 2',
                'Normal'
            ],
        },
        console_redirection={
            "type": "str",
            "choices": [
                'platform-default',
                'com-0',
                'com-1',
                'disabled',
                'enabled',
                'serial-port-a'
            ],
        },
        core_multi_processing={
            "type": "str",
            "choices": [
                'platform-default',
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9',
                '10',
                '11',
                '12',
                '13',
                '14',
                '15',
                '16',
                '17',
                '18',
                '19',
                '20',
                '21',
                '22',
                '23',
                '24',
                '25',
                '26',
                '27',
                '28',
                '29',
                '30',
                '31',
                '32',
                '33',
                '34',
                '35',
                '36',
                '37',
                '38',
                '39',
                '40',
                '41',
                '42',
                '43',
                '44',
                '45',
                '46',
                '47',
                '48',
                '49',
                '50',
                '51',
                '52',
                '53',
                '54',
                '55',
                '56',
                '57',
                '58',
                '59',
                '60',
                '61',
                '62',
                '63',
                '64',
                'all'
            ],
        },
        cpu_energy_performance={
            "type": "str",
            "choices": [
                'platform-default',
                'balanced-energy',
                'balanced-performance',
                'balanced-power',
                'energy-efficient',
                'performance',
                'power'
            ],
        },
        cpu_frequency_floor={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cpu_pa_limit={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        cpu_perf_enhancement={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled'
            ],
        },
        cpu_performance={
            "type": "str",
            "choices": [
                'platform-default',
                'custom',
                'enterprise',
                'high-throughput',
                'hpc'
            ],
        },
        cpu_power_management={
            "type": "str",
            "choices": [
                'platform-default',
                'custom',
                'disabled',
                'energy-efficient',
                'performance'
            ],
        },
        crfastgo_config={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Default',
                'Disable optimization',
                'Enable optimization',
                'Option 1',
                'Option 2',
                'Option 3',
                'Option 4',
                'Option 5'
            ],
        },
        cr_qos={
            "type": "str",
            "choices": [
                'platform-default',
                'Disabled',
                'Mode 0 - Disable the PMem QoS Feature',
                'Mode 1 - M2M QoS Enable and CHA QoS Disable',
                'Mode 2 - M2M QoS Enable and CHA QoS Enable',
                'Profile 1',
                'Recipe 1',
                'Recipe 2',
                'Recipe 3'
            ],
        },
        dcpmm_firmware_downgrade={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        demand_scrub={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        direct_cache_access={
            "type": "str",
            "choices": [
                'platform-default',
                'auto',
                'disabled',
                'enabled'
            ],
        },
        dma_ctrl_opt_in={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        dram_clock_throttling={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Balanced',
                'Energy Efficient',
                'Performance'
            ],
        },
        dram_refresh_rate={
            "type": "str",
            "choices": [
                'platform-default',
                '1x',
                '2x',
                '3x',
                '4x',
                'Auto'
            ],
        },
        dram_sw_thermal_throttling={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        eadr_support={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        edpc_en={
            "type": "str",
            "choices": [
                'platform-default',
                'Disabled',
                'On Fatal Error',
                'On Fatal and Non-Fatal Errors'
            ],
        },
        enable_clock_spread_spec={
            "type": "str",
            "choices": [
                'platform-default',
                '0P3_Percent',
                '0P5_Percent',
                'disabled',
                'enabled',
                'Hardware',
                'Off'
            ],
        },
        enable_mktme={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        enable_rmt={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        enable_sgx={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        enable_tme={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        energy_efficient_turbo={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        eng_perf_tuning={
            "type": "str",
            "choices": [
                'platform-default',
                'BIOS',
                'OS'
            ],
        },
        enhanced_intel_speed_step_tech={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        epoch_update={
            "type": "str",
            "choices": [
                'platform-default',
                'Change to New Random Owner EPOCHs',
                'Manual User Defined Owner EPOCHs',
                'SGX Owner EPOCH activated'
            ],
        },
        epp_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        epp_profile={
            "type": "str",
            "choices": [
                'platform-default',
                'Balanced Performance',
                'Balanced Power',
                'Performance',
                'Power'
            ],
        },
        error_check_scrub={
            "type": "str",
            "choices": [
                'platform-default',
                'Disabled',
                'Enabled with Result Collection',
                'Enabled without Result Collection'
            ],
        },
        execute_disable_bit={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        extended_apic={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'X2APIC',
                'XAPIC'
            ],
        },
        flow_control={
            "type": "str",
            "choices": [
                'platform-default',
                'none',
                'rts-cts'
            ],
        },
        frb2enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        hardware_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        hwpm_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'Disabled',
                'HWPM Native Mode',
                'HWPM OOB Mode',
                'NATIVE MODE',
                'Native Mode with no Legacy',
                'OOB MODE'
            ],
        },
        imc_interleave={
            "type": "str",
            "choices": [
                'platform-default',
                '1-way Interleave',
                '2-way Interleave',
                'Auto'
            ],
        },
        intel_dynamic_speed_select={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_hyper_threading_tech={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_speed_select={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Base',
                'Config 1',
                'Config 2',
                'Config 3',
                'Config 4'
            ],
        },
        intel_turbo_boost_tech={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_virtualization_technology={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_vtdats_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_vtd_coherency_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_vtd_interrupt_remapping={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_vtd_pass_through_dma_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        intel_vt_for_directed_io={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        ioh_error_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'No',
                'Yes'
            ],
        },
        ioh_resource={
            "type": "str",
            "choices": [
                'platform-default',
                'IOH0 24k IOH1 40k',
                'IOH0 32k IOH1 32k',
                'IOH0 40k IOH1 24k',
                'IOH0 48k IOH1 16k',
                'IOH0 56k IOH1 8k'
            ],
        },
        ip_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        ipv4http={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        ipv4pxe={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        ipv6http={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        ipv6pxe={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        kti_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        legacy_os_redirection={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        legacy_usb_support={
            "type": "str",
            "choices": [
                'platform-default',
                'auto',
                'disabled',
                'enabled'
            ],
        },
        llc_alloc={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        llc_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        lom_port0state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        lom_port1state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        lom_port2state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        lom_port3state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        lom_ports_all_state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        lv_ddr_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'auto',
                'performance-mode',
                'power-saving-mode'
            ],
        },
        make_device_non_bootable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        memory_bandwidth_boost={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        memory_inter_leave={
            "type": "str",
            "choices": [
                'platform-default',
                '1 Way Node Interleave',
                '2 Way Node Interleave',
                '4 Way Node Interleave',
                '8 Way Node Interleave',
                'disabled',
                'enabled'
            ],
        },
        memory_mapped_io_above4gb={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        memory_refresh_rate={
            "type": "str",
            "choices": [
                'platform-default',
                '1x Refresh',
                '2x Refresh'
            ],
        },
        memory_size_limit={
            "type": "str",
        },
        memory_thermal_throttling={
            "type": "str",
            "choices": [
                'platform-default',
                'CLTT with PECI',
                'Disabled'
            ],
        },
        mirroring_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'inter-socket',
                'intra-socket'
            ],
        },
        mmcfg_base={
            "type": "str",
            "choices": [
                'platform-default',
                '1 GB',
                '2 GB',
                '2.5 GB',
                '3 GB',
                'Auto'
            ],
        },
        network_stack={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        numa_optimized={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        nvmdimm_perform_config={
            "type": "str",
            "choices": [
                'platform-default',
                'BW Optimized',
                'Balanced Profile',
                'Latency Optimized'
            ],
        },
        onboard10gbit_lom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        onboard_gbit_lom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        onboard_scu_storage_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        onboard_scu_storage_sw_stack={
            "type": "str",
            "choices": [
                'platform-default',
                'Intel RSTe',
                'LSI SW RAID'
            ],
        },
        operation_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'Test Only',
                'Test and Repair'
            ],
        },
        os_boot_watchdog_timer={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        os_boot_watchdog_timer_policy={
            "type": "str",
            "choices": [
                'platform-default',
                'do-nothing',
                'power-off',
                'reset'
            ],
        },
        os_boot_watchdog_timer_timeout={
            "type": "str",
            "choices": [
                'platform-default',
                '5-minutes',
                '10-minutes',
                '15-minutes',
                '20-minutes'
            ],
        },
        out_of_band_mgmt_port={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        package_cstate_limit={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'C0 C1 State',
                'C0/C1',
                'C2',
                'C6 Non Retention',
                'C6 Retention',
                'No Limit'
            ],
        },
        panic_high_watermark={
            "type": "str",
            "choices": [
                'platform-default',
                'High',
                'Low'
            ],
        },
        partial_cache_line_sparing={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        partial_mirror_mode_config={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'Percentage',
                'Value in GB'
            ],
        },
        partial_mirror_percent={
            "type": "str",
        },
        partial_mirror_value1={
            "type": "str",
        },
        partial_mirror_value2={
            "type": "str",
        },
        partial_mirror_value3={
            "type": "str",
        },
        partial_mirror_value4={
            "type": "str",
        },
        patrol_scrub={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'Enable at End of POST',
                'enabled'
            ],
        },
        patrol_scrub_duration={
            "type": "str",
        },
        pch_pcie_pll_ssc={
            "type": "str",
        },
        pch_usb30mode={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_ari_support={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        pcie_pll_ssc={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'ZeroPointFive'
            ],
        },
        pc_ie_ras_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_mraid1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        pcie_slot_mraid1option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_mraid2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        pcie_slot_mraid2option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_mstorraid_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4'
            ],
        },
        pcie_slot_mstorraid_option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_nvme1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        pcie_slot_nvme1option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_nvme2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        pcie_slot_nvme2option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_nvme3link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        pcie_slot_nvme3option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_nvme4link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        pcie_slot_nvme4option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_nvme5link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        pcie_slot_nvme5option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slot_nvme6link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        pcie_slot_nvme6option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pcie_slots_cdn_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pc_ie_ssd_hot_plug_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pci_option_ro_ms={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        pci_rom_clp={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        pop_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        post_error_pause={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        post_package_repair={
            "type": "str",
            "choices": [
                'platform-default',
                'Disabled',
                'Hard PPR'
            ],
        },
        processor_c1e={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        processor_c3report={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        processor_c6report={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        processor_cstate={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        psata={
            "type": "str",
            "choices": [
                'platform-default',
                'AHCI',
                'Disabled',
                'LSI SW RAID'
            ],
        },
        pstate_coord_type={
            "type": "str",
            "choices": [
                'platform-default',
                'HW ALL',
                'SW ALL',
                'SW ANY'
            ],
        },
        putty_key_pad={
            "type": "str",
            "choices": [
                'platform-default',
                'ESCN',
                'LINUX',
                'SCO',
                'VT100',
                'VT400',
                'XTERMR6'
            ],
        },
        pwr_perf_tuning={
            "type": "str",
            "choices": [
                'platform-default',
                'bios',
                'os',
                'peci'
            ],
        },
        qpi_link_frequency={
            "type": "str",
            "choices": [
                'platform-default',
                '6.4-gt/s',
                '7.2-gt/s',
                '8.0-gt/s',
                '9.6-gt/s',
                'auto'
            ],
        },
        qpi_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                '10.4GT/s',
                '11.2GT/s',
                '12.8GT/s',
                '14.4GT/s',
                '16.0GT/s',
                '9.6GT/s',
                'Auto'
            ],
        },
        qpi_snoop_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'auto',
                'cluster-on-die',
                'early-snoop',
                'home-directory-snoop',
                'home-directory-snoop-with-osb',
                'home-snoop'
            ],
        },
        rank_inter_leave={
            "type": "str",
            "choices": [
                'platform-default',
                '1-way',
                '2-way',
                '4-way',
                '8-way',
                'auto'
            ],
        },
        redirection_after_post={
            "type": "str",
            "choices": [
                'platform-default',
                'Always Enable',
                'Bootloader'
            ],
        },
        sata_mode_select={
            "type": "str",
            "choices": [
                'platform-default',
                'AHCI',
                'Disabled',
                'LSI SW RAID'
            ],
        },
        select_memory_ras_configuration={
            "type": "str",
            "choices": [
                'platform-default',
                'adddc-sparing',
                'lockstep',
                'maximum-performance',
                'mirror-mode-1lm',
                'mirroring',
                'partial-mirror-mode-1lm',
                'sparing'
            ],
        },
        select_ppr_type={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'Hard PPR',
                'Soft PPR'
            ],
        },
        serial_port_aenable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sev={
            "type": "str",
            "choices": [
                'platform-default',
                '253 ASIDs',
                '509 ASIDs',
                'Auto'
            ],
        },
        sgx_auto_registration_agent={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sgx_epoch0={
            "type": "str",
        },
        sgx_epoch1={
            "type": "str",
        },
        sgx_factory_reset={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sgx_le_pub_key_hash0={
            "type": "str",
        },
        sgx_le_pub_key_hash1={
            "type": "str",
        },
        sgx_le_pub_key_hash2={
            "type": "str",
        },
        sgx_le_pub_key_hash3={
            "type": "str",
        },
        sgx_le_wr={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sgx_package_info_in_band_access={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sgx_qos={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sha1pcr_bank={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sha256pcr_bank={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        single_pctl_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'No',
                'Yes'
            ],
        },
        slot10link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot10state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot11link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot11state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot12link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot12state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot13state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot14state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot1state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot2state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot3link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot3state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot4link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot4state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot5link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot5state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot6link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot6state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot7link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot7state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot8link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot8state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot9link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4'
            ],
        },
        slot9state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_flom_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_front_nvme10link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme10option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme11link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme11option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme12link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme12option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme13link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme13option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme14link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme14option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme15link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme15option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme16link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme16option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme17link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme17option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme18link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme18option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme19link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme19option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme1option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme20link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme20option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme21link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme21option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme22link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme22option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme23link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme23option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme24link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme24option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme2option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme3link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme3option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme4link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme4option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme5link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme5option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme6link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme6option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme7link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme7option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme8link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme8option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_nvme9link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_front_nvme9option_rom={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_front_slot5link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_front_slot6link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_gpu1state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu2state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu3state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu4state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu5state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu6state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu7state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_gpu8state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_hba_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_hba_state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_lom1link={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_lom2link={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_mezz_state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_mlom_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_mlom_state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_mraid_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_mraid_state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n10state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n11state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n12state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n13state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n14state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n15state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n16state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n17state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n18state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n19state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n1state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_n20state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n21state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n22state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n23state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n24state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n2state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_n3state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n4state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n5state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n6state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n7state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n8state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_n9state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_raid_link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_raid_state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_rear_nvme1state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_rear_nvme2state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme3link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_rear_nvme3state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme4link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3',
                'GEN4',
                'GEN5'
            ],
        },
        slot_rear_nvme4state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme5state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme6state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme7state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_rear_nvme8state={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        slot_riser1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser1slot1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser1slot2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser1slot3link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser2slot4link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser2slot5link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_riser2slot6link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_sas_state={
            "type": "str",
            "choices": [
                'platform-default',
                'disabled',
                'enabled',
                'Legacy Only',
                'UEFI Only'
            ],
        },
        slot_ssd_slot1link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        slot_ssd_slot2link_speed={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Disabled',
                'GEN1',
                'GEN2',
                'GEN3'
            ],
        },
        smee={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        smt_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'Off'
            ],
        },
        snc={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled',
                'SNC2',
                'SNC4'
            ],
        },
        snoopy_mode_for2lm={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        snoopy_mode_for_ad={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        sparing_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'dimm-sparing',
                'rank-sparing'
            ],
        },
        sr_iov={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        streamer_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        svm_mode={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        terminal_type={
            "type": "str",
            "choices": [
                'platform-default',
                'pc-ansi',
                'vt100',
                'vt100-plus',
                'vt-utf8'
            ],
        },
        tpm_control={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        tpm_pending_operation={
            "type": "str",
            "choices": [
                'platform-default',
                'None',
                'TpmClear'
            ],
        },
        tpm_ppi_required={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        tpm_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        tsme={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        txt_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        ucsm_boot_order_rule={
            "type": "str",
            "choices": [
                'platform-default',
                'Loose',
                'Strict'
            ],
        },
        ufs_disable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        uma_based_clustering={
            "type": "str",
            "choices": [
                'platform-default',
                'Disable (All2All)',
                'Hemisphere (2-clusters)',
                'Quadrant (4-clusters)'
            ],
        },
        upi_link_enablement={
            "type": "str",
            "choices": [
                'platform-default',
                '1',
                '2',
                '3',
                'Auto'
            ],
        },
        upi_power_management={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_emul6064={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_port_front={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_port_internal={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_port_kvm={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_port_rear={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_port_sd_card={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_port_vmedia={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        usb_xhci_support={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        vga_priority={
            "type": "str",
            "choices": [
                'platform-default',
                'Offboard',
                'Onboard',
                'Onboard VGA Disabled'
            ],
        },
        virtual_numa={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        vmd_enable={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        vol_memory_mode={
            "type": "str",
            "choices": [
                'platform-default',
                '1LM',
                '2LM'
            ],
        },
        work_load_config={
            "type": "str",
            "choices": [
                'platform-default',
                'Balanced',
                'I/O Sensitive',
                'NUMA',
                'UMA'
            ],
        },
        x2apic_opt_out={
            "type": "str",
            "choices": [
                'platform-default',
                'enabled',
                'disabled'
            ],
        },
        xpt_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
        xpt_remote_prefetch={
            "type": "str",
            "choices": [
                'platform-default',
                'Auto',
                'disabled',
                'enabled'
            ],
        },
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    intersight = IntersightModule(module)
    intersight.result['api_response'] = {}
    intersight.result['trace_id'] = ''

    # Resource path used to configure policy
    resource_path = '/bios/Policies'
    # Define API body used in compares or create
    intersight.api_body = {
        'Name': intersight.module.params['name'],
        'Organization': {
            'Name': intersight.module.params['organization']
        }
    }
    intersight.set_tags_and_description()

    # Apply all BIOS properties using the property mapping
    apply_bios_properties(intersight.module.params, intersight.api_body)

    intersight.configure_policy_or_profile(resource_path=resource_path)

    module.exit_json(**intersight.result)


if __name__ == '__main__':
    main()
