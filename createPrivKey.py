import os
import random
import time
import hashlib

# secp256k1's Domain Parameter(order of G)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# by CSPRNG method, mix os.urandom() and random()
# and create 256 bits random value by hash256
def random_key():
    r = (
        str(os.urandom(32))
        + str(random.randrange(2**256))
        + str(int(time.time() * 1000000))
    )
    r = bytes(r, "utf-8")
    h = hashlib.sha256(r).digest()
    key = "".join("{:02x}".format(y) for y in h)
    return key


# pass when secp256k1's value is less than n
while 1:
    privKey = random_key()
    if int(privKey, 16) < N:
        break

print("PrivKey (Hex) : ", privKey)
print("privKey (Dec) : ", int(privKey, 16))
