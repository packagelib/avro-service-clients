import os
import urlparse

from avro import protocol
from avro_registry import clients


CLIENTS = {
    "file": clients.FileSystemClient
}
PROTOCL_ENVVAR = "PROTOCOL_REGISTRY"

def get_protocol(service_name, version):
    protocol_loc = os.environ.get(PROTOCOL_ENVVAR)
    if protocol_loc is None:
        err = "Environment variable $%s is not set." % PROTOCOL_ENVVAR
        raise ValueError(err)

    parsed = urlparse.urlparse(protocol_loc)
    scheme = 'file'
    if parsed.scheme:
        scheme = parsed.scheme
    client = CLIENTS[scheme](parsed)
    protocol_contents = client.get(service_name, version)
    protocol = protocol.parse(protocol_contents)
    return protocol
