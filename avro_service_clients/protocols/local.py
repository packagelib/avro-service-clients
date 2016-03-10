import os
from avro import protocol as avro_protocol
from zope import interface as zi

from avro_service_clients import constants
from avro_service_clients import interfaces as api

REGISTRY_PATH_ENVVAR = "LOCAL_REGISTRY_PATH"


@zi.implementer(api.IProtocolLoader)
class FileSystemProtocolLoader(object):
    """
    Protocol loader for accessing Avro protocols from file system paths.
    """

    type_name = "local"

    def __init__(self):
        env_key = "{}_{}".format(
            constants.ENV_PREFIX,
            REGISTRY_PATH_ENVVAR
        )
        self._root = os.environ[env_key]

    def get_protocol_string(self, name, version=None):
        """
        Retrieves an avro protocol by loading a derived filename from the
        file-system.

        The environment variable AVRO_SERVICE_CLIENTS_LOCAL_REGISTRY_PATH
        should be set and a valid path.

        Inside the path, the protocol file should be named:

        <name>.avpr OR
        <name>-<version>.avpr

        :param name: a service name.
        :param version: an optional service version.
        :return: the contents of a loaded avro protocol file.
        """
        filename_parts = [name]

        if version:
            filename_parts.append(str(version))

        filename = "-".join(filename_parts)
        filename = "{}.avpr".format(filename)
        location = os.path.abspath(os.path.join(self._root, filename))

        if not os.path.exists(location):
            raise OSError("No such file or directory: {}".format(location))

        if not os.path.isfile(location):
            raise IOError("{} is not a regular file.".format(location))

        with open(location) as _file:
            contents = _file.read()

        return contents

    def get_protocol(self, name, version=None):
        """
        Retrieves an avro.protocol object.

        First loads the protocol string, then parses it by calling the
        avro.protocol parser.

        :param name: a service name.
        :param version: an optional version.
        :return: an avro.protocol.Protocol object.
        """
        contents = self.get_protocol_string(name, version=version)
        return avro_protocol.parse(contents)


protocol_loader = (
    FileSystemProtocolLoader.type_name,
    FileSystemProtocolLoader
)
__all__ = ["protocol_loader"]
