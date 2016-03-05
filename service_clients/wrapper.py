

class ClientWrapper(object):

    def __init__(self, avro_client):
        self._client = avro_client

    def _func_wrapper(self, function_name):
        client = self._client

        def _invoke(**kwargs):
            response = client.request(function_name, kwargs)
            return response
        return _invoke

    def __getattr__(self, item):
        return self._func_wrapper(item)
