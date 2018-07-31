from collections import defaultdict
import json

import utils
from db import Bucket
from transaction import CoinbaseTx


class UTXOSet(object):
    db_file = 'blockchain.db'
    utxo_bucket = 'utxo'

    def __init__(self, blockchain):
        self._bucket = Bucket(UTXOSet.db_file, UTXOSet.utxo_bucket)
        self._bc = blockchain

    @property
    def blockchain(self):
        return self._bc

    def reindex(self):
        # Rebuilds the UTXO set
        self._bucket.reset()

        utxos = self._bc.find_utxo()
        for tx_id, outs in utxos.items():
            self._bucket.put(tx_id, utils.serialize(outs))

        self._bucket.commit()

    def find_spendable_outputs(self, pubkey_hash, amount):
        # Finds and returns unspent outputs to reference in inputs
        accumulated = 0
        unspent_outputs = defaultdict(list)

        for tx_id, outs in self._bucket.kv.items():
            outs = utils.deserialize(outs)

            for out_idx, out in enumerate(outs):
                if out.is_locked_with_key(pubkey_hash) and accumulated < amount:
                    accumulated += out.value
                    unspent_outputs[tx_id].append(out_idx)

        return accumulated, unspent_outputs

    def find_utxo(self, pubkey_hash):
        # Finds UTXO for a public key hash
        utxos = []

        for _, outs in self._bucket.kv.items():
            outs = utils.deserialize(outs)

            for out in outs:
                if out.is_locked_with_key(pubkey_hash):
                    utxos.append(out)

        return utxos

    def print_utxo(self):
        utxos = []

        for _, outs in self._bucket.kv.items():
            outs = utils.deserialize(outs)
            for out in outs:
                print(out)

    def count_transactions(self):
        # Returns the number of transactions in the UTXO set
        return len(self._bucket)

    def update(self, block):
        # Updates the UTXO set with transactions from the Block
        for tx in block.transactions:
            if not isinstance(tx, CoinbaseTx):
                for vin in tx.vin:
                    update_outs = []
                    outs_bytes = self._bucket.get(vin.tx_id)
                    outs = utils.deserialize(outs_bytes)

                    for out_idx, out in enumerate(outs):
                        if out_idx != vin.vout:
                            update_outs.append(out)

                    if len(update_outs) == 0:
                        self._bucket.delete(vin.tx_id)
                    else:
                        self._bucket.put(
                            vin.tx_id, utils.serialize(update_outs))
            # Add new outputs
            new_outputs = [out for out in tx.vout]
            self._bucket.put(tx.ID, utils.serialize(new_outputs))

        self._bucket.commit()

    @property
    def utxo_set(self):
        return {k: utils.deserialize(v) for k, v in self._bucket.kv.items()}
