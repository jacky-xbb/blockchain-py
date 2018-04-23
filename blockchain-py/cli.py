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
    # A add command
    add_parser = sub_parser.add_parser(
        'addblock', help='Print all the blocks of the blockchain')
    add_parser.add_argument(
        '--data', type=str, dest='add_data', help='block data')

    return parser


def add_block(bc, data):
    bc.add_block(data)
    print("Success!")


def print_chain(bc):
    for block in bc.blocks:
        print("Prev. hash: {0}".format(block.prev_block_hash))
        print("Data: {0}".format(block.data))
        print("Hash: {0}".format(block.hash))
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))


if __name__ == '__main__':
    parser = new_parser()
    args = parser.parse_args()
    bc = Blockchain()

    if hasattr(args, 'print'):
        print_chain(bc)

    if hasattr(args, 'add_data'):
        add_block(bc, args.add_data)
