import os

from avro import protocol as avro_protocol
from avro import ipc as avro_ipc
from zope import interface as zi

from service_clients import wrapper
from service_clients.clients import interfaces as api


@zi.implementer(api.IProtocolRetriever)
class FileSystemProtocolRetriever(object):

    name = "local"
    key_type_map = {
        "host": "HOST",
        "port": "PORT",
        "path": "PATH"
    }

    def __init__(self, location):
        self._root = location

    def get_protocol_string(self, service_name, version):
        filename_parts = [service_name]
        if version:
            filename_parts.append("v{}".format(version))
        filename = "-".join(filename_parts)
        filename = "{}.avpr".format(filename)
        location = os.path.abspath(os.path.join(self._root, filename))
        if not os.path.exists(location):
            raise OSError("No such file or directory: '%s'" % location)

        with open(location) as _file:
            contents = _file.read()

        return contents

    def get_protocol(self, service_name, version):
        contents = self.get_protocol_string(service_name, version)
        return avro_protocol.parse(contents)

    def format_envvar_key(self, service_name, version, suffix):
        key_parts = [service_name, self.key_type_map[suffix]]
        if version:
            key_parts.insert(1, version.replace(".", "_"))
        key = "_".join(key_parts).upper()
        return key

    def get_host_info(self, service_name, version=None):
        host_key = self.format_envvar_key(service_name, version, "host")
        port_key = self.format_envvar_key(service_name, version, "port")
        path_key = self.format_envvar_key(service_name, version, "path")
        host = os.environ.get(host_key)
        port = os.environ.get(port_key)
        resource = os.environ.get(path_key)
        return host, port, resource

    def get_client(self, service_name, version=None):
        protocol = self.get_protocol(service_name, version)
        host, port, resource = self.get_host_info(service_name, version)
        transceiver = avro_ipc.HTTPTransceiver(host, port, resource)
        client = avro_ipc.Requestor(protocol, transceiver)
        return wrapper.ClientWrapper(client)
