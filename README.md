Avro Service Clients Library
============================

Quick start example:

Create an Avro file and compile it into a schema:

    protocol FooService {
        string my_function(string my_arg);
    }

Wire that up into an Avro IPC responder (e.g. https://github.com/packagelib/flask-avro)


Dump the schema into `/path/to/avro/schema/files/foo.avpr`


Set environment variables:

    AVRO_SERVICE_CLIENTS_LOCAL_REGISTRY_PATH=/path/to/avro/schema/files
    AVRO_SERVICE_CLIENTS_FOO_HOST=localhost
    AVRO_SERVICE_CLIENTS_FOO_PORT=8080
    AVRO_SERVICE_CLIENTS_FOO_PATH=/my/service/endpoint

Then use the library to make a client:

    import avro_service_clients

    client = avro_service_clients.get_client("foo")
    client.my_function(my_arg="bar")
