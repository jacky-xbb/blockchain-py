import hashlib

import redis


def encode(str, code='utf-8'):
    return str.encode(code)


def decode(bytes, code='utf-8'):
    return bytes.decode(code)


def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()


class ContinueIt(Exception):
    pass


class BreakIt(Exception):
    pass
