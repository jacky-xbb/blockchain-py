import utils


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
        self._address = address
        self._public_key_hash = self._lock(address)

    @staticmethod
    def _lock(address):
        return utils.address_to_pubkey_hash(address)

    def __repr__(self):
        return 'TXOutput(address={0!r}, value={1!r}, public_key_hash={2!r})'.format(
            self._address, self._value, self._public_key_hash)

    def is_locked_with_key(self, pubkey_hash):
        return self._public_key_hash == pubkey_hash

    @property
    def value(self):
        return self._value

    @property
    def address(self):
        return self._address

    @property
    def public_key_hash(self):
        return self._public_key_hash


# class TXOutputs(object):
#     def __init__(self, outputs=None):
#         if not outputs:
#             self.outputs = []
#         else:
#             self.outputs = outputs[:]

#     def serialize(self):
#         return pickle.dumps(self.outputs)

#     def deserialize(self, data):
#         return pickle.loads(data)
