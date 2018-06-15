import sys
import pickle
try:
    from logbook import Logger
    Logger = Logger   # Does nothing except it shuts up pyflakes annoying error
except ImportError:
    from logging import Logger
from abc import ABCMeta, abstractclassmethod

import ecdsa
import base58

import utils
import wallets as ws
from errors import NotEnoughFundsError


class TXInput(object):
    """ Represents a transaction input

    Args:
        txid (string): Transaction ID.
        vout (int): Transaction output value.
        sig (string): Signature.
        pubkey (string): Public key.

    Attributes:
        _tx_id (bytes): Transaction ID.
        _vout (int): Transaction output value.
        _sig (string): Signature.
        _public_key (string): Public key.
    """

    def __init__(self, txid, vout, sig, pubkey):
        self._tx_id = utils.encode(txid)
        self._vout = vout
        self._sig = sig
        self._public_key = pubkey

    def uses_key(self, pubkey_hash):
        # checks whether the address initiated the transaction
        pubkey_hash = utils.hash_public_key(self._public_key)
        return pubkey_hash == pubkey_hash

    def __repr__(self):
        return 'TXInput(tx_id={0!r}, vout={1!r}, signature={2!r}, public_key={3!r})'.format(
            self._tx_id, self._vout, self._sig, self._public_key)

    @property
    def tx_id(self):
        return utils.decode(self._tx_id)

    @property
    def vout(self):
        return self._vout

    @property
    def signature(self):
        return self._sig

    @property
    def public_key(self):
        return self._public_key

    @signature.setter
    def signature(self, sig):
        self._sig = sig

    @public_key.setter
    def public_key(self, public_key):
        self._public_key = public_key


class TXOutput(object):
    """ Represents a transaction output

    Args:
        value (int): Transaction output.
        address (string): Address of WIF.

    Attributes:
        _value (int): Transaction output.
        _public_key_hash (string): Hash of a public key.

    """

    # the amount of reward
    subsidy = 10

    def __init__(self, value, address):
        self._value = value
        self._public_key_hash = self._lock(address)

    @staticmethod
    def _lock(address):
        # import pdb
        # pdb.set_trace()
        return utils.address_to_pubkey_hash(address)

    def __repr__(self):
        return 'TXOutput(value={0!r}, public_key_hash={1!r})'.format(
            self._value, self._public_key_hash)

    def is_locked_with_key(self, pubkey_hash):
        return self._public_key_hash == pubkey_hash

    @property
    def value(self):
        return self._value

    @property
    def public_key_hash(self):
        return self._public_key_hash


class Transaction(object):
    """ Represents a ABC transaction 

    """

    __metaclass__ = ABCMeta

    def __init__(self, id=None, vin=None, vout=None):
        self._id = id
        self._vin = vin
        self._vout = vout

    @property
    def ID(self):
        return self._id

    @property
    def vin(self):
        return self._vin

    @property
    def vout(self):
        return self._vout

    def set_id(self):
        # sets ID of a transaction
        self._id = utils.sum256(pickle.dumps(self))
        return self

    def hash(self):
        # returns the hash of the Transaction
        return utils.sum256(pickle.dumps(self))

    @abstractclassmethod
    def tx_type(self):
        raise NotImplementedError


class CoinbaseTx(Transaction):
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
            data = 'Reward to {0}'.format(to)

        self._id = None
        self._vin = [TXInput('', -1, None, data)]
        self._vout = [TXOutput(TXOutput.subsidy, to)]

    def __repr__(self):
        return 'CoinbaseTx(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self._id, self._vin, self._vout)

    def tx_type(self):
        return u'Coinbase'

    # def is_coinbase(self):
    #     # checks whether the transaction is coinbase
    #     return len(self._vin) == 1 and \
    #         len(self._vin[0].tx_id) == 0 and \
    #         self._vin[0].vout == -1


class UTXOTx(Transaction):
    """ Represents a UTXO transaction 

    Args:
        from_addr (string): address of from.
        to_addr (string): address of to.
        amount (int): amount you should to pay.
        bc (blcokchain object): a blockchain.

    Attributes:
        _id (tytes): Transaction ID.
        _vin (list): List of transaction input.
        _vout (list): List of transaction output.
    """

    def __init__(self, from_addr, to_addr, amount, bc):
        inputs = []
        outputs = []

        self.log = Logger('UTXOTx')
        wallets = ws.Wallets()
        wallet = wallets.get_wallet(from_addr)
        pubkey_hash = utils.hash_public_key(wallet.public_key)

        # acc, valid_outputs = bc.find_spendable_outputs(
        #     base58.b58decode_check(pubkey_hash), amount)
        acc, valid_outputs = bc.find_spendable_outputs(pubkey_hash, amount)
        # import pdb
        # pdb.set_trace()
        if acc < amount:
            self.log.error('Not enough funds')
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

        self._id = None
        self._vin = inputs
        self._vout = outputs

    def __repr__(self):
        return 'UTXOTx(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self._id, self._vin, self._vout)

    def tx_type(self):
        return u'UTXO'

    def _trimmed_copy(self):
        inputs = []
        outputs = []

        for vin in self.vin:
            inputs.append(TXInput(vin.tx_id, vin.vout, None, None))

        for vout in self.vout:
            outputs.append(TXOutput(vout.value, vout.public_key_hash))

        return Transaction(self.ID, inputs, outputs)

    def sign(self, priv_key, prev_txs):
        for vin in self.vin:
            if not prev_txs[vin.tx_id].ID:
                self.log.error("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(tx_copy.vin):
            prev_tx = prev_txs[vin.tx_id]
            tx_copy.vin[in_id].signature = None
            tx_copy.vin[in_id].public_key = prev_tx.out[vin.vout].public_key_hash
            tx_copy.ID = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sk = ecdsa.SigningKey.from_string(
                priv_key.hex(), curve=ecdsa.SECP256k1)
            sig = sk.sign(tx_copy.ID)

            self.vin[in_id].signature = sig

    def verify(self, prev_txs):
        for vin in self.vin:
            if not prev_txs[vin.tx_id].ID:
                self.log.error("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(tx_copy.vin):
            prev_tx = prev_txs[vin.tx_id]
            tx_copy.vin[in_id].signature = None
            tx_copy.vin[in_id].public_key = prev_tx.out[vin.vout].public_key_hash
            tx_copy.ID = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sig = self.vin[in_id].signature
            vk = ecdsa.VerifyingKey.from_string(
                vin.public_key[2:].decode('hex'), curve=ecdsa.SECP256k1)
            if not vk.verify(sig, tx_copy.ID):
                return False

        return True
