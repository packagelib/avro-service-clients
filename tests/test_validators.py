import unittest
import string
import random

from avro_service_clients import validators


class TestValidators(unittest.TestCase):

    def setUp(self):
        valid = set(list(string.digits + string.ascii_letters))
        invalid = set.difference(
            set(string.printable),
            valid
        )
        self.invalid_envvar_chars = list(invalid)

    def test_validate_envvar_key_none(self):
        self.assertEqual("", validators.validate_envvar_key(None))

    def test_validate_envvar_key_simple(self):
        # Test that anything other than ascii a-z0-9 is converted.
        input_string = "foo-bar"
        expected = "FOO_BAR"
        actual = validators.validate_envvar_key(input_string)
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
        actual = validators.validate_envvar_key(prefix + middle + suffix)
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
        actual = validators.validate_envvar_key(prefix + middle + suffix)
        self.assertEqual(expected, actual)
