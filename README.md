# Ansible Collection - cisco.intersight

Documentation for the collection.# intersight-ansible
* Ansible Modules for Cisco Intersight.
* Apache License, Version 2.0 (the "License") 

## News

This repo represents the working copy of modules for Cisco Intersight that will submitted to Ansible in the future.  This repo can be used to provide Cisco Intersight modules before their inclusion in official Ansible releases.

There is currently not support for scripted install/uninstall to avoid collision with Ansible hosted modules and ongoing maintenance.  If you are running playbooks from the top-level directory of this repository (with library and module_utils subdirectories) you should not need any other setup to use the modules.

If needed, you can specfiy this repo as a library and module_utils location with env variables or command line options (e.g., ANSIBLE_LIBRARY=./library ansible-playbook ..).  Alternatively, your .ansible.cfg file can be updated to use this repo as the library path and module_utils path with the following:
```
[defaults]
library = <path to intersight-ansible clone>/library
module_utils = <path to intersight-ansible clone>/module_utils
```

### Current Development Status

| Configuration Category | Configuration Task | Module Name | Status (planned for Ansible 2.6, Proof of Concept, TBD |
| ---------------------- | ------------------ | ----------- | ------ |
| General purpose resource config | Any (with user provided data) | intersight_rest_api | Planned for 2.8 |
| Resource data collection/inventory | GET servers information | intersight_facts | Planned for 2.8 |

### Ansible Development Notes

Modules in development follow processes documented at http://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html.  The modules support ansible-doc, and when submitted to Ansible they must pass Ansible CI testing and have integration tests.

When developing modules in this repository, here are a few helpful commands to sanity check the code and documentation (replace module_name with your module (e.g., intersight_objects)).  Ansible modules won't generally be pylint or pycodestyle (PEP8) clean without disabling several of the checks:
  ```
  pylint --disable=invalid-name,no-member,too-many-nested-blocks,redefined-variable-type,too-many-statements,too-many-branches,broad-except,line-too-long,missing-docstring,wrong-import-position,too-many-locals,import-error <module_name>.py
  
  pycodestyle --max-line-length 160 --config /dev/null --ignore E402 <module_name>.py
  
  ansible-doc <module_name>
  ```

### Install
- ansible must be installed
```
sudo pip install ansible
```
- clone this repository 
```
git clone https://github.com/ciscoucs/intersight-ansible
```

### Usage

Authentication with the Intersight API requires the use of API keys that should be generated within the Intersight UI.  See (https://intersight.com/help) or (https://communities.cisco.com/docs/DOC-76947) for more information on generating and using API keys.
If you do not have an Intersight account, you can create one and claim devices in Intersight using the DevNet Intersight Sandbox at https://devnetsandbox.cisco.com/RM/Diagram/Index/a63216d2-e891-4856-9f27-309ca61ec862?diagramType=Topology
Because Intersight has a single API endpoint, minimal setup is required in playbooks or variables to access the API.  Here's an example playbook:
```
---
- hosts: localhost
  connection: local
  gather_facts: false
  tasks:
  - name: Configure Boot Policy
    intersight_rest_api:
      api_private_key: <path to your private key>
      api_key_id: <your public key id>
      resource_path: /boot/PrecisionPolicies
      api_body: {
```

localhost (the Ansible controller) can be used without the need to specify any hosts or inventory.  Hosts can be specified to perform parallel actions.  An example of Server Firmware Update on multiple servers is provided by the server_firmware.yml playbook.

If you're using playbooks in this repo, you will need to provide your own inventory file and cusomtize any variables used in playbooks with settings for your environment.  This repo includes an example_inventory file with host groups for HX Clusters (Intersight_HX) and Servers (Intersight_Servers) and API key variables shared for Intersight host groups:
```
[Intersight_HX]
sjc07-r13-501
sjc07-r13-503

[Intersight_Servers]

[Intersight:children]
Intersight_HX
Intersight_Servers

[Intersight:vars]
api_private_key=~/Downloads/SecretKey.txt
api_key_id=...
```
For demo purposes, you can copy the example_inventory file to a new file named inventory.  Then, edit the inventory file to provide your own api_private_key location and api_key_id for use in playbooks.  If you're are using the Intersight Virtual Appliance, your inventory file can also specify the appliance URI and use of local certificates:
```
api_uri=https://tme-appliance2.intersightdemo.cisco.com/api/v1
validate_certs=false
```

Once you've provided API key information, the inventory file can be automatically updated with data from your Intersight account using one of the following playbooks:
- update_all_inventory.yml (if you'd like all Servers in the inventory)
- update_standalone_inventory.yml (if you'd like only Standalone C-Series Servers that can be managed through Server Policies/Profiles)

Here are example command lines for creating your own inventory and running the update_standalone_inventory.yml playbook:
```
cp example_inventory inventory
edit inventory with your api_private_key and api_key_id
ansible-playbook -i inventory update_standalone_inventory.yml
```
With an inventory for your Intersight account, you can now run playbooks to configure profiles/policies, and perform other server actions in Intersight:
```
ansible-playbook -i inventory cos_server_policies_and_profiles.yml --list-tasks --list-hosts (will show the tasks and their tags along with the hosts that will be configured)
ansible-playbook -i inventory cos_server_policies_and_profiles.yml (will configure policies and profiles in Intersight)
ansible-playbook -i inventory deploy_server_profiles.yml (note: this will deploy settings, run with --check to see what would change 1st)
ansible-playbook -i inventory server_actions.yml (note: by default this will PowerOn all servers, view the playbook to see other options)
```

Here are example command lines for creating an inventory with all Servers and getting detailed server information:
```
cp example_inventory inventory
edit inventory with your api_private_key and api_key_id
ansible-playbook -i inventory update_all_inventory.yml
ansible-playbook -i inventory get_server_details.yml
```
The get_server_details.yml file will create a JSON file with server details for each server in the inventory (saved to a local .json file)
# Community:

* We are on Slack (https://ciscoucs.slack.com/) - Slack requires registration, but the ucspython team is open invitation to
  anyone.  Click [here](https://ucspython.herokuapp.com) to register 
