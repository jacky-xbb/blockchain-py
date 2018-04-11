import pickle
from collections import defaultdict


from block import Block
from db import DB
from transaction import CoinbaseTx
from utils import ContinueIt, BreakIt


class Blockchain(object):
    """ Blockchain keeps a sequence of Blocks

    Attributes:
        _tip (bytes): Point to the latest hash of block.
        _db (DB): DB instance
    """
    latest = 'l'
    db_file = 'blockchain.db'
    genesis_coinbase_data = 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

    def __init__(self, address=None):
        self._db = DB(Blockchain.db_file)

        try:
            self._tip = self._db.get('l')
        except KeyError:
            if not address:
                self._tip = None
            else:
                cb_tx = CoinbaseTx(address, Blockchain.genesis_coinbase_data).set_id()
                genesis = Block([cb_tx]).pow_of_block()
                self._block_put(genesis)

    def _block_put(self, block):
        self._db.put(block.hash, block.serialize())
        self._db.put('l', block.hash)
        self._tip = block.hash
        self._db.commit()

    def MineBlock(self, transaction_lst):
        # Mines a new block with the provided transactions
        last_hash = self._db.get('l')
        new_block = Block(transaction_lst, last_hash)
        self._block_put(new_block)

    def find_utxo(self, address=None):
        # Finds and returns all unspent transaction outputs
        utxos = []
        unspent_txs = self.find_unspent_transactions(address)

        for tx in unspent_txs:
            for out in tx.vout:
                if out.canbe_unlocked_with(address):
                    utxos.append(out)

        return utxos

    def find_unspent_transactions(self, address):
        # Returns a list of transactions containing unspent outputs
        spent_txo = defaultdict(list)
        unspent_txs = []
        for block in self.blocks:
            for tx in block.transactions:
                tx_id = tx.ID

                try:
                    for out_idx, out in enumerate(tx.vout):
                        # Was the output spent?
                        if not spent_txo[tx_id]:
                            for spent_out in spent_txo[tx_id]:
                                if spent_out == out_idx:
                                    raise ContinueIt

                        if out.canbe_unlocked_with(address):
                            unspent_txs.append(tx)
                except ContinueIt:
                    pass

                    if not tx.is_coinbase():
                        for vin in tx.vin:
                            if vin.can_unlock_output_with(address):
                                tx_id = vin.tx_id
                                spent_txo[tx_id].append(vin.vout)

        return unspent_txs

    def find_spendable_outputs(self, address, amount):
        # Finds and returns unspent outputs to reference in inputs
        accumulated = 0
        unspent_outputs = defaultdict(list)
        unspent_txs = self.find_unspent_transactions(address)

        try:
            for tx in unspent_txs:
                tx_id = tx.ID

                for out_idx, out in enumerate(tx.vout):
                    if out.canbe_unlocked_with(address) and accumulated < amount:
                        accumulated += out.value
                        unspent_outputs[tx_id].append(out_idx)

                        if accumulated >= amount:
                            raise BreakIt
        except BreakIt:
            pass

        return accumulated, unspent_outputs

    @property
    def blocks(self):
        if not self._tip:
            return []
        current_tip = self._tip
        while True:
            encoded_block = self._db.get(current_tip)
            block = pickle.load(encoded_block)
            yield block
            current_tip = block.prev_block_hash
