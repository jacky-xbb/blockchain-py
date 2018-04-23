import pickle


class BaseDB(object):
    pass


class DB(BaseDB):

    def __init__(self, db_file):
        self._db_file = db_file
        try:
            with open(self._db_file, 'rb') as f:
                self.kv = pickle.load(f)
        except FileNotFoundError:
            self.kv = {}

    def get(self, key):
        return self.kv[key]

    def put(self, key, value):
        self.kv[key] = value

    def delete(self, key):
        del self.kv[key]

    def commit(self):
        with open(self._db_file, 'wb') as f:
            pickle.dump(self.kv, f)

    def _has_key(self, key):
        return key in self.kv

    def __contains__(self, key):
        return self._has_key(key)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.kv == other.kv
