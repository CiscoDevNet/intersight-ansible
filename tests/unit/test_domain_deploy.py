import unittest
from unittest.mock import MagicMock, patch

from ansible_collections.cisco.intersight.plugins.modules import intersight_domain as domain


class ModuleFailure(Exception):
    pass


class ModuleExit(Exception):
    pass


def make_intersight(check_mode=False, state='Assigned', action='No-op'):
    intersight = MagicMock()
    intersight.module.check_mode = check_mode
    intersight.module.params = {'wait_for_action': True, 'action_timeout': 120, 'action_poll_interval': 10}
    intersight.module.fail_json.side_effect = ModuleFailure
    intersight.result = {'changed': False, 'api_response': {}}
    profiles = [
        {'Moid': 'switch-' + fi, 'Name': 'domain-' + fi, 'SwitchId': fi,
         'AssignedSwitch': {'Moid': 'fi-' + fi},
         'ConfigContext': {'ConfigState': state, 'ControlAction': action}}
        for fi in ('A', 'B')
    ]
    intersight.call_api.return_value = {'Results': profiles}
    return intersight, profiles


class TestDeployDomain(unittest.TestCase):
    @patch.object(domain, 'wait_for_switch_deployment')
    def test_check_mode_only_reads_and_reports_changes(self, wait):
        intersight, profiles = make_intersight(check_mode=True)
        domain.deploy_domain_profile(intersight, 'cluster-1')
        self.assertTrue(intersight.result['changed'])
        self.assertEqual(intersight.result['switch_profiles'], profiles)
        intersight.call_api.assert_called_once_with(
            http_method='get', resource_path='/fabric/SwitchProfiles',
            query_params={'$filter': "SwitchClusterProfile.Moid eq 'cluster-1'"},
        )
        wait.assert_not_called()

    @patch.object(domain, 'wait_for_switch_deployment')
    def test_check_mode_does_not_wait_for_active_deployment(self, wait):
        intersight, _ = make_intersight(check_mode=True, state='Configuring', action='Deploy')
        domain.deploy_domain_profile(intersight, 'cluster-1')
        self.assertTrue(intersight.result['changed'])
        self.assertEqual(intersight.call_api.call_count, 1)
        wait.assert_not_called()

    def test_associated_is_idempotent(self):
        intersight, _ = make_intersight(state='Associated')
        domain.deploy_domain_profile(intersight, 'cluster-1')
        self.assertFalse(intersight.result['changed'])
        self.assertEqual(intersight.call_api.call_count, 1)

    def test_configuration_changes_require_deployment(self):
        intersight, _ = make_intersight(check_mode=True, state='Associated')
        domain.deploy_domain_profile(intersight, 'cluster-1', configuration_changed=True)
        self.assertTrue(intersight.result['changed'])

    @patch.object(domain, 'wait_for_switch_deployment')
    def test_deploys_both_switches_and_waits(self, wait):
        intersight, profiles = make_intersight()
        wait.side_effect = profiles
        domain.deploy_domain_profile(intersight, 'cluster-1')
        patches = [c.kwargs for c in intersight.call_api.call_args_list if c.kwargs['http_method'] == 'patch']
        self.assertEqual(patches, [
            {'http_method': 'patch', 'resource_path': '/fabric/SwitchProfiles',
             'moid': 'switch-' + fi, 'body': {'Action': 'Deploy'}} for fi in ('A', 'B')
        ])
        self.assertEqual(wait.call_count, 2)
        self.assertTrue(intersight.result['changed'])

    @patch.object(domain, 'wait_for_switch_deployment')
    def test_no_wait(self, wait):
        intersight, _ = make_intersight()
        intersight.module.params['wait_for_action'] = False
        domain.deploy_domain_profile(intersight, 'cluster-1')
        wait.assert_not_called()
        self.assertTrue(intersight.result['changed'])

    @patch.object(domain, 'wait_for_switch_deployment')
    def test_active_deploy_is_not_resubmitted(self, wait):
        intersight, profiles = make_intersight(state='Configuring', action='Deploy')
        wait.side_effect = profiles
        domain.deploy_domain_profile(intersight, 'cluster-1')
        self.assertEqual(intersight.call_api.call_count, 1)
        self.assertEqual(wait.call_count, 2)

    def test_missing_assignment_fails_before_any_patch(self):
        intersight, profiles = make_intersight()
        profiles[1]['AssignedSwitch'] = None
        with self.assertRaises(ModuleFailure):
            domain.deploy_domain_profile(intersight, 'cluster-1')
        self.assertEqual(intersight.call_api.call_count, 1)

    def test_missing_switch_profile_fails(self):
        intersight, _ = make_intersight()
        intersight.call_api.return_value = {'Results': []}
        with self.assertRaises(ModuleFailure):
            domain.deploy_domain_profile(intersight, 'cluster-1')
        self.assertEqual(intersight.call_api.call_count, 1)


class TestWaitForDeployment(unittest.TestCase):
    def test_associated_completes(self):
        intersight, profiles = make_intersight(state='Associated')
        intersight.call_api.return_value = profiles[0]
        self.assertEqual(domain.wait_for_switch_deployment(intersight, 'switch-A', 120, 10), profiles[0])

    def test_failure_includes_response(self):
        intersight, profiles = make_intersight(state='Failed')
        intersight.call_api.return_value = profiles[0]
        with self.assertRaises(ModuleFailure):
            domain.wait_for_switch_deployment(intersight, 'switch-A', 120, 10)
        self.assertEqual(intersight.module.fail_json.call_args.kwargs['api_response'], profiles[0])

    @patch.object(domain.time, 'sleep')
    @patch.object(domain.time, 'monotonic', side_effect=[0, 10, 120])
    def test_timeout_and_polling(self, monotonic, sleep):
        intersight, profiles = make_intersight(state='Configuring', action='Deploy')
        intersight.call_api.return_value = profiles[0]
        with self.assertRaises(ModuleFailure):
            domain.wait_for_switch_deployment(intersight, 'switch-A', 120, 10)
        sleep.assert_called_once_with(10)
        self.assertIn('Timed out', intersight.module.fail_json.call_args.kwargs['msg'])


class TestMain(unittest.TestCase):
    def run_main(self, check_mode=True, found=True, organization_found=True, **overrides):
        module = MagicMock()
        module.check_mode = check_mode
        module.params = dict(state='present', name='domain', organization='org', action='Deploy',
                             wait_for_action=True, action_timeout=120, action_poll_interval=10,
                             system_qos_policy=None)
        module.params.update(overrides)
        module.fail_json.side_effect = ModuleFailure
        module.exit_json.side_effect = ModuleExit
        intersight = MagicMock()
        intersight.result = {'changed': False, 'api_response': {}}
        intersight.get_moid_by_name.return_value = 'org-1' if organization_found else None

        def get_resource(**kwargs):
            intersight.result['api_response'] = {'Moid': 'cluster-1', 'Name': 'domain'} if found else {}

        intersight.get_resource.side_effect = get_resource
        intersight.configure_policy_or_profile.return_value = None
        with patch.object(domain, 'AnsibleModule', return_value=module), \
                patch.object(domain, 'IntersightModule', return_value=intersight), \
                patch.object(domain, 'deploy_domain_profile') as deploy:
            try:
                domain.main()
            except (ModuleExit, ModuleFailure):
                pass
        return module, intersight, deploy

    def test_deploy_only_preserves_configuration(self):
        module, intersight, deploy = self.run_main()
        intersight.configure_policy_or_profile.assert_not_called()
        deploy.assert_called_once_with(intersight, 'cluster-1')
        self.assertEqual(module.exit_json.call_args.kwargs['api_response']['Moid'], 'cluster-1')
        self.assertIn("Organization.Moid eq 'org-1'", intersight.get_resource.call_args.kwargs['query_params']['$filter'])

    def test_missing_domain_fails_without_creating(self):
        module, intersight, deploy = self.run_main(found=False)
        self.assertIn("not found", module.fail_json.call_args.kwargs['msg'])
        intersight.configure_policy_or_profile.assert_not_called()
        deploy.assert_not_called()

    def test_missing_organization_fails(self):
        module, intersight, deploy = self.run_main(organization_found=False)
        self.assertIn("Organization", module.fail_json.call_args.kwargs['msg'])
        intersight.get_resource.assert_not_called()
        deploy.assert_not_called()

    def test_check_mode_new_domain_skips_deployment(self):
        module, intersight, deploy = self.run_main(system_qos_policy='qos')
        intersight.configure_policy_or_profile.assert_called_once()
        deploy.assert_not_called()
        module.exit_json.assert_called_once()

    def test_configuration_still_requires_qos(self):
        module, intersight, deploy = self.run_main(description='updated')
        module.fail_json.assert_called_once()
        intersight.configure_policy_or_profile.assert_not_called()
        deploy.assert_not_called()

    def test_action_rejects_absent(self):
        module, _, deploy = self.run_main(state='absent')
        module.fail_json.assert_called_once_with(msg='action requires state=present.')
        deploy.assert_not_called()

    def test_poll_interval_must_be_positive(self):
        module, _, deploy = self.run_main(action_poll_interval=0)
        module.fail_json.assert_called_once_with(msg='action_timeout and action_poll_interval must be positive.')
        deploy.assert_not_called()


if __name__ == '__main__':
    unittest.main()
