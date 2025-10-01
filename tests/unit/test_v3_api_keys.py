from ansible_collections.cisco.intersight.plugins.module_utils.intersight import (
    IntersightModule
)
import unittest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
import base64
from types import SimpleNamespace

# this is not a real/valid key
v3_secret_key = """
-----BEGIN EC PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgFpLumf8DcLaJSAM1
pp6rmKCz00eZAewOElJKETFiW/WhRANCAAT0RlNvtEUFP2n6Aq38dnWvsT1AkZjm
B9I2RZyK1NILUMKp1rdSI05SaOS5Ca5YyJ4ZVOfSIN0ZduOSAkWaAPy0
-----END EC PRIVATE KEY-----
"""
v3_key_id = "59c84e4a16267c0001c23428/59cc595416267c0001a0dfc7/62b39fc27564612d319801ce"
# this is not a real/valid key
v2_secret_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvV0n1s8QcR7S7u5rR94//VoUSIxJ7jvLdZRNYRQcQCECxp+H
V6ut+61D5t7YQqNcTIEv71ssC9UNs/wCIFELeN5MweLqvYto03SFJB0bLZ+ycpnp
e9jTqALZqa6uCLycFjtV9s7sW5nZZcuDiyLlNCygtkzXkUdBQ3ycaZpJphKwezQ1
xXgmWaUV6JqihSwVgj9U7sZOQN/6eCbbL2/kLoHnAYVIlbiuV0uTZsFGLsm2ZP1o
A3h2NdqhPHrBlWSmUAdhYIGlu7WNQ0yN5d6PpwHERCUI2+fOKxau8C42EYDttYf1
tnU4VZC7ItmE8ZDlrGn9f5F8virhhlBEESTXkwIDAQABAoIBABfQiVwYembfi4OE
9HT7XGzOUVK2Ye3WE0ZcOkcFMnBWNnUoRusdqinGpo14ZRYsWUU90ft2KdnrF2gV
P2c1Cg5PVrPjh8YCrFI7iyr5hht8xAJpnNV4dVXh1eHjF/v9TFv3Zl49s7fpZ0/I
AmkTIGQpYKTMkSeyIGEOYNVfE/gQljcRz6yf60GmWJY5IglXh/00GtB3GQHJqWLs
rWMi7uwtFCp6dpQDjC7VAanAnmkti4/+hiNC8c+29Zf5LcQYPz2oY3V1UlpynyYH
b+mRL5iFJwcKZs+93waTyD/igFzK+ly9Nw3/vM/D0h5wxw8UPMFHyBKN3MAI4tzW
M1QtbYECgYEA5c3V1mReeOIDx6ilUebKUooryhg0EcKIYA5bUFvlYkB7E688CpdL
nCHoeRjCKcQ0jZzpZcBpB+CoaHNLCvpaKSHzvXGmFUztMX7FMVGERWk8RwvxCVl3
j9LstVvcXklt6OE2E3GLQUhLFbs0xWghlNZWMf/KCx7t/WUChRgGRWECgYEA0vMx
EDlLISZTheR2hKlENn2yAxYfo8XieArPcjt1kivGVVqnItUMtzCRHnF1cjYnbk8g
Tf5x+8LwlOHTCX9VrQQYM98t0WsWVSmkrzss1/K0yu09sYsdOet9UL7Jet7kpA3L
dfRxXQHySJaUPVYFR9f8hQsuJrUdndFiHdHlzXMCgYEAzFNzIXgGo9bZ44mozKS3
GiKugrd4fJ4KIdZCDLZYwz5v8HWrngMeAEoJ6LpB0V8aFxwATi+Bc7amJpD0lWM6
DT6Z+MR3FpNahtqfvJUtVYYXSVhtzZFWBHRXcX2m99K0Pg8YxLr9RWNhF4Znimpn
CW52H2i+nZq3oslQL0TINqECgYA33LTScgmmNqsJmu2TxetNbs3UKWipiv6lAV/c
BUjmM3drJP17qOWcIV1crXkHjLW2bXfFj6sJm57wHjkvm6vJjHsISYKtoWkhlkyJ
JueCLECaOGcM/CT6MJVX654ZTqtHkmudyeS3V4uck1ugPoZZdyXk6YgIMhAsucT8
1pe/ZwKBgGoZAhOaR/s5EM/bwIpqPE870VnWeIbvDc8vMH3tW/q7SysfyNxyZ99w
pQ8EfDaxnEFVuY7Xa8i/qr7mmXo5E+d0TrxkB1bqtwaJJ8ojaW5G/PIkU3aTC6uV
11QYh2F1qu2ow8Y4Q3DZ78jc9M3gHvzuknyencU2K0+VhVgwEVtI
-----END RSA PRIVATE KEY-----
"""
v2_key_id = "59c84e4a16267c0001c23428/59cc595416267c0001a0dfc7/62b3ba347564612d3198f5b1"


class TestIntersightModuleUtilKeyHandling(unittest.TestCase):
    def setUp(self):
        pass

    def with_key(self, key_id, secret_key):
        am = SimpleNamespace(params={
            "api_key_id": key_id,
            "api_private_key": secret_key,
            "api_uri": "https://intersight.com",
        })
        i = IntersightModule(am)
        sig = i.get_sig_b64encode('')
        return sig

    def test_with_v3_key(self):
        sig = self.with_key(v3_key_id, v3_secret_key)

        # For v3 (ECDSA) authentication, the signature is not deterministic (includes a random nonce) so we can't just use known-good examples.
        # Instead, we can verify that the signed string is correct and verify against the signature
        priv_key = serialization.load_pem_private_key(
            v3_secret_key.encode("utf-8")
            .replace(b"-----BEGIN EC PRIVATE KEY-----", b"-----BEGIN PRIVATE KEY-----")
            .replace(b"-----END EC PRIVATE KEY-----", b"-----END PRIVATE KEY-----"),
            password=None,
            backend=default_backend(),
        )
        pub_key = priv_key.public_key()
        # pubkey.verify() will raise InvalidSignature exception if the verification fails and therefore fail the test
        pub_key.verify(
            base64.b64decode(sig),
            ''.encode(),
            ec.ECDSA(hashes.SHA256()),
        )

    def test_with_v2_key(self):
        sig = self.with_key(v2_key_id, v2_secret_key)
        expected_sig = (b"QuBlJiYPGIxqzrkUqbQLqkp0N9d5Bki4921YuoV32SFzDjwePAqY"
                        b"FL80My3InHrx61RO0yNr4MVYmuHMihvWGLkNt3z7/7VA4dyS9B9p"
                        b"CGrT78b69upSM05A6x09fc+AHVwy3emex8OJJ6SXGXdnbSoIa4Fj"
                        b"tlejACMVd+5rydrFZ0c0d8uGqLcWdiRWUJY60u7a8SDPo8E1mPzv"
                        b"UrW8IJt3wjrLRnNSKH3qzmdKbyosed2+OtwrR22nubRx8qGHon/x"
                        b"rZ5EWrGfdR3V3YU6JaB30WVbiKQZ/ZOW775hvn9ub8NH6Z0n88b5"
                        b"0h3D6Ua0mSgZfDaJnugGAE56f+Ultg==")
        assert sig == expected_sig

    def test_with_broken_key(self):
        with self.assertRaises(ValueError):
            self.with_key(v2_key_id, "")

    def test_with_invalid_key_type(self):
        with self.assertRaises(Exception) as cm:
            self.with_key(v2_key_id, """
-----BEGIN PRIVATE KEY-----
MIIBWgIBADCCATMGByqGSM44BAEwggEmAoGBAJ4MYKsC6z7haWi9Sm+cV/gxn+mI
jWMXEyC8+bnB0ySQxxLxy6XUnpRf4dwv/PsE1duObRse3L9jI0iExMDGveJRG7Od
ee+4qKRoCLNA5ycZkW7Hxcx0ELftKZWtS/17kXn0BvxvkUPe9X8FQPgi9XDC95/k
PX6PpQtcM/VBZtxHAh0A6n10yJauVEYPo40DqnCzb7ENStTbYPGb+n8qyQKBgC51
J96l4D/RxB6+mu+7C7IRQjsyf+I0yiqqi0zBVt3lltxlS2Bxzhxag5sCarJBtxH+
okvj7Xb1QrlWyFW7X3mKsl5+9lHfKucwrPEGGeBnAmJrcTVH8mV7vSALl3YFMFtr
9dy+QvfsIgvxKvFhRLgyUe0oQe0tGqk8BrXGRW03BB4CHFp5tg9e6x4bbdjd+qr5
P6D93gUzYoUOPkUUp+M=
-----END PRIVATE KEY-----
""")
        self.assertEqual(str(cm.exception), "Unsupported key: DSAPrivateKey")
