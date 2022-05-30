# Digital Signature Algorithm
import math
import random
from Cryptodome.Hash import SHA256

# secp256k1's domain parameters
# y^2 = x^3 + 7 mod m
a = 0
b = 7
m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# addictive operation
def addOperation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return p

    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]

    if p == q:
        # Doubling
        # slope (s) = (3*x1^2+a)/(2*y1) mod m
        # get denominator's inver by Fermat's little theorem
        r = 2 * y1
        rInv = pow(r, m - 2, m)
        s = (rInv * (3*(x1**2)+a)) % m
    else:
        r = x2 - x1
        rInv = pow(r, m - 2, m)
        s = (rInv * (y2 - y1)) % m
    x3 = (s**2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3,y3 


# create private key
def generatePrivKey():
    while 1:
        d = random.getrandbits(256)
        if d > 0 & d < n:
            break
    return d


# create public key
def generatePubKey(d, g):
    bits = bin(d)
    bits = bits[2 : len(bits)]

    # initialize. bits[0] = 1 (always)
    K = g

    # Double-and-Add from second bit
    bits = bits[1 : len(bits)]
    for bit in bits:
        # Double
        K = addOperation(a, b, K, K, m)

        # Multiply
        if bit == "1":
            K = addOperation(a, b, K, g, m)

    return K


# document to sign
message = "sign to this document"
message = message.encode()

# generate privKey and PubKey
d = generatePrivKey()
Q = generatePubKey(d, G)

# generate ephemeral key
k = generatePrivKey()
x, y = generatePubKey(k, G)
r = x % n

# Signing
h = SHA256.new()
h.update(message)
hx = h.hexdigest()
hx = int(hx, 16)

invK = pow(k, n - 2, n)  # Fermat's little theorem
s = ((hx + d * r) * invK) % n

# send digital signature
print("\nMessage=", message.decode())
print("\nCreating digital signature :")
print("h(x) =", hex(hx))
print(" r =", hex(r))
print(" s =", hex(s))

# verification
w = pow(s, n - 2, n)
u1 = (w * hx) % n
u2 = (w * r) % n
v1 = generatePubKey(u1, G)
v2 = generatePubKey(u2, Q)
x, y = addOperation(a, b, v1, v2, m)

print("\nVerifying digital signature :")
print("h(x) =", hex(hx))
print(" x =", hex(x))
print(" r =", hex(r))

if r == x % n:
    print("\n* Valid Signature")
else:
    print("\n* Invalid Signature")
