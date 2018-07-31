import sys
import pickle
from collections import defaultdict


from block import Block
from db import Bucket
from transaction import CoinbaseTx
from utils import ContinueIt, BreakIt
from errors import NotFoundTransaction


class Blockchain(object):
    """ Blockchain keeps a sequence of Blocks

    Attributes:
        _tip (bytes): Point to the latest hash of block.
        _bucket (dict): bucket of DB 
    """
    latest = 'l'
    db_file = 'blockchain.db'
    block_bucket = 'blocks'
    genesis_coinbase_data = 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

    def __init__(self, address=None):
        self._bucket = Bucket(Blockchain.db_file, Blockchain.block_bucket)

        try:
            self._tip = self._bucket.get('l')
        except KeyError:
            if not address:
                self._tip = None
            else:
                cb_tx = CoinbaseTx(
                    address, Blockchain.genesis_coinbase_data)
                genesis = Block([cb_tx]).pow_of_block()
                self._block_put(genesis)

    def _block_put(self, block):
        self._bucket.put(block.hash, block.serialize())
        self._bucket.put('l', block.hash)
        self._tip = block.hash
        self._bucket.commit()

    def MineBlock(self, transaction_lst):
        # Mines a new block with the provided transactions
        last_hash = self._bucket.get('l')

        for tx in transaction_lst:
            if not self.verify_transaction(tx):
                print("ERROR: Invalid transaction")
                sys.exit()

        new_block = Block(transaction_lst, last_hash).pow_of_block()
        self._block_put(new_block)
        return new_block

    def find_unspent_transactions(self, pubkey_hash):
        # Returns a list of transactions containing unspent outputs
        spent_txo = defaultdict(list)
        unspent_txs = []
        for block in self.blocks:
            for tx in block.transactions:

                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vin:
                        if vin.uses_key(pubkey_hash):
                            tx_id = vin.tx_id
                            spent_txo[tx_id].append(vin.vout)

                tx_id = tx.ID
                try:
                    for out_idx, out in enumerate(tx.vout):
                        # Was the output spent?
                        if spent_txo[tx_id]:
                            for spent_out in spent_txo[tx_id]:
                                if spent_out == out_idx:
                                    raise ContinueIt

                        if out.is_locked_with_key(pubkey_hash):
                            unspent_txs.append(tx)
                except ContinueIt:
                    pass

        return unspent_txs

    def find_utxo(self):
        # Finds all unspent transaction outputs
        utxo = defaultdict(list)
        spent_txos = defaultdict(list)

        for block in self.blocks:
            for tx in block.transactions:

                try:
                    for out_idx, out in enumerate(tx.vout):
                        # Was the output spent?
                        if spent_txos[tx.ID]:
                            for spent_out in spent_txos[tx.ID]:
                                if spent_out == out_idx:
                                    raise ContinueIt

                        utxo[tx.ID].append(out)
                except ContinueIt:
                    pass

                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vin:
                        spent_txos[vin.tx_id].append(vin.vout)

        return utxo

    @property
    def blocks(self):
        current_tip = self._tip
        while True:
            if not current_tip:
                # Encounter genesis block
                raise StopIteration
            encoded_block = self._bucket.get(current_tip)
            block = pickle.loads(encoded_block)
            yield block
            current_tip = block.prev_block_hash

    def find_transaction(self, ID):
        # finds a transaction by its ID
        for block in self.blocks:
            for tx in block.transactions:
                if tx.ID == ID:
                    return tx

        # return None
        raise NotFoundTransaction

    def sign_transaction(self, tx, priv_key):
        prev_txs = {}
        for vin in tx.vin:
            prev_tx = self.find_transaction(vin.tx_id)
            prev_txs[prev_tx.ID] = prev_tx

        tx.sign(priv_key, prev_txs)

    def verify_transaction(self, tx):
        if isinstance(tx, CoinbaseTx):
            return True

        prev_txs = {}
        for vin in tx.vin:
            prev_tx = self.find_transaction(vin.tx_id)
            prev_txs[prev_tx.ID] = prev_tx

        return tx.verify(prev_txs)
