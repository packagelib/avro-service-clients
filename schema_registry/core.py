import os
import urlparse

from avro import protocol
from schema_registry import clients


CLIENTS = {
    "file": clients.FileSystemClient
}


def get_schema(service_name, version):
    schema_loc = os.environ.get("SCHEMA_REGISTRY")
    if schema_loc is None:
        raise ValueError("Environment variable $SCHEMA_REGISTRY is not set.")

    parsed = urlparse.urlparse(schema_loc)
    scheme = 'file'
    if parsed.scheme:
        scheme = parsed.scheme

    client = CLIENTS[scheme](parsed)
    schema_contents = client.get(service_name, version)
    schema = protocol.parse(schema_contents)
    return schema
