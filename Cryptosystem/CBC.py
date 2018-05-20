import random
from AES import *

# Welcome to CBC:

# Interface:

# block(string) -> (listof block)

# CBC((listof block), key, iv) -> (listof cipher)

# CBC_Inv((listof cipher), key, iv) -> (listof block)

# unblock((listof block)) -> string

# generate_IV() -> Random IV

# generate_key() -> Random key (for testing purposes)

ex_plaintext = "This is a test that is more than 16 characters"
ex_key = generate_key()
ex_IV = generate_IV()


# for testing purposes only 
def generate_key():
    key = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
          random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
          random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
          random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    return key


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
    xi.append(mess[i:] + "0000000000000000"[:16 - (len(mess) - i)])
    return xi

def unblock(blks):
    text =''
    for x in blks:
        text += x
    return text


def CBC(xi, key, iv):
    i = 0
    IV = iv
    new = ''
    yi = []
    while i < len(xi):
        for x in range(0, 16):
            new += chr(ord(xi[i][x]) ^ IV[x // 4][x % 4])
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















