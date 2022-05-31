import os
import math
import random
import time
import hashlib

# Addictive Operation
def addOperation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return p

    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]

    if p == q:
        # Doubling
        # slope (s) = (s*x1^2+a)/(2*y1) mod m
        # get denominator's inver by fermat's little theorem
        r = 2 * y1
        rInv = pow(r, m - 2, m)
        s = (rInv * (3 * (x1**2) + a)) % m
    else:
        r = x2 - x1
        rInv = pow(r, m - 2, m)
        s = (rInv * (y2 - y1)) % m
    x3 = (s**2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3, y3

# create 256 bits random value by CSPRNG method using os.urandom() and rnadom()
def random_key():
    r = str(os.urandom(32))\
        +str(random.randrange(2**256))\
        +str(int(time.time()*1000000))
    r=bytes(r,'utf-8')
    h = hashlib.sha256(r).digest()
    key =''.join('{:02x}'.format(y) for y in h)
    return key

# Domin parameters of secp256k1
# y^2 = x^3 + 7 mod m
a=0
b=7
m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Create private key
while(1):
    d = int(random_key(),16)
    if d>0 & d<n:
        break

# Create public key by Double-and-Add algorithm
bits = bin(d)
bits = bits[2:len(bits)]
    
# initialize. bits[0]==1 always
K=G
    
# apply Double-and-Add algorithm from second bit
bits = bits[1:len(bits)]
for bit in bits:
    # Double
    K = addOperation(a,b,K,K,m)

    # Multiply
    if bit=='1':
        K = addOperation(a,b,K,G,m)

privKey = d
pubKey = K
print("\nPrivate Key : ", hex(privKey))
print("\n Public Key : (%s,\n        %s" % (hex(pubKey[0]), hex(pubKey[1])))
    