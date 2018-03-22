import time
import hashlib

import utils
from pow import Pow


class Block(object):

    def __init__(self, data='Genesis Block', prev_block_hash=''):
        self._timestamp = utils.encode(str(int(time.time())))
        self._data = utils.encode(data)
        self._prev_block_hash = utils.encode(prev_block_hash)
        self._hash = None
        self._nonce = None

    def pow_of_block(self):
        pow = Pow(self)
        nonce, hash = pow.run()
        self._nonce, self._hash = nonce, utils.encode(hash)
        return self

    @property
    def hash(self):
        return utils.decode(self._hash)

    @property
    def data(self):
        return utils.decode(self._data)

    @property
    def prev_block_hash(self):
        return utils.decode(self._prev_block_hash)

    @property
    def timestamp(self):
        return str(self._timestamp)

    @property
    def nonce(self):
        return str(self._nonce)
