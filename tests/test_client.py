import os
import types
import unittest
import mock

from avro import ipc as avro_ipc
from avro import protocol as avro_protocol

from avro_service_clients import core


here = os.path.abspath(os.path.dirname(__file__))
schema_dir = os.path.join(here, "schemas")
protocol_file = os.path.join(schema_dir, "test.avpr")


class TestClient(unittest.TestCase):

    def test_client_attributes(self):
        with open(protocol_file) as _file:
            protocol_string = _file.read()

        protocol = avro_protocol.parse(protocol_string)
        avro_client = avro_ipc.Requestor(protocol, None)
        client = core.Client(avro_client)

        self.assertTrue(hasattr(client, "foo"))
        self.assertIsInstance(client.foo, types.MethodType)

        with mock.patch.object(client._client, "request", return_value="bar"):
            self.assertRaises(
                TypeError,
                client.foo,
                baz="fizz"
            )

            response = client.foo()
            self.assertEqual("bar", response)

            response = client.foo(bar="baz")
            self.assertEqual("bar", response)
