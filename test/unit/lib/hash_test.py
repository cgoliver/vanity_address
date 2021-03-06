from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from vanity_address.lib.hash import sha256, ripemd160, hash256, hash160, keccak256


class Hash256Test(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._sha256_result = 'f26c9c06a82db27233b98a2b1c5a778c987613f7589ef1fa04c39fe3f6e30e3b'
        self._hash256_result = 'd24dbe11526b088edded1aee68c5ea2aa175bee0cc0e695f3d188f14607ef5c5'

    @patch('vanity_address.lib.hash.sha256')
    def test_hash256_calls_sha256_twice(self, sha256):
        sha256.return_value = self._sha256_result

        hash256(self._hex_str)

        sha256.assert_has_calls([call(self._hex_str), call(self._sha256_result)])

    @patch('vanity_address.lib.hash.sha256')
    def test_hash256_returns_the_result_of_the_second_hash(self, sha256):
        second_hash = MagicMock()
        sha256.side_effect = [self._sha256_result, second_hash]

        result = hash256(self._hex_str)

        self.assertEqual(result, second_hash)


class Hash160Test(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._sha256_result = 'f26c9c06a82db27233b98a2b1c5a778c987613f7589ef1fa04c39fe3f6e30e3b'
        self._ripemd160_result = '92762ca96d0f1d6b494ab881ac85b3205c33934b'

    @patch('vanity_address.lib.hash.sha256')
    def test_hash256_calls_sha256(self, sha256):
        sha256.return_value = self._sha256_result

        hash160(self._hex_str)

        sha256.assert_called_once_with(self._hex_str)

    @patch('vanity_address.lib.hash.ripemd160')
    @patch('vanity_address.lib.hash.sha256')
    def test_hash256_calls_ripemd_with_the_result_of_the_sha256(self, sha256, ripemd160):
        sha256.return_value = self._sha256_result

        hash160(self._hex_str)

        ripemd160.assert_called_once_with(self._sha256_result)

    @patch('vanity_address.lib.hash.ripemd160')
    def test_hash256_calls_the_result_of_the_ripemd(self, ripemd160):
        ripemd_result = MagicMock()
        ripemd160.return_value = ripemd_result

        result = hash160(self._hex_str)

        self.assertEqual(result, ripemd_result)


class Sha256Test(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._bytes = b'\x1a+<'
        self._sha256_result = 'f26c9c06a82db27233b98a2b1c5a778c987613f7589ef1fa04c39fe3f6e30e3b'

    @patch('vanity_address.lib.hash.unhexlify')
    def test_sha256_calls_unhexlify(self, unhexlify):
        unhexlify.return_value = self._bytes

        sha256(self._hex_str)

        unhexlify.assert_called_once_with(self._hex_str)

    @patch('vanity_address.lib.hash.hashlib.sha256')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_sha256_calls_hashlib_sha256(self, unhexlify, hashlib_sha256):
        unhexlify.return_value = self._bytes

        sha256(self._hex_str)

        hashlib_sha256.assert_any_call(self._bytes)

    @patch('vanity_address.lib.hash.hashlib.sha256')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_sha256_gets_sha_hexdigest(self, unhexlify, hashlib_sha256):
        unhexlify.return_value = self._bytes
        hashlib_sha256.return_value.hexdigest.return_value = self._sha256_result

        sha256(self._hex_str)

        hashlib_sha256.return_value.hexdigest.assert_called_once()

    @patch('vanity_address.lib.hash.hashlib.sha256')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_sha256_returns_the_sha_hexdigest(self, unhexlify, hashlib_sha256):
        unhexlify.return_value = self._bytes
        sha256_result = MagicMock
        hashlib_sha256.return_value.hexdigest.return_value = sha256_result

        result = sha256(self._hex_str)

        self.assertEqual(result, sha256_result)

    def test_sha256_returns_the_correct_hash(self):
        result = sha256(self._hex_str)

        self.assertEqual(result, self._sha256_result)


class RipemdTest(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._bytes = b'\x1a+<'
        self._ripemd160_result = '2885f0092763dc3b0761e43cb64a9de1af9a16bb'

    @patch('vanity_address.lib.hash.unhexlify')
    def test_ripemd160_calls_unhexlify(self, unhexlify):
        unhexlify.return_value = self._bytes

        ripemd160(self._hex_str)

        unhexlify.assert_called_once_with(self._hex_str)

    @patch('vanity_address.lib.hash.hashlib')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_ripemd160_calls_hashlib_ripemd160(self, unhexlify, hashlib):
        unhexlify.return_value = self._bytes

        ripemd160(self._hex_str)

        hashlib.new.assert_any_call('ripemd160', self._bytes)

    @patch('vanity_address.lib.hash.hashlib')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_ripemd160_gets_sha_hexdigest(self, _, hashlib):
        hashlib.new.return_value.hexdigest.return_value = self._ripemd160_result

        ripemd160(self._hex_str)

        hashlib.new.return_value.hexdigest.assert_called_once()

    @patch('vanity_address.lib.hash.hashlib')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_ripemd160_returns_the_sha_hexdigest(self, _, hashlib):
        hashlib.new.return_value.hexdigest.return_value = self._ripemd160_result

        result = ripemd160(self._hex_str)

        self.assertEqual(result, self._ripemd160_result)

    def test_ripemd160_returns_the_correct_hash(self):
        result = ripemd160(self._hex_str)

        self.assertEqual(result, self._ripemd160_result)


class Keccak256Test(TestCase):
    def setUp(self):
        self._hex_str = '3853007f3fd5d97789ddc1fdee84822a5b75290c71ea39e57636675df2b42384'
        self._bytes = b'8S\x00\x7f?\xd5\xd9w\x89\xdd\xc1\xfd\xee\x84\x82*[u)\x0cq\xea9\xe5v6g]\xf2\xb4#\x84'
        self._sha3_256_result = 'd67a37d503c31c625d57835c8a16626a8d44f95d319fd94a0720aaa7e59e60be'

    @patch('vanity_address.lib.hash.unhexlify')
    def test_keccak256_calls_unhexlify(self, unhexlify):
        unhexlify.return_value = self._bytes

        keccak256(self._hex_str)

        unhexlify.assert_called_once_with(self._hex_str)

    @patch('vanity_address.lib.hash.hashlib.sha3_256')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_keccak256_calls_hashlib_sha3_256(self, unhexlify, sha3_256):
        unhexlify.return_value = self._bytes

        keccak256(self._hex_str)

        sha3_256.assert_called_once_with(self._bytes)

    @patch('vanity_address.lib.hash.hashlib.sha3_256')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_keccak256_gets_the_hexdigest_of_sha3_256(self, _, sha3_256):
        keccak256(self._hex_str)

        sha3_256.return_value.hexdigest.assert_called_once()

    @patch('vanity_address.lib.hash.hashlib.sha3_256')
    @patch('vanity_address.lib.hash.unhexlify')
    def test_keccak256_returns_the_hexdigest_of_sha3_256(self, _, sha3_256):
        sha3_256.return_value.hexdigest.return_value = self._sha3_256_result

        result = keccak256(self._hex_str)

        self.assertEqual(result, self._sha3_256_result)

    def test_keccak256_returns_the_correct_hash(self):
        result = keccak256(self._hex_str)

        self.assertEqual(result, self._sha3_256_result)
