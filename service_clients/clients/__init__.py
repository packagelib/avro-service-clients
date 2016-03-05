import os

from zope import component as zc
from zope.component import factory as zf
from zope.component import interfaces as zci

from . import interfaces as storage_api
from . import local as local_api


AVRO_API_PREFIX = "avro-registry-api"
REGISTRY_TYPE_ENVVAR = "AVRO_REGISTRY_TYPE"
REGISTRY_PATH_ENVVAR = "AVRO_REGISTRY_PATH"


def avro_api_name(name):
    return "{}-{}".format(AVRO_API_PREFIX, name)


def get_api(name):
    path = os.environ.get(REGISTRY_PATH_ENVVAR)
    api_obj = zc.createObject(avro_api_name(name), path)
    return api_obj


def get():
    storage_type = os.environ.get(
        REGISTRY_TYPE_ENVVAR,
        "local"
    )
    return get_api(storage_type or "local")


def _init():
    registry = zc.getGlobalSiteManager()
    _avro_apis = [local_api.FileSystemProtocolRetriever]
    for impl in _avro_apis:
        name = avro_api_name(impl.name)
        registry.registerUtility(
            zf.Factory(impl, name),
            zci.IFactory,
            name=name
        )

_init()


__all__ = [
    avro_api_name.__name__,
    get_api.__name__,
    get.__name__
]
