import json
import os
import unittest

import mock
from avro import protocol as avro_protocol

from avro_service_clients.protocols import local as local_loader


here = os.path.abspath(os.path.dirname(__file__))
schema_dir = os.path.join(here, os.pardir, "schemas")


class TestLocalProtocolLoader(unittest.TestCase):

    def setUp(self):
        self.envvar = "AVRO_SERVICE_CLIENTS_LOCAL_REGISTRY_PATH"

    def test_get_protocol_string(self):
        # Make sure files exist.
        mock_env = {self.envvar: "bogus-directory"}
        with mock.patch.dict(os.environ, mock_env):
            obj = local_loader.FileSystemProtocolLoader()
        self.assertRaises(
            OSError,
            obj.get_protocol_string,
            "foo"
        )

        mock_env = {self.envvar: schema_dir}
        with mock.patch.dict(os.environ, mock_env):
            obj = local_loader.FileSystemProtocolLoader()

        # Make sure non-regular files blow up.
        self.assertRaises(
            IOError,
            obj.get_protocol_string,
            "a-directory"
        )

        with open(os.path.join(schema_dir, "test.avpr")) as _file:
            expected = json.load(_file)

        actual = json.loads(obj.get_protocol_string("test"))
        self.assertDictEqual(expected, actual)

        # Test version-based.
        with open(os.path.join(schema_dir, "test-1.0.0.avpr")) as _file:
            expected = json.load(_file)

        actual = json.loads(obj.get_protocol_string("test", "1.0.0"))
        self.assertDictEqual(expected, actual)

    def test_get_protocol(self):
        mock_env = {self.envvar: schema_dir}
        with mock.patch.dict(os.environ, mock_env):
            obj = local_loader.FileSystemProtocolLoader()

        protocol = obj.get_protocol("test")

        self.assertIsInstance(protocol, avro_protocol.Protocol)

    def test_root_location(self):
        mock_env = {self.envvar: schema_dir}
        with mock.patch.dict(os.environ, mock_env):
            obj = local_loader.FileSystemProtocolLoader()
        self.assertEqual(obj._root, schema_dir)
