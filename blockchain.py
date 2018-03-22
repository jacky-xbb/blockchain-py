from block import Block


class Blockchain(object):
    def __init__(self):
        block = Block()
        self._blocks = [block.pow_of_block()]

    def add_block(self, data):
        # AddBlock saves provided data as a block in the blockchain
        prev_block_hash = self._blocks[len(self._blocks)-1].hash
        block = Block(data, prev_block_hash)
        self._blocks.append(block.pow_of_block())

    @property
    def blocks(self):
        return self._blocks
