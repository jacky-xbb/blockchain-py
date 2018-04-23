import argparse

from blockchain import Blockchain
from transaction import UTXOTx
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
    # A send command
    send_parser = sub_parser.add_parser(
        'send', help='Send AMOUNT of coins from FROM address to TO')
    send_parser.add_argument(
        '--from', type=str, dest='send_from', help='FROM')
    send_parser.add_argument(
        '--to', type=str, dest='send_to', help='TO')
    send_parser.add_argument(
        '--amount', type=int, dest='send_amount', help='AMOUNT')

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
        print("Hash: {0}".format(block.hash))
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))


def send(from_addr, to_addr, amount):
    bc = Blockchain()

    tx = UTXOTx(from_addr, to_addr, amount, bc).set_id()
    bc.MineBlock([tx])
    print('Success!')


if __name__ == '__main__':
    parser = new_parser()
    args = parser.parse_args()

    if hasattr(args, 'print'):
        print_chain()

    if hasattr(args, 'balance_address'):
        get_balance(args.balance_address)

    if hasattr(args, 'blockchain_address'):
        create_blockchain(args.blockchain_address)

    if hasattr(args, 'send_from') and \
            hasattr(args, 'send_to') and \
            hasattr(args, 'send_amount'):
        send(args.send_from, args.send_to, args.send_amount)


# command
"""
python cli.py createblockchain --address Ivan 
python cli.py getbalance --address Ivan
python cli.py send --from Ivan --to bxb --amount 6
python cli.py getbalance --address Ivan
python cli.py print
"""
