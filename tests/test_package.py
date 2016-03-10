import os
import unittest

import mock

import avro_service_clients
from avro_service_clients import core


here = os.path.abspath(os.path.dirname(__file__))
schema_dir = os.path.join(here, "schemas")


class TestEnvironmentClientLoader(unittest.TestCase):

    def test_get_client(self):
        reg_path_envvar = "AVRO_SERVICE_CLIENTS_LOCAL_REGISTRY_PATH"
        protocol_loader_ennvar = "AVRO_SERVICE_CLIENTS_PROTOCOL_LOADER_TYPE"
        mocked_env = {
            reg_path_envvar: schema_dir,
            protocol_loader_ennvar: "local"
        }
        with mock.patch.dict(os.environ, mocked_env):
            loader = avro_service_clients.get_loader()

        expected_host = "127.0.0.1"
        expected_port = "8080"
        expected_path = "/bogus"
        mocked_env.update({
            "AVRO_SERVICE_CLIENTS_TEST_HOST": expected_host,
            "AVRO_SERVICE_CLIENTS_TEST_PORT": expected_port,
            "AVRO_SERVICE_CLIENTS_TEST_PATH": expected_path,
        })

        with mock.patch.dict(os.environ, mocked_env), \
                mock.patch("avro.ipc.HTTPTransceiver"):
            client = avro_service_clients.get_client("test")

        self.assertIsInstance(client, core.Client)
