from zope import interface as zi


class IProtocolLoader(zi.Interface):

    type_name = zi.Attribute("""Protocol loader type.""")

    def get_protocol_string(name, version):
        """Retrieve avro protocol string for the given name/version."""

    def get_protocol(name, version):
        """Retrieve avro protocol for the given name/version."""


class IClientLoader(zi.Interface):

    type_name = zi.Attribute("""Client loader type.""")

    def get_host_info(name, version):
        """Retrieve host, port, path tuple for name/version."""

    def get_client(name, version):
        """Retrieve avro client for name/version"""
