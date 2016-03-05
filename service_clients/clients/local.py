import os

from avro_registry.clients import interfaces as api

from zope import interface as zi


@zi.implementer(api.IProtocolRetriever)
class FileSystemProtocolRetriever(object):

    name = "local"

    def __init__(self, location):
        self._root = location

    def get(self, service_name, version):
        filename = "-".join([
            service_name,
            "v{}".format(version),
            ".avpr"
        ])
        location = os.path.abspath(os.path.join(self._root, filename))
        if not os.path.exists(location):
            raise OSError("No such file or directory: '%s'" % location)

        with open(location) as _file:
            contents = _file.read()

        return contents
