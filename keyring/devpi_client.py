import contextlib

import pluggy

import keyring
from keyring.errors import KeyringError


hookimpl = pluggy.HookimplMarker("devpiclient")


# https://github.com/jaraco/jaraco.context/blob/c3a9b739/jaraco/context.py#L205
suppress = type('suppress', (contextlib.suppress, contextlib.ContextDecorator), {})


def restore_signature(func):
    # workaround for pytest-dev/pluggy#358
    def wrapper(url, username):
        return func(url, username)

    return wrapper


@hookimpl()
@restore_signature
@suppress(KeyringError)
def devpiclient_get_password(url, username):
    """
    >>> pluggy._hooks.varnames(devpiclient_get_password)
    (('url', 'username'), ())
    """
    return keyring.get_password(url, username)
