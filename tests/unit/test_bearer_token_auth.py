from ansible_collections.cisco.intersight.plugins.module_utils.intersight import (
    IntersightModule
)
import unittest
from types import SimpleNamespace

v3_secret_key = """
-----BEGIN EC PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgFpLumf8DcLaJSAM1
pp6rmKCz00eZAewOElJKETFiW/WhRANCAAT0RlNvtEUFP2n6Aq38dnWvsT1AkZjm
B9I2RZyK1NILUMKp1rdSI05SaOS5Ca5YyJ4ZVOfSIN0ZduOSAkWaAPy0
-----END EC PRIVATE KEY-----
"""
v3_key_id = "59c84e4a16267c0001c23428/59cc595416267c0001a0dfc7/62b39fc27564612d319801ce"


class TestBearerTokenAuth(unittest.TestCase):

    def test_bearer_token_skips_key_loading(self):
        am = SimpleNamespace(params={
            "api_key_id": None,
            "api_private_key": None,
            "api_bearer_token": "test-bearer-token-value",
            "api_uri": "https://intersight.com/api/v1",
            "validate_certs": True,
            "use_proxy": True,
        })
        i = IntersightModule(am)
        assert i.bearer_token == "test-bearer-token-value"
        assert i.public_key is None
        assert i.private_key is None

    def test_bearer_token_no_cryptography_required(self):
        am = SimpleNamespace(params={
            "api_key_id": None,
            "api_private_key": None,
            "api_bearer_token": "my-token",
            "api_uri": "https://intersight.com/api/v1",
            "validate_certs": True,
            "use_proxy": True,
        })
        i = IntersightModule(am)
        assert i.bearer_token == "my-token"

    def test_missing_all_auth_fails(self):
        failed = {}

        def mock_fail_json(msg):
            failed['msg'] = msg
            raise SystemExit(1)

        am = SimpleNamespace(params={
            "api_key_id": None,
            "api_private_key": None,
            "api_bearer_token": None,
            "api_uri": "https://intersight.com/api/v1",
            "validate_certs": True,
            "use_proxy": True,
        })
        am.fail_json = mock_fail_json

        with self.assertRaises(SystemExit):
            IntersightModule(am)
        assert 'api_key_id is required' in failed['msg']

    def test_missing_private_key_fails(self):
        failed = {}

        def mock_fail_json(msg):
            failed['msg'] = msg
            raise SystemExit(1)

        am = SimpleNamespace(params={
            "api_key_id": "some-key-id",
            "api_private_key": None,
            "api_bearer_token": None,
            "api_uri": "https://intersight.com/api/v1",
            "validate_certs": True,
            "use_proxy": True,
        })
        am.fail_json = mock_fail_json

        with self.assertRaises(SystemExit):
            IntersightModule(am)
        assert 'api_private_key is required' in failed['msg']

    def test_signature_auth_still_works_with_bearer_none(self):
        am = SimpleNamespace(params={
            "api_key_id": v3_key_id,
            "api_private_key": v3_secret_key,
            "api_bearer_token": None,
            "api_uri": "https://intersight.com/api/v1",
            "validate_certs": True,
            "use_proxy": True,
        })
        i = IntersightModule(am)
        assert i.bearer_token is None
        assert i.public_key == v3_key_id
        assert i.private_key == v3_secret_key
        sig = i.get_sig_b64encode('')
        assert sig is not None
