from zope import interface as zi


class IProtocolRetriever(zi.Interface):

    name = zi.Attribute("""Registry type name.""")

    def get(service_name, version):
        """Retrieve a protocol for the given service_name/version."""
