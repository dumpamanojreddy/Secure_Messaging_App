from CBC import *

def AESencrypt(message, key):
    blks = block(message)
    IV = generate_IV()
    E = CBC(blks, key, IV)
    return [E, IV]

def AESdecrypt(blks, key, IV):
    blked = CBC_Inv(blks, key, IV)
return unblock(blked)
