

def _make_method(function_name, params):
    """
    This needs to be in a new stack frame so that function_name and params
    are, effectively, snapshotted to _invoke's scope.

    :param function_name: a function name.
    :param params: function parameters.
    :return: a method to bind to a client object.
    """
    def _invoke(_self, **kwargs):
        param_keys = kwargs.keys()
        valid_names = set.difference(set(param_keys), set(params))
        err = "{}() got unexpected keyword arguments {}".format(
            function_name,
            list(valid_names)
        )
        if len(valid_names) > 0:
            raise TypeError(err)

        response = _self._client.request(function_name, kwargs)
        return response

    return _invoke


class Client(object):

    type_spec = {}

    def __init__(self, avro_client):
        self._client = avro_client
        self._setup_methods(self._client.local_protocol.to_json())

    def _setup_methods(self, protocol_json):
        messages = protocol_json.get("messages") or {}
        for method, definition in messages.iteritems():
            function_name = str(method)
            doc_strings = [
                "Client request method for {}.\n".format(function_name)
            ]
            request_params = definition["request"]
            param_names = sorted([p["name"] for p in request_params])
            for param in request_params:
                param_doc = ":param {}: type {}".format(
                    param["name"],
                    param["type"]
                )
                doc_strings.append(param_doc)
            response_spec = definition["response"]
            if isinstance(response_spec, dict):
                response_str = ":returns: {} of {}.".format(
                    response_spec["type"],
                    response_spec["items"]
                )
            elif hasattr(response_spec, "__iter__"):
                response_str = ":returns: {}.".format(
                    " or ".join([str(r) for r in response_spec])
                )
            else:
                response_str = ":returns: {}.".format(response_spec)

            doc_strings.append(response_str)

            _invoke = _make_method(function_name, param_names)
            _invoke.__module__ = __package__
            _invoke.__name__ = function_name
            _invoke.__doc__ = "\n".join(doc_strings)
            descriptor = _invoke.__get__(self, self.__class__)
            setattr(self, function_name, descriptor)
