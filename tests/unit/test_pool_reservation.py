import unittest
from unittest.mock import MagicMock

from ansible_collections.cisco.intersight.plugins.modules.intersight_pool_reservation import (
    get_pool_moid,
    get_existing_reservation,
    create_reservation,
    delete_reservation,
    POOL_TYPE_MAP,
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


class TestGetPoolMoid(unittest.TestCase):
    def test_returns_moid(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': [{'Moid': 'pool-123'}]}

        result = get_pool_moid(intersight, '/ippool/Pools', 'IP-Pool-01', 'org-123')

        self.assertEqual(result, 'pool-123')

    def test_returns_none_when_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        result = get_pool_moid(intersight, '/ippool/Pools', 'Bad-Pool', 'org-123')

        self.assertIsNone(result)


class TestGetExistingReservation(unittest.TestCase):
    def test_finds_existing(self):
        intersight = make_intersight_mock()
        reservation = {'Moid': 'res-123', 'Identity': '10.10.10.100'}
        intersight.call_api.return_value = {'Results': [reservation]}

        result = get_existing_reservation(intersight, '/ippool/Reservations', 'pool-123', '10.10.10.100', 'org-123')

        self.assertEqual(result['Moid'], 'res-123')

    def test_returns_none_when_not_found(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        result = get_existing_reservation(intersight, '/ippool/Reservations', 'pool-123', '10.10.10.200', 'org-123')

        self.assertIsNone(result)

    def test_filter_includes_identity(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Results': []}

        get_existing_reservation(intersight, '/ippool/Reservations', 'pool-123', '10.10.10.100', 'org-123')

        call_args = intersight.call_api.call_args
        filter_str = call_args.kwargs['query_params']['$filter']
        self.assertIn("Identity eq '10.10.10.100'", filter_str)
        self.assertIn("Organization.Moid eq 'org-123'", filter_str)
        self.assertNotIn("Pool.Moid eq 'pool-123'", filter_str)


class TestCreateReservation(unittest.TestCase):
    def test_posts_ip_reservation(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Moid': 'res-new', 'Identity': '10.10.10.100'}

        result = create_reservation(
            intersight, '/ippool/Reservations', 'pool-123',
            'org-123', '10.10.10.100', 'static', 'ippool.Reservation', 'ip',
        )

        call_args = intersight.call_api.call_args
        self.assertEqual(call_args.kwargs['http_method'], 'post')
        body = call_args.kwargs['body']
        self.assertEqual(body['Identity'], '10.10.10.100')
        self.assertEqual(body['AllocationType'], 'static')
        self.assertNotIn('Pool', body)
        self.assertEqual(body['Organization']['Moid'], 'org-123')

    def test_dynamic_omits_identity(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {'Moid': 'res-new'}

        create_reservation(
            intersight, '/ippool/Reservations', 'pool-123',
            'org-123', None, 'dynamic', 'ippool.Reservation', 'ip',
        )

        call_args = intersight.call_api.call_args
        body = call_args.kwargs['body']
        self.assertNotIn('Identity', body)
        self.assertEqual(body['Pool']['Moid'], 'pool-123')
        self.assertEqual(body['Organization']['Moid'], 'org-123')

    def test_wwnn_sets_id_purpose(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {}

        create_reservation(
            intersight, '/fcpool/Reservations', 'pool-123',
            'org-123', '20:00:00:25:B5:00:00:01', 'static', 'fcpool.Reservation', 'wwnn',
        )

        call_args = intersight.call_api.call_args
        body = call_args.kwargs['body']
        self.assertEqual(body['IdPurpose'], 'WWNN')

    def test_wwpn_sets_id_purpose(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {}

        create_reservation(
            intersight, '/fcpool/Reservations', 'pool-123',
            'org-123', '20:00:00:25:B5:00:00:02', 'static', 'fcpool.Reservation', 'wwpn',
        )

        call_args = intersight.call_api.call_args
        body = call_args.kwargs['body']
        self.assertEqual(body['IdPurpose'], 'WWPN')


    def test_iqn_reservation(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {}

        create_reservation(
            intersight, '/iqnpool/Reservations', 'pool-123',
            'org-123', 'iqn.2010-11.com.flexpod:storage:component:server01', 'static', 'iqnpool.Reservation', 'iqn',
        )

        call_args = intersight.call_api.call_args
        body = call_args.kwargs['body']
        self.assertEqual(body['Identity'], 'iqn.2010-11.com.flexpod:storage:component:server01')
        self.assertEqual(body['ObjectType'], 'iqnpool.Reservation')
        self.assertNotIn('IdPurpose', body)


class TestDeleteReservation(unittest.TestCase):
    def test_deletes_by_moid(self):
        intersight = make_intersight_mock()
        intersight.call_api.return_value = {}

        delete_reservation(intersight, '/ippool/Reservations', 'res-123')

        call_args = intersight.call_api.call_args
        self.assertEqual(call_args.kwargs['http_method'], 'delete')
        self.assertEqual(call_args.kwargs['moid'], 'res-123')


class TestPoolTypeMap(unittest.TestCase):
    def test_all_pool_types_mapped(self):
        for pool_type in ['ip', 'uuid', 'mac', 'iqn', 'wwnn', 'wwpn']:
            self.assertIn(pool_type, POOL_TYPE_MAP)
            self.assertIn('resource_path', POOL_TYPE_MAP[pool_type])
            self.assertIn('pool_path', POOL_TYPE_MAP[pool_type])


if __name__ == '__main__':
    unittest.main()
