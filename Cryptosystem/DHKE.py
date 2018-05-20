import hashlib
import random

# Welcome to DHKE

# interface:

# PrivateKey = Integer less than P

# PublicKey = Integer

# SharedKey = 16 byte array

# generate_private_key() -> PrivateKey

# generate_public_key(PrivateKey) -> PublicKey

# generate_secret_key(PrivateKey, PublicKey) -> SharedKey


 P = 1255049
BASE = 113359


def generate_private_key():
    random.randint(2, P-2)


def generate_public_key(Priv):
    return pow(BASE, Priv, P)


def generate_secret_key(Priv, Pub):
    s = pow(Pub, Priv, P)
    s = hashlib.sha1(str(s)).hexdigest()
    i = 0
    key = []
    while i < 32:
        key += [int(s[i:i+2], 16)]
        i += 2
return key



