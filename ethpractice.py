# ECDSA and Ethereum transaction eduction module

import sys
from random import SystemRandom
import sha3
import time
import rlp
import requests

from tinyec.ec import SubGroup, Curve, Point, mod_inv
import web3
from eth_utils import (
    keccak,
    int_to_big_endian,
    big_endian_to_int,
    to_checksum_address,
)

from decimal import Decimal

# - global vars

BarPrint = "----------------------------------------------"

# for communicating with Ethereum kovan testnet 
WEB3 = web3.Web3(web3.HTTPProvider('https://kovan.infura.io/v3/6ce49391e58049228c984c3206459aa1'))    # kbae
ETHERSCAN_API = 'http://api-kovan.etherscan.io/api'

# -- Ethereum helper functions

# get an Ethereum address from x, y coordinates of a pubkey
def get_ethaddress(x, y):

    raw = b''.join((
        pad32(int_to_big_endian(x)), pad32(int_to_big_endian(y))
        ))

    k = sha3.keccak_256()
    k.update(raw)
    kec = k.digest()[-20:]

    ethaddr = to_checksum_address(kec)

    return ethaddr

def pad32(value: bytes) -> bytes:
    return value.rjust(32, b'\x00')

# get Ethereum balance from Ethereum testnet
def get_balance(address):
    return WEB3.eth.getBalance(address)  # wei amount

# get gas fee estimations from Ethereum gas station
def gasfee_est_from_station():
    est = requests.get('https://ethgasstation.info/json/ethgasAPI.json').json()
    fastest = WEB3.toWei(est["fastest"]/10, 'gwei')
    fast = WEB3.toWei(est["fast"]/10, 'gwei')
    average = WEB3.toWei(est["average"]/10, 'gwei')
    safeLow = WEB3.toWei(est["safeLow"]/10, 'gwei')

    print(f'Gas fee estimation\n Fastest: {fastest}\n Fast   : {fast}\n Average: {average}\n SafeLow: {safeLow}')

    return fast

# get a new nonce of address to prepare a new transaction
def get_nonce(address):
    return WEB3.eth.getTransactionCount(address)

# get Ethereum wallet information
def get_wallet_info(x, y):
    address = get_ethaddress(x, y)
    balance = get_balance(address)
    ethbalance = WEB3.fromWei(balance, 'ether')

    return address, ethbalance

# send an Ethereum transfer transaction
def send_eth(sk):

    toAddr = input("Enter recipient's address: ")
    amount = input("Enter amount (Ether): ")

    s256 = secp256k1()
    pubKey = s256.g * sk

    address = get_ethaddress(pubKey.x, pubKey.y)
    gasfee = gasfee_est_from_station()
    nonce = get_nonce(address)

    signed_txn = WEB3.eth.account.signTransaction(
        {
            'nonce': nonce,
            'gasPrice': gasfee,
            'from': address,
            'gas': 21000,
            'to': toAddr,
            'chainId': 42,
            'value': WEB3.toWei(amount, 'ether')
        },
        hex(sk)
    )
    print(signed_txn)

    return WEB3.eth.sendRawTransaction(signed_txn.rawTransaction)


# -- general elliption curve functions

def secp256k1():
    name = 'secp256k1'
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    a = 0x0000000000000000000000000000000000000000000000000000000000000000
    b = 0x0000000000000000000000000000000000000000000000000000000000000007
    g = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
        0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
    h = 1
    curve = Curve(a, b, SubGroup(p, g, n, h), name)

    return curve

def print_curve_params(curve):
    print(f'curve name:       {curve.name}')
    print(f'curve equation:   y^2 = x^3 + {curve.a}x + {curve.b} (mod p)')
    print(f'base field order: {curve.field.p}')
    print(f'EC group order:   {curve.field.n}')
    print(f'Generator.x:      {curve.g.x}')
    print(f'Generator.y:      {curve.g.y}')

# -- main function

def main():

    if len(sys.argv) != 2:
        print("\nUsage: $ python ethpractice.py (curve | key | wallet | transfer)\n")
        return

    # Modify for your own address
    MySecretKey = 21343688835301941572950132213128418439664108536245453048167327443418888658104

    option = sys.argv[1]
    if option == "curve":
        print("\n[SECP256K1 curve details]\n"+BarPrint)
        s256 = secp256k1()
        print_curve_params(s256)
        print(BarPrint+"\n")

    elif option == "key":
        print("\n[Keypair info]\n"+BarPrint)
        privKey = MySecretKey
        s256 = secp256k1()
        pubKey = s256.g * privKey
        print(f'SK: {privKey}\nPubKey: x= {pubKey.x}  y= {pubKey.y}')
        print(BarPrint+"\n")

    elif option == "wallet":
        print("\n[Wallet info]\n"+BarPrint)
        privKey = MySecretKey
        s256 = secp256k1()
        pubKey = privKey * s256.g
        address, ethbalance = get_wallet_info(pubKey.x, pubKey.y)
        print(f'Eth Address: {address}  Balance: {ethbalance}')
        print(BarPrint+"\n")

    elif option == "transfer":
        print("\n[Ether transfer (kovan)]\n"+BarPrint)
        txid = send_eth(MySecretKey)

        print(f'txid: {txid}')
        print("Sent. Wait 5 seconds to get tx info ...")
        time.sleep(5)

        txdetails = WEB3.eth.getTransaction(txid)
        print(f' txdetails: {txdetails}')

        print(BarPrint+"\n")

    else:
        print("\nUsage: $ python ethpractice.py (curve | key | wallet | transfer)\n")

if __name__ == "__main__":
    main()

