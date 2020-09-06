from os import environ


def get_env_value(variable_name, default_value=None):
    return environ.get(variable_name, default_value)
