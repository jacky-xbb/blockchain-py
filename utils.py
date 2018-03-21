import hashlib


def encode(string, code='utf-8'):
    return string.encode(code)


def decode(string, code='utf-8'):
    return string.decode(code)


def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()
