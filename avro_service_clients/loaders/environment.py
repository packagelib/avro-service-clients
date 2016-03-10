import os

from avro import ipc as avro_ipc
from zope import component as zc
from zope import interface as zi

from avro_service_clients import core
from avro_service_clients import interfaces as api
from avro_service_clients import utils


@zc.adapter(api.IProtocolLoader)
@zi.implementer(api.IClientLoader)
class EnvironmentClientLoader(object):
    """
    Loader for accessing host, port, path information from the runtime
    environment.

    The get_client method retrieves an Avro IPC client wrapper.
    """

    type_name = "environment"

    def __init__(self, protocol_loader):
        self._protocol_loader = protocol_loader

    def get_host_info(self, name, version=None):
        """
        Retrieves a three-element tuple of host information for a service.

        The tuple consist of (host, port, path).

        Each value is looked up from an environment variable assumed to be
        set in the runtime environment.

        :param name: a service name.
        :param version: optional service version.
        :return: a three-element tuple of (host, port, path).
        """
        host_key = utils.format_envvar_key(name, version, "host")
        port_key = utils.format_envvar_key(name, version, "port")
        path_key = utils.format_envvar_key(name, version, "path")
        host = os.environ.get(host_key)
        port = os.environ.get(port_key)
        resource = os.environ.get(path_key)
        return host, port, resource

    def get_client(self, name, version=None):
        """
        Retrieves an Avro Client for a service.

        :param name: a service name.
        :param version: optional service versio.
        :return: an avro_service_clients.Client object.
        """
        protocol = self._protocol_loader.get_protocol(name, version)
        host, port, resource = self.get_host_info(name, version)
        transceiver = avro_ipc.HTTPTransceiver(host, port, resource)
        client = avro_ipc.Requestor(protocol, transceiver)
        return core.Client(client)


client_loader = (
    EnvironmentClientLoader.type_name,
    EnvironmentClientLoader,
    (api.IProtocolLoader,),
    api.IClientLoader
)
__all__ = ["client_loader"]
