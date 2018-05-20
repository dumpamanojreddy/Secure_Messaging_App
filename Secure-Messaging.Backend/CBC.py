import random
from aes import *

# Welcome to CBC:

# Interface:

# block(string) -> (listof block)

# CBC((listof block), key, iv) -> (listof cipher)

# CBC_Inv((listof cipher), key, iv) -> (listof block)

# unblock((listof block)) -> string

# generate_IV() -> Random IV


ex_plaintext = "This is a test that is more than 16 characters"


def generate_IV():
    IV = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]]

    return IV


def block(mess):
    i = 0
    xi = []
    while i < len(mess) - 16:
        xi.append(mess[i:i+16])
        i = i + 16
    xi.append(mess[i:] + "~~~~~~~~~~~~~~~~"[:16 - (len(mess) - i)])
    return xi

def unblock(blks):
    text =''
    x = 0
    while x < len(blks) - 1:
        text += blks[x]
        x += 1
    text += unpad(blks[x])
    return text


def unpad(str):
    x = 0
    while x < len(str):
        if str[x] == '~':
            return str[0:x]
        x += 1
    return str;



def CBC(xi, key, iv):
    i = 0
    IV = iv
    new = ''
    yi = []
    while i < len(xi):
        for x in range(0, 16):
            t = (ord(xi[i][x]) ^ IV[x // 4][x % 4])
            new += chr(t)
        yi += [encrypt(new, key)]
        new = ''
        IV = yi[i]
        i += 1
    return yi


def CBC_Inv(yi, key, iv):
    new = ''
    i = 0
    IV = iv
    xi = []
    while i < len(yi):
        xi += [decrypt(yi[i], key)]
        for x in range(0, 16):
            new += chr(ord(xi[i][x]) ^ IV[x // 4][x % 4])
        xi[i] = new
        IV = yi[i]
        i += 1
        new = ''
    return xi

def AESencrypt(message, key):
    blks = block(message)
    IV = generate_IV()
    E = CBC(blks, key, IV)
    return [E, IV]

def AESdecrypt(blks, key, IV):
    blked = CBC_Inv(blks, key, IV)
    return unblock(blked)















