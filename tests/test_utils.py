import unittest
import string
import random

from avro_service_clients import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        valid = set(list(string.digits + string.ascii_letters + "_ "))
        invalid = set.difference(
            set(string.printable),
            valid
        )
        self.invalid_envvar_chars = list(invalid)

    def test_validate_envvar_key_none(self):
        self.assertEqual("", utils.validate_envvar_key(None))

    def test_validate_envvar_key_simple(self):
        # Test that anything other than ascii a-z0-9 and _ is converted.
        input_string = "foo-bar"
        expected = "FOO_BAR"
        actual = utils.validate_envvar_key(input_string)
        self.assertEqual(expected, actual)

    def test_validate_envvar_key_bookends(self):
        prefix = "".join(
            [random.choice(self.invalid_envvar_chars) for _ in range(10)]
        )
        middle = "foo"
        suffix = "".join(
            [random.choice(self.invalid_envvar_chars) for _ in range(10)]
        )

        expected = "FOO"
        actual = utils.validate_envvar_key(prefix + middle + suffix)
        self.assertEqual(expected, actual)

    def test_validate_envvar_key_nested(self):

        prefix0 = "foo"
        prefix1 = "".join(
            [random.choice(self.invalid_envvar_chars) for _ in range(10)]
        )
        prefix = prefix0 + prefix1
        middle = "bar"
        suffix0 = "".join(
            [random.choice(self.invalid_envvar_chars) for _ in range(10)]
        )
        suffix1 = "baz"
        suffix = suffix0 + suffix1

        expected = "FOO_BAR_BAZ"
        actual = utils.validate_envvar_key(prefix + middle + suffix)
        self.assertEqual(expected, actual)

    def test_format_envvar_key(self):
        expected = "AVRO_SERVICE_CLIENTS_FOO_HOST"
        actual = utils.format_envvar_key("foo", None, "host")
        self.assertEqual(expected, actual)

        expected = "AVRO_SERVICE_CLIENTS_FOO_1_0_0_HOST"
        actual = utils.format_envvar_key("foo", "1.0.0", "host")
        self.assertEqual(expected, actual)

        self.assertRaises(
            KeyError,
            utils.format_envvar_key,
            "foo",
            "1.0.0",
            "bogus"
        )
