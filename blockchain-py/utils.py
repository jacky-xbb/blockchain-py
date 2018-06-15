import hashlib
import binascii
import ecdsa
import unittest
import base58


# b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


# def base58_encode(n):
#     result = ''
#     while n > 0:
#         result = b58[n % 58] + result
#         n /= 58
#     return result


# def base58_decode(s):
#     result = 0
#     for i in range(0, len(s)):
#         result = result * 58 + b58.index(s[i])
#     return result


# def base256_encode(n):
#     result = ''
#     while n > 0:
#         result = chr(n % 256) + result
#         n /= 256
#     return result


# def base256_decode(s):
#     result = 0
#     import pdb
#     pdb.set_trace()
#     for c in s:
#         result = result * 256 + ord(c)
#     return result


# def count_leading_chars(s, ch):
#     count = 0
#     for c in s:
#         if c == ch:
#             count += 1
#         else:
#             break
#     return count


# def base58_check_encode(version, payload):
#     # https://en.bitcoin.it/wiki/Base58Check_encoding
#     s = version + payload
#     checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
#     result = s + checksum
#     leadingZeros = count_leading_chars(result, '\0')
#     return '1' * leadingZeros + base58_encode(base256_decode(result))


# def base58_check_decode(s):
#     leadingOnes = count_leading_chars(s, '1')
#     s = base256_encode(base58_decode(s))
#     result = '\0' * leadingOnes + s[:-4]
#     chk = s[-4:]
#     checksum = hashlib.sha256(hashlib.sha256(result).digest()).digest()[0:4]
#     assert(chk == checksum)
#     # version = result[0]
#     return result[1:]


def hash_public_key(pubkey):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest())
    return ripemd160.digest()
    # data = b'0' + ripemd160.digest()
    # return decode(base58.b58encode_check(data))


def get_address(pubkey_hash):
    data = b'0' + pubkey_hash
    return decode(base58.b58encode_check(data))


def address_to_pubkey_hash(address):
    # import pdb
    # pdb.set_trace()
    return base58.b58decode_check(encode(address))[1:]


def privatekey_to_wif(key):
    data = b'0x80' + binascii.hexlify(key)
    return base58.b58encode_check(data)


def privatekey_to_publickey(key):
    sk = ecdsa.SigningKey.from_string(key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return '04' + decode(binascii.hexlify(vk.to_string()))


def encode(str, code='utf-8'):
    return str.encode(code)


def decode(bytes, code='utf-8'):
    return bytes.decode(code)


def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()


class ContinueIt(Exception):
    pass


class BreakIt(Exception):
    pass
