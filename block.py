import time
import hashlib


class Block(object):
    CODE = 'utf-8'

    def __init__(self, data='Genesis Block', prev_block_hash=''):
        self._timestamp = str(int(time.time())).encode(Block.CODE)
        self._data = data.encode(Block.CODE)
        self._prev_block_hash = prev_block_hash.encode(Block.CODE)
        self._hash = self._set_hash()

    def _set_hash(self):
        # SetHash calculates and sets block hash
        m = hashlib.sha256()
        m.update(self._timestamp)
        m.update(self._data)
        m.update(self._prev_block_hash)
        return m.hexdigest().encode(Block.CODE)

    @property
    def hash(self):
        return self._hash.decode(Block.CODE)

    @property
    def data(self):
        return self._data.decode(Block.CODE)

    @property
    def prev_block_hash(self):
        return self._prev_block_hash.decode(Block.CODE)

    @property
    def timestamp(self):
        return str(self._timestamp)


class Blockchain(object):
    def __init__(self):
        self._blocks = [Block()]

    def add_block(self, data):
        # AddBlock saves provided data as a block in the blockchain
        prev_block_hash = self._blocks[len(self._blocks)-1].hash
        self._blocks.append(Block(data, prev_block_hash))

    @property
    def blocks(self):
        return self._blocks
