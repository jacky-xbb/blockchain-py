import argparse

from blockchain import Blockchain
from pow import Pow


def new_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(help='commands')
    # A print command
    print_parser = sub_parser.add_parser(
        'print', help='Print all the blocks of the blockchain')
    print_parser.add_argument('--print', dest='print', action='store_true')
    # A getbalance command
    balance_parser = sub_parser.add_parser(
        'getbalance', help='Get balance of ADDRESS')
    balance_parser.add_argument(
        '--address', type=str, dest='balance_address', help='ADDRESS of balance')
    # A createblockchain command
    bc_parser = sub_parser.add_parser(
        'createblockchain', help='Create a blockchain and send genesis block reward to ADDRESS')
    bc_parser.add_argument(
        '--address', type=str, dest='blockchain_address', help='ADDRESS')

    return parser


def get_balance(address):
    bc = Blockchain()

    balance = 0
    UTXOs = bc.find_utxo(address)

    for out in UTXOs:
        balance += out.value

    print('Balance of {0}: {1}'.format(address, balance))


def create_blockchain(address):
    Blockchain(address)
    print('Done!')


def print_chain():
    bc = Blockchain()

    for block in bc.blocks:
        print("Prev. hash: {0}".format(block.prev_block_hash))
        print("Data: {0}".format(block.data))
        print("Hash: {0}".format(block.hash))
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))


def hello():
    print('hello')


if __name__ == '__main__':
    parser = new_parser()
    args = parser.parse_args()

    if hasattr(args, 'print'):
        print_chain()

    if hasattr(args, 'balance_address'):
        get_balance(args.balance_address)

    if hasattr(args, 'blockchain_address'):
        create_blockchain(args.blockchain_address)
