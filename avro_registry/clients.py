import os


class FileSystemClient(object):

    def __init__(self, location):
        self._root = location.path

    def get(self, service_name, version):
        location = os.path.abspath(
            os.path.join(
                self._root,
                service_name,
                "v%d.avsc" % version
            )
        )
        if not os.path.exists(location):
            raise OSError("No such file or directory: '%s'" % location)

        with open(location) as _file:
            contents = _file.read()

        return contents
