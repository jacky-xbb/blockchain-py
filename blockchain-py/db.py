import pickle
from collections import defaultdict


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=Singleton):

    def __init__(self, db_file):
        self._db_file = db_file
        try:
            with open(self._db_file, 'rb') as f:
                self.kv = pickle.load(f)
        except FileNotFoundError:
            self.kv = defaultdict(dict)

    def commit(self):
        with open(self._db_file, 'wb') as f:
            pickle.dump(self.kv, f)

    def get(self, bucket, key):
        return self.kv[bucket][key]

    def put(self, bucket, key, value):
        self.kv[bucket][key] = value

    def delete(self, bucket, key):
        del self.kv[bucket][key]

    def reset(self, bucket):
        self.kv[bucket] = {}

    # def _has_key(self, key):
    #     return key in self.kv

    # def __contains__(self, key):
    #     return self._has_key(key)

    # def __eq__(self, other):
    #     return isinstance(other, self.__class__) and self.kv == other.kv


class Bucket(object):

    def __init__(self, db_file, bucket):
        self._db = DB(db_file)
        self._bucket = bucket

    def reset(self):
        self._db.reset(self._bucket)

    def get(self, key):
        return self._db.get(self._bucket, key)

    def put(self, key, value):
        self._db.put(self._bucket, key, value)

    def delete(self, key):
        self._db.delete(self._bucket, key)

    def commit(self):
        self._db.commit()

    @property
    def kv(self):
        return self._db.kv[self._bucket]


if __name__ == '__main__':
    # bucket_1 = Bucket('test.db', 'b1')
    # bucket_1.put('a', 1)
    # print(bucket_1.get('a'))
    # bucket_1.commit()

    # bucket_2 = Bucket('test.db', 'b2')
    # bucket_2.put('a', 2)
    # bucket_2.put('b', 3)
    # # print(bucket_1.get('a'))
    # # print(bucket_2.get('a'))
    # # print(bucket_2.get('b'))
    # print(bucket_2._db.kv)
    # bucket_2.commit()

    bucket_3 = Bucket('test.db', 'b3')
    print(bucket_3._db.kv)
