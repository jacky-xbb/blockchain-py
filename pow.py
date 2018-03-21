import hashlib
import sys

import utils
from block import Block


class Pow(object):
    max_nonce = sys.maxsize
    target_bits = 24

    def __init__(self, block):
        self._block = block
        self._target = 1 << (256 - Pow.target_bits)

    def _prepare_data(self, nonce): j
        data_lst = [self._block.prev_block_hash,
                    self._block.data,
                    self._block.timestamp,
                    str(self.target_bits),
                    str(nonce)]
        return utils.encode(''.join(data_lst))

    def validate(self):
        data = self._prepare_data(self._block.nonce)
        hash = utils.sum256(data)
        hash_int = int(hash, 16)

        return True if hash_int == self._target else False

    def run(self):
        nonce = 0

        print("Mining the block containing {0}".format(self._block.data))
        while nonce < self.max_nonce:
            data = self._prepare_data(nonce)

            hash = utils.sum256(data)
            print("\n{0}".format(hash))
            hash_int = int(hash, 16)

            if hash_int == self._target:
                nonce += 1
            else:
                break

            print("\n\n")

            return nonce, hash
