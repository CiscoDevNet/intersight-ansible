import unittest
from unittest.mock import MagicMock

from ansible_collections.cisco.intersight.plugins.modules.intersight_server_profile_derive import (
    get_profile_by_name,
    get_template_moid,
    derive_profile,
    sync_profile,
    delete_profile,
    profile_needs_sync,
)


class FailJsonException(Exception):
    pass


def make_intersight_mock(check_mode=False):
    module = MagicMock()
    module.check_mode = check_mode
    module.params = {}
    module.fail_json.side_effect = FailJsonException
    intersight = MagicMock()
    intersight.module = module
    intersight.result = {'changed': False, 'api_response': {}}
    return intersight


def make_profile(name='test-profile', moid='profile-123', config_state='Associated'):
    return {
        'Moid': moid,
        'Name': name,
        'ConfigContext': {
            'ControlAction': 'No-op',
            'ConfigState': config_state,
            'OperState': 'Ok',
        },
    }


class TestGetProfileByName(unittest.TestCase):
    def test_returns_profile_when_found(self):
        intersight = make_intersight_mock()
        profile = make_profile()
        intersight.call_api.return_value = {'Results': [profile]}

        result = get_profile_by_name(intersight, 'test-profile')

        self.assertEqual(result['Moid'], 'profile-123')

    def test_returns_none_when_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        result = get_profile_by_name(intersight, 'nonexistent')

        self.assertIsNone(result)


class TestGetTemplateMoid(unittest.TestCase):
    def test_returns_moid_when_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': [{'Moid': 'template-abc'}]}

        result = get_template_moid(intersight, 'My-Template', 'org-123')

        self.assertEqual(result, 'template-abc')

    def test_returns_none_when_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        result = get_template_moid(intersight, 'Bad-Template', 'org-123')

        self.assertIsNone(result)


class TestDeriveProfile(unittest.TestCase):
    def test_posts_mocloner(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Moid': 'cloner-123'}

        derive_profile(intersight, 'template-abc', 'SP-Derived-1', 'org-123')

        call_args = intersight.call_api.call_args
        self.assertEqual(call_args.kwargs['http_method'], 'post')
        self.assertEqual(call_args.kwargs['resource_path'], '/bulk/MoCloners')
        body = call_args.kwargs['body']
        self.assertEqual(body['Sources'][0]['Moid'], 'template-abc')
        self.assertEqual(body['Targets'][0]['Name'], 'SP-Derived-1')


class TestSyncProfile(unittest.TestCase):
    def test_posts_momerger(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {}

        sync_profile(intersight, 'template-abc', 'profile-123')

        call_args = intersight.call_api.call_args
        self.assertEqual(call_args.kwargs['http_method'], 'post')
        self.assertEqual(call_args.kwargs['resource_path'], '/bulk/MoMergers')
        body = call_args.kwargs['body']
        self.assertEqual(body['MergeAction'], 'Replace')
        self.assertEqual(body['Sources'][0]['Moid'], 'template-abc')
        self.assertEqual(body['Targets'][0]['Moid'], 'profile-123')


class TestDeleteProfile(unittest.TestCase):
    def test_deletes_by_moid(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {}

        delete_profile(intersight, 'profile-123')

        call_args = intersight.call_api.call_args
        self.assertEqual(call_args.kwargs['http_method'], 'delete')
        self.assertEqual(call_args.kwargs['moid'], 'profile-123')


class TestProfileNeedsSync(unittest.TestCase):
    def test_force_sync_always_true(self):
        profile = make_profile(config_state='Associated')
        self.assertTrue(profile_needs_sync(profile, force_sync=True))

    def test_pending_changes_needs_sync(self):
        profile = make_profile(config_state='Pending-changes')
        self.assertTrue(profile_needs_sync(profile, force_sync=False))

    def test_out_of_sync_needs_sync(self):
        profile = make_profile(config_state='Out-of-sync')
        self.assertTrue(profile_needs_sync(profile, force_sync=False))

    def test_inconsistent_needs_sync(self):
        profile = make_profile(config_state='Inconsistent')
        self.assertTrue(profile_needs_sync(profile, force_sync=False))

    def test_associated_no_sync(self):
        profile = make_profile(config_state='Associated')
        self.assertFalse(profile_needs_sync(profile, force_sync=False))

    def test_assigned_no_sync(self):
        profile = make_profile(config_state='Assigned')
        self.assertFalse(profile_needs_sync(profile, force_sync=False))


if __name__ == '__main__':
    unittest.main()
