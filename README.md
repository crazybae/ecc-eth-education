# ECDSA and Ethereum transaction eduction module

## 사전 준비 사항

- Python 3.8.5 for Windows / Ubuntu / MacOS
- ECDSA cryptography library for education (tynyec)
- Common utility functions for Ethereum development (eth-utils)
- SHA-3 wrapper (keccak) for Python (pysha3)
- Python library for interacting with Ethereum (web3)

```
pip install eth-utils
pip install pysha3
pip install rlp
pip install requests
pip install tinyec
pip install web3

```

## Education Goals

- Understanding 
  - Basic concepts of elliptic curve cryptography
  - Logics from private keys to public keys to Ethereum addresses
- Using web3 module to
  - retrieve balance, nonce
  - inquiry gas fee estimation
  - prepare, sign, monitor, and broadcast transactions