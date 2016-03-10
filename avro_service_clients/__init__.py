import os
import pkgutil
import importlib

from zope import component as zc
from zope.component import factory as zf
from zope.component import interfaces as zci

from . import constants
from . import interfaces as api

LOADER_TYPE_ENVVAR = "{}_LOADER_TYPE".format(constants.ENV_PREFIX)
PROTOCOL_LOADER_TYPE_ENVVAR = "{}_PROTOCOL_LOADER_TYPE".format(
    constants.ENV_PREFIX
)


def registry_api_name(name):
    return "{}-{}".format(constants.REGISTRY_PREFIX, name)


def get_protocol_loader():

    protocol_loader_type = os.environ.get(
        PROTOCOL_LOADER_TYPE_ENVVAR, "local"
    ) or "local"
    protocol_loader_type = "{}-protocol".format(protocol_loader_type)
    protocol_type_name = registry_api_name(protocol_loader_type)
    protocol_loader = zc.createObject(protocol_type_name)
    return protocol_loader


def get_loader():
    client_loader_type = os.environ.get(
        LOADER_TYPE_ENVVAR, "environment"
    ) or "environment"
    client_loader_type = "{}-client".format(client_loader_type)
    client_type_name = registry_api_name(client_loader_type)
    client_loader = zc.getAdapter(
        get_protocol_loader(),
        interface=api.IClientLoader,
        name=client_type_name
    )
    return client_loader


def get_client(name, version=None):
    loader = get_loader()
    return loader.get_client(name, version=version)


def _init():
    """Auto import and register all zope objects."""
    registry = zc.getGlobalSiteManager()

    _prefix = "{}.".format(__name__)
    for loader, name, is_pkg in pkgutil.walk_packages(__path__, _prefix):
        module = importlib.import_module(name)
        # Load protocol loader utilities
        protocol_loader_util = getattr(module, "protocol_loader", None)
        if protocol_loader_util:
            util_name, impl = protocol_loader_util
            util_name = registry_api_name(util_name)
            util_name = "{}-protocol".format(util_name)
            registry.registerUtility(
                zf.Factory(impl, util_name),
                zci.IFactory,
                name=util_name
            )
        # Load client adapter
        client_loader = getattr(module, "client_loader", None)
        if client_loader:
            adapter_name, impl, adapted_ifaces, iface = client_loader
            adapter_name = registry_api_name(adapter_name)
            adapter_name = "{}-client".format(adapter_name)
            registry.registerAdapter(
                impl,
                adapted_ifaces,
                iface,
                adapter_name
            )

_init()
__all__ = [
    registry_api_name.__name__,
    get_client.__name__,
    get_loader.__name__,
    get_protocol_loader.__name__
]
