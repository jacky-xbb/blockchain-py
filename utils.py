import hashlib

import redis


def encode(str, code='utf-8'):
    if not str:
        return b''
    return str.encode(code)


def decode(bytes, code='utf-8'):
    if not bytes:
        return u''
    return bytes.decode(code)


def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()


class DB(object):
    def __init__(self, host='localhost', port=6379, db=0, bucket='blocks'):
        self.bucket = bucket
        self.db = redis.Redis(host='localhost', port=6379, db=0)

    def put(self, key, val):
        self.db.hset(self.bucket, key, val)

    def get(self, key):
        # return bytes
        return self.db.hget(self.bucket, key)
