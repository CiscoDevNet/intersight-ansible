import unittest
from unittest.mock import patch, MagicMock, call
from types import SimpleNamespace

from ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile import (
    wait_for_profile_action,
    get_deploy_failure_reason,
    perform_profile_action,
)


class FailJsonException(Exception):
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


if __name__ == '__main__':
    unittest.main()
