

class Client(object):

    def __init__(self, avro_client):
        self._client = avro_client

    def _func_wrapper(self, function_name):

        def _invoke(_self, **kwargs):
            response = _self._client.request(function_name, kwargs)
            return response

        _invoke.__module__ = __package__
        _invoke.__name__ = function_name
        _invoke.__doc__ = "Client request method for: {}".format(function_name)
        descriptor = _invoke.__get__(self, self.__class__)
        setattr(self, function_name, descriptor)
        return descriptor

    def __getattr__(self, item):
        descriptor = self.__dict__.get(item)
        if descriptor is None:
            descriptor = self._func_wrapper(item)
        return descriptor
