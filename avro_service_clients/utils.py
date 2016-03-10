import re

from avro_service_clients import constants


_bad_chars_re = re.compile("[^a-zA-Z0-9_]")
_first_replace = re.compile("\.|-|\s")
_reduce_re = re.compile("_+")

key_type_map = {
    "host": "HOST",
    "port": "PORT",
    "path": "PATH"
}


def validate_envvar_key(envvar_name):
    """
    Validates and sanitizes a string in order to make it a valid environment
    variable key.

    :param envvar_name: input string.
    :return: an IEEE 1003.1-2001 compliant environment variable name.
    """
    envvar_name = envvar_name or ""
    try:
        if isinstance(envvar_name, unicode):
            envvar_name = envvar_name.encode('utf-8')
        else:
            envvar_name = str(envvar_name)
    except Exception:
        raise ValueError("Invalid value for environment variable name.")

    # First make sure ".", "-", and " " are replaced.
    envvar_name = _first_replace.sub("_", envvar_name)

    # Get rid of anything invalid.
    envvar_name = _bad_chars_re.sub("_", envvar_name.lower())

    # Trim the trailing bad chars.
    envvar_name = envvar_name.strip("_")

    # Make sure we only ever have a single '_' in a row.
    envvar_name = _reduce_re.sub("_", envvar_name)

    return envvar_name.upper()


def format_envvar_key(name, version, suffix):
    """
    Formats an environment variable based on provided input.

    Used for lookups for various client info.

    :param name: a service name.
    :param version: a service version.
    :param suffix: a key suffix.
    :return: a formatted environment variable key.
    """
    key_parts = [
        constants.ENV_PREFIX,
        validate_envvar_key(name),
        key_type_map[suffix]
    ]
    if version:
        key_parts.insert(2, version)
    return validate_envvar_key("_".join(key_parts))
