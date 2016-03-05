from zope import interface as zi


class IProtocolRetriever(zi.Interface):

    name = zi.Attribute("""Registry type name.""")

    def get_protocol_string(service_name, version):
        """Retrieve a protocol string for the given service_name/version."""
    def get_protocol(service_name, version):
        """Retrieve a protocol for the given service_name/version."""

    def get_host_info(self, service_name, version=None):
        """Retrieve host, port, path tuple for service_name/version."""

    def get_client(self, service_name, version=None):
        """Retrieve avro client for service_name/version"""
