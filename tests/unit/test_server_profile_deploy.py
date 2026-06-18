import unittest
from unittest.mock import patch, MagicMock

from ansible_collections.cisco.intersight.plugins.modules import intersight_server_profile as server_profile_module
from ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile import (
    wait_for_profile_action,
    get_deploy_failure_reason,
    perform_profile_action,
    perform_unassign,
    perform_attach,
    perform_detach,
)


class FailJsonException(Exception):
    pass


class ExitJsonException(Exception):
    pass


def make_intersight_mock(check_mode=False):
    """Create a mock IntersightModule with the minimum interface needed for testing."""
    module = MagicMock()
    module.check_mode = check_mode
    module.params = {}
    module.fail_json.side_effect = FailJsonException
    intersight = MagicMock()
    intersight.module = module
    intersight.result = {'changed': False, 'api_response': {}}
    return intersight


def make_profile_response(control_action='No-op', config_state='Associated', oper_state='Ok', moid='test-moid-123'):
    """Build a mock API response for a server profile."""
    return {
        'Results': [{
            'Moid': moid,
            'Name': 'test-profile',
            'ConfigContext': {
                'ControlAction': control_action,
                'ConfigState': config_state,
                'OperState': oper_state,
            },
        }],
    }


def make_module_params(**overrides):
    """Build a complete parameter dict for main() tests."""
    params = {
        'state': 'present',
        'organization': 'Demo-DevNet',
        'name': 'test-profile',
        'target_platform': 'Standalone',
        'tags': [],
        'description': '',
        'assigned_server': None,
        'assigned_server_serial': None,
        'uuid_address_type': None,
        'uuid_pool': None,
        'static_uuid_address': None,
        'action': None,
        'server_profile_template': None,
        'wait_for_action': True,
        'action_timeout': 1200,
        'action_poll_interval': 60,
    }
    for policy_name in server_profile_module.policy_resource_path:
        params[policy_name] = None
    params.update(overrides)
    return params


class TestWaitForProfileAction(unittest.TestCase):
    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.time')
    def test_returns_immediately_when_already_associated(self, mock_time):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = make_profile_response(
            control_action='No-op', config_state='Associated',
        )

        result = wait_for_profile_action(intersight, 'test-profile', timeout=120, poll_interval=10)

        self.assertTrue(result)
        mock_time.sleep.assert_not_called()

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.time')
    def test_polls_until_noop(self, mock_time):
        intersight = make_intersight_mock()
        intersight.call_api.side_effect = [
            make_profile_response(control_action='Deploy', config_state='Configuring', oper_state='InProgress'),
            make_profile_response(control_action='Deploy', config_state='Configuring', oper_state='InProgress'),
            make_profile_response(control_action='No-op', config_state='Associated', oper_state='Ok'),
        ]

        result = wait_for_profile_action(intersight, 'test-profile', timeout=300, poll_interval=10)

        self.assertTrue(result)
        self.assertEqual(mock_time.sleep.call_count, 2)

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.time')
    def test_fails_on_oper_state_failed(self, mock_time):
        intersight = make_intersight_mock()
        intersight.call_api.side_effect = [
            make_profile_response(control_action='Deploy', config_state='Configuring', oper_state='InProgress'),
            make_profile_response(control_action='Deploy', config_state='Failed', oper_state='Failed'),
            # get_deploy_failure_reason call
            {'Results': [{'TaskInfos': [{'Status': 'FAILED', 'FailureReason': 'BIOS update failed'}]}]},
        ]

        with self.assertRaises(FailJsonException):
            wait_for_profile_action(intersight, 'test-profile', timeout=300, poll_interval=10)

        intersight.module.fail_json.assert_called_once()
        fail_call = intersight.module.fail_json.call_args
        msg = fail_call.kwargs.get('msg', '')
        self.assertIn('BIOS update failed', msg)

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.time')
    def test_timeout(self, mock_time):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = make_profile_response(
            control_action='Deploy', config_state='Configuring', oper_state='InProgress',
        )

        # timeout=20, poll_interval=10 => 2 iterations then timeout
        with self.assertRaises(FailJsonException):
            wait_for_profile_action(intersight, 'test-profile', timeout=20, poll_interval=10)

        intersight.module.fail_json.assert_called_once()
        fail_call = intersight.module.fail_json.call_args
        msg = fail_call.kwargs.get('msg', '')
        self.assertIn('Timed out', msg)

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.time')
    def test_undeploy_completes_on_not_associated(self, mock_time):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = make_profile_response(
            control_action='No-op', config_state='Not-associated',
        )

        result = wait_for_profile_action(intersight, 'test-profile', timeout=120, poll_interval=10)

        self.assertTrue(result)
        mock_time.sleep.assert_not_called()


class TestGetDeployFailureReason(unittest.TestCase):
    def test_extracts_failure_reasons(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {
            'Results': [{
                'TaskInfos': [
                    {'Status': 'FAILED', 'FailureReason': 'Storage policy error'},
                    {'Status': 'OK', 'FailureReason': ''},
                    {'Status': 'FAILED', 'FailureReason': 'Network config invalid'},
                ],
            }],
        }

        result = get_deploy_failure_reason(intersight, 'test-profile')

        self.assertEqual(result, 'Storage policy error; Network config invalid')

    def test_returns_unknown_when_no_results(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        result = get_deploy_failure_reason(intersight, 'test-profile')

        self.assertIn('Unknown', result)


class TestPerformProfileAction(unittest.TestCase):
    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.wait_for_profile_action')
    def test_deploy_skips_when_already_associated(self, mock_wait):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = make_profile_response(
            control_action='No-op', config_state='Associated',
        )

        perform_profile_action(intersight, 'test-profile', 'Deploy', wait=True, timeout=120, poll_interval=10)

        self.assertFalse(intersight.result['changed'])
        mock_wait.assert_not_called()

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.wait_for_profile_action')
    def test_undeploy_skips_when_not_associated(self, mock_wait):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = make_profile_response(
            control_action='No-op', config_state='Not-associated',
        )

        perform_profile_action(intersight, 'test-profile', 'Undeploy', wait=True, timeout=120, poll_interval=10)

        self.assertFalse(intersight.result['changed'])
        mock_wait.assert_not_called()

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.wait_for_profile_action')
    def test_deploy_sends_patch_and_waits(self, mock_wait):
        intersight = make_intersight_mock()
        # GET returns profile in Assigned state (not yet deployed)
        intersight.call_api.return_value = make_profile_response(
            control_action='No-op', config_state='Assigned',
        )

        perform_profile_action(intersight, 'test-profile', 'Deploy', wait=True, timeout=120, poll_interval=10)

        self.assertTrue(intersight.result['changed'])
        # Verify PATCH was called with Deploy action
        patch_call = intersight.call_api.call_args_list[-1]
        self.assertEqual(patch_call.kwargs.get('http_method', patch_call[1].get('http_method')), 'patch')
        mock_wait.assert_called_once()

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.wait_for_profile_action')
    def test_deploy_no_wait(self, mock_wait):
        intersight = make_intersight_mock()
        get_response = make_profile_response(control_action='No-op', config_state='Assigned')
        intersight.call_api.return_value = get_response

        perform_profile_action(intersight, 'test-profile', 'Deploy', wait=False, timeout=120, poll_interval=10)

        self.assertTrue(intersight.result['changed'])
        mock_wait.assert_not_called()

    @patch('ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile.wait_for_profile_action')
    def test_check_mode_does_not_patch(self, mock_wait):
        intersight = make_intersight_mock(check_mode=True)
        intersight.call_api.return_value = make_profile_response(
            control_action='No-op', config_state='Assigned',
        )

        perform_profile_action(intersight, 'test-profile', 'Deploy', wait=True, timeout=120, poll_interval=10)

        self.assertTrue(intersight.result['changed'])
        # Only 1 call (GET), no PATCH
        self.assertEqual(intersight.call_api.call_count, 1)
        mock_wait.assert_not_called()

    def test_fails_when_profile_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        with self.assertRaises(FailJsonException):
            perform_profile_action(intersight, 'nonexistent', 'Deploy', wait=True, timeout=120, poll_interval=10)

        intersight.module.fail_json.assert_called_once()


class TestPerformUnassign(unittest.TestCase):
    def test_skips_when_no_server_assigned(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = make_profile_response(config_state='Not-assigned')
        # No AssignedServer set
        intersight.call_api.return_value['Results'][0]['AssignedServer'] = None

        perform_unassign(intersight, 'test-profile')

        self.assertFalse(intersight.result['changed'])

    def test_unassigns_server(self):
        intersight = make_intersight_mock()
        profile = make_profile_response(config_state='Assigned')
        profile['Results'][0]['AssignedServer'] = {'Moid': 'server-123', 'ObjectType': 'compute.Blade'}
        intersight.call_api.return_value = profile

        perform_unassign(intersight, 'test-profile')

        self.assertTrue(intersight.result['changed'])
        patch_call = intersight.call_api.call_args_list[-1]
        self.assertEqual(patch_call.kwargs.get('http_method', patch_call[1].get('http_method')), 'patch')

    def test_check_mode(self):
        intersight = make_intersight_mock(check_mode=True)
        profile = make_profile_response()
        profile['Results'][0]['AssignedServer'] = {'Moid': 'server-123', 'ObjectType': 'compute.Blade'}
        intersight.call_api.return_value = profile

        perform_unassign(intersight, 'test-profile')

        self.assertTrue(intersight.result['changed'])
        self.assertEqual(intersight.call_api.call_count, 1)

    def test_fails_profile_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        with self.assertRaises(FailJsonException):
            perform_unassign(intersight, 'nonexistent')


class TestPerformAttach(unittest.TestCase):
    def test_skips_when_already_attached_to_same_template(self):
        intersight = make_intersight_mock()
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = {'Moid': 'template-abc', 'ObjectType': 'server.ProfileTemplate'}
        intersight.call_api.return_value = profile
        intersight.get_moid_by_name = MagicMock(return_value='template-abc')

        perform_attach(intersight, 'test-profile', 'My-Template', 'default')

        self.assertFalse(intersight.result['changed'])

    def test_attaches_to_template(self):
        intersight = make_intersight_mock()
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = None
        intersight.call_api.return_value = profile
        intersight.get_moid_by_name = MagicMock(return_value='template-xyz')

        perform_attach(intersight, 'test-profile', 'My-Template', 'default')

        self.assertTrue(intersight.result['changed'])
        post_call = [c for c in intersight.call_api.call_args_list if c.kwargs.get('http_method') == 'post']
        self.assertEqual(len(post_call), 1)

    def test_fails_template_not_found(self):
        intersight = make_intersight_mock()
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = None
        intersight.call_api.return_value = profile
        intersight.get_moid_by_name = MagicMock(return_value=None)

        with self.assertRaises(FailJsonException):
            perform_attach(intersight, 'test-profile', 'Bad-Template', 'default')

    def test_check_mode(self):
        intersight = make_intersight_mock(check_mode=True)
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = None
        intersight.call_api.return_value = profile
        intersight.get_moid_by_name = MagicMock(return_value='template-xyz')

        perform_attach(intersight, 'test-profile', 'My-Template', 'default')

        self.assertTrue(intersight.result['changed'])
        post_calls = [c for c in intersight.call_api.call_args_list if c.kwargs.get('http_method') == 'post']
        self.assertEqual(len(post_calls), 0)


class TestPerformDetach(unittest.TestCase):
    def test_skips_when_not_attached(self):
        intersight = make_intersight_mock()
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = None
        intersight.call_api.return_value = profile

        perform_detach(intersight, 'test-profile')

        self.assertFalse(intersight.result['changed'])

    def test_detaches_from_template(self):
        intersight = make_intersight_mock()
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = {'Moid': 'template-abc', 'ObjectType': 'server.ProfileTemplate'}
        intersight.call_api.return_value = profile

        perform_detach(intersight, 'test-profile')

        self.assertTrue(intersight.result['changed'])

    def test_check_mode(self):
        intersight = make_intersight_mock(check_mode=True)
        profile = make_profile_response()
        profile['Results'][0]['SrcTemplate'] = {'Moid': 'template-abc', 'ObjectType': 'server.ProfileTemplate'}
        intersight.call_api.return_value = profile

        perform_detach(intersight, 'test-profile')

        self.assertTrue(intersight.result['changed'])
        self.assertEqual(intersight.call_api.call_count, 1)

    def test_fails_profile_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        with self.assertRaises(FailJsonException):
            perform_detach(intersight, 'nonexistent')


class TestMain(unittest.TestCase):
    @patch.object(server_profile_module, 'perform_profile_action')
    @patch.object(server_profile_module, 'IntersightModule')
    @patch.object(server_profile_module, 'AnsibleModule')
    def test_check_mode_create_with_action_skips_action(
        self,
        ansible_module_mock,
        intersight_module_mock,
        perform_profile_action_mock,
    ):
        module = MagicMock()
        module.check_mode = True
        module.params = make_module_params(action='Deploy', wait_for_action=False)
        module.exit_json.side_effect = ExitJsonException
        module.fail_json.side_effect = FailJsonException
        ansible_module_mock.return_value = module

        intersight = MagicMock()
        intersight.module = module
        intersight.result = {'changed': True, 'api_response': {}, 'trace_id': ''}
        intersight.configure_policy_or_profile.return_value = None
        intersight_module_mock.return_value = intersight

        with self.assertRaises(ExitJsonException):
            server_profile_module.main()

        perform_profile_action_mock.assert_not_called()
        module.exit_json.assert_called_once_with(**intersight.result)

    @patch.object(server_profile_module, 'perform_profile_action')
    @patch.object(server_profile_module, 'IntersightModule')
    @patch.object(server_profile_module, 'AnsibleModule')
    def test_check_mode_existing_profile_runs_action(
        self,
        ansible_module_mock,
        intersight_module_mock,
        perform_profile_action_mock,
    ):
        module = MagicMock()
        module.check_mode = True
        module.params = make_module_params(action='Deploy', wait_for_action=False)
        module.exit_json.side_effect = ExitJsonException
        module.fail_json.side_effect = FailJsonException
        ansible_module_mock.return_value = module

        intersight = MagicMock()
        intersight.module = module
        intersight.result = {'changed': False, 'api_response': {}, 'trace_id': ''}
        intersight.configure_policy_or_profile.return_value = 'profile-123'
        intersight_module_mock.return_value = intersight

        with self.assertRaises(ExitJsonException):
            server_profile_module.main()

        perform_profile_action_mock.assert_called_once_with(
            intersight,
            profile_name='test-profile',
            action='Deploy',
            wait=False,
            timeout=1200,
            poll_interval=60,
        )
        module.exit_json.assert_called_once_with(**intersight.result)


if __name__ == '__main__':
    unittest.main()
