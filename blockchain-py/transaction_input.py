import utils


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
