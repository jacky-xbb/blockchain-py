from block import Block

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