import sys
import pickle
import random
import string
import logging
log = logging.getLogger(__name__)

import ecdsa

import utils
import wallets as ws
from errors import NotEnoughFundsError
from transaction_output import TXOutput
from transaction_input import TXInput


class Transaction(object):
    """ Represents a transaction

    """

    def __init__(self, tx_id=None, vin=None, vout=None):
        self._id = tx_id
        self._vin = vin
        self._vout = vout

    def __repr__(self):
        return 'Transaction(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self.ID, self.vin, self.vout)

    @property
    def ID(self):
        return self._id

    @ID.setter
    def ID(self, id):
        self._id = id

    @property
    def vin(self):
        return self._vin

    @property
    def vout(self):
        return self._vout

    def set_id(self):
        # sets ID of a transaction
        self._id = self.hash()
        return self

    def hash(self):
        # returns the hash of the Transaction
        return utils.sum256_hex(pickle.dumps(self))

    def _trimmed_copy(self):
        inputs = []
        outputs = []

        for vin in self.vin:
            inputs.append(TXInput(vin.tx_id, vin.vout, None, None))

        for vout in self.vout:
            outputs.append(TXOutput(vout.value, vout.address))

        return Transaction(self.ID, inputs, outputs)

    def sign(self, priv_key, prev_txs):
        for vin in self.vin:
            if not prev_txs[vin.tx_id].ID:
                # log.error("Previous transaction is not correct")
                print("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(tx_copy.vin):
            prev_tx = prev_txs[vin.tx_id]
            tx_copy.vin[in_id].signature = None
            tx_copy.vin[in_id].public_key = prev_tx.vout[vin.vout].public_key_hash
            tx_copy.ID = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sk = ecdsa.SigningKey.from_string(
                priv_key, curve=ecdsa.SECP256k1)
            sig = sk.sign(utils.encode(tx_copy.ID))

            self.vin[in_id].signature = sig

    def verify(self, prev_txs):
        for vin in self.vin:
            if not prev_txs[vin.tx_id].ID:
                # log.error("Previous transaction is not correct")
                print("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(self.vin):
            prev_tx = prev_txs[vin.tx_id]
            tx_copy.vin[in_id].signature = None
            tx_copy.vin[in_id].public_key = prev_tx.vout[vin.vout].public_key_hash
            tx_copy.ID = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sig = self.vin[in_id].signature
            # vk = ecdsa.VerifyingKey.from_string(
            #     vin.public_key[2:], curve=ecdsa.SECP256k1)
            vk = utils.pubkey_to_verifykey(vin.public_key)
            if not vk.verify(sig, utils.encode(tx_copy.ID)):
                return False

        return True


class CoinbaseTx(object):
    """ Represents a coinbase transaction

    Args:
        to (string): address of coinbase.
        data (string): script of signature.

    Attributes:
        _id (tytes): Transaction ID.
        _vin (list): List of transaction input.
        _vout (list): List of transaction output.
    """

    def __init__(self, to, data=None):
        if not data:
            # data = 'Reward to {0}'.format(to)
            data = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(20))

        tx_id = None
        vin = [TXInput('', -1, None, data)]
        vout = [TXOutput(TXOutput.subsidy, to)]
        self._tx = Transaction(tx_id, vin, vout).set_id()

    def __repr__(self):
        return 'CoinbaseTx(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self._tx.ID, self._tx.vin, self._tx.vout)

    def to_bytes(self):
        return utils.serialize(self)

    @property
    def ID(self):
        return self._tx.ID

    @property
    def vin(self):
        return self._tx.vin

    @property
    def vout(self):
        return self._tx.vout

    def sign(self, priv_key, prev_txs):
        raise NotImplementedError

    def verify(self, prev_txs):
        raise NotImplementedError


class UTXOTx(object):
    """ Represents a UTXO transaction

    Args:
        from_addr (string): the address of sender.
        to_addr (string): the address of receiver.
        amount (int): amount you should to pay.
        utxo_set (UTXOSet object): a UTXO set.

    Attributes:
        _tx (Transaction object): a object of Transaction
        _utxo_set (UTXOSet object): a object of UTXO set.
    """

    def __init__(self, from_addr, to_addr, amount, utxo_set):
        inputs = []
        outputs = []

        # log('UTXOTx')
        wallets = ws.Wallets()
        wallet = wallets.get_wallet(from_addr)
        pubkey_hash = utils.hash_public_key(wallet.public_key)

        acc, valid_outputs = utxo_set.find_spendable_outputs(
            pubkey_hash, amount)
        if acc < amount:
            # log.error('Not enough funds')
            print('Not enough funds')
            sys.exit()

        # Build a list of inputs
        for tx_id, outs in valid_outputs.items():
            for out in outs:
                input = TXInput(tx_id, out, None, wallet.public_key)
                inputs.append(input)

        # Build a list of outputs
        outputs.append(TXOutput(amount, to_addr))
        if acc > amount:
            # A change
            outputs.append(TXOutput(acc-amount, from_addr))

        self._tx = Transaction(None, inputs, outputs).set_id()
        self._utxo_set = utxo_set
        self._sign_utxo(wallet.private_key)

    def to_bytes(self):
        return utils.serialize(self)

    def __repr__(self):
        return 'UTXOTx(id={0!r}, vin={1!r}, vout={2!r}, utxo_set={3!r})'.format(
            self._tx.ID, self._tx.vin, self._tx.vout, self._utxo_set)

    @property
    def ID(self):
        return self._tx.ID

    @property
    def vin(self):
        return self._tx.vin

    @property
    def vout(self):
        return self._tx.vout

    def _sign_utxo(self, private_key):
        self._utxo_set.blockchain.sign_transaction(self._tx, private_key)

    def sign(self, priv_key, prev_txs):
        self._tx.sign(priv_key, prev_txs)

    def verify(self, prev_txs):
        return self._tx.verify(prev_txs)
