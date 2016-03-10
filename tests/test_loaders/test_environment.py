import os
import unittest
import types

import mock

import avro_service_clients
from avro_service_clients import core
from avro_service_clients.loaders import environment as env_loader


here = os.path.abspath(os.path.dirname(__file__))
schema_dir = os.path.join(here, os.pardir, "schemas")


class TestEnvironmentClientLoader(unittest.TestCase):

    def setUp(self):
        reg_path_envvar = "AVRO_SERVICE_CLIENTS_LOCAL_REGISTRY_PATH"
        protocol_loader_ennvar = "AVRO_SERVICE_CLIENTS_PROTOCOL_LOADER_TYPE"
        mocked_env = {
            reg_path_envvar: schema_dir,
            protocol_loader_ennvar: "local"
        }
        with mock.patch.dict(os.environ, mocked_env):
            self.protocol_loader = avro_service_clients.get_protocol_loader()

    def test_get_host_info(self):
        loader = env_loader.EnvironmentClientLoader(self.protocol_loader)

        expected_host = "127.0.0.1"
        expected_port = "8080"
        expected_path = "/bogus"
        mocked_env = {
            "AVRO_SERVICE_CLIENTS_FOO_HOST": expected_host,
            "AVRO_SERVICE_CLIENTS_FOO_PORT": expected_port,
            "AVRO_SERVICE_CLIENTS_FOO_PATH": expected_path,
        }
        expected_info = (expected_host, expected_port, expected_path)

        with mock.patch.dict(os.environ, mocked_env):
            actual_info = loader.get_host_info("foo")

        self.assertEqual(expected_info, actual_info)

    def test_get_client(self):
        loader = env_loader.EnvironmentClientLoader(self.protocol_loader)

        expected_host = "127.0.0.1"
        expected_port = "8080"
        expected_path = "/bogus"
        mocked_env = {
            "AVRO_SERVICE_CLIENTS_TEST_HOST": expected_host,
            "AVRO_SERVICE_CLIENTS_TEST_PORT": expected_port,
            "AVRO_SERVICE_CLIENTS_TEST_PATH": expected_path,
        }

        with mock.patch.dict(os.environ, mocked_env), \
                mock.patch("avro.ipc.HTTPTransceiver"):
            client = loader.get_client("test")

        self.assertIsInstance(client, core.Client)
