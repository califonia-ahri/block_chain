# use pubKey_create.py's private key and public keys
privKey = "b0291dcb1e6eb07fd2aa174a7ffbed1d1b9c5d9038f9bb35b681adccf5d97fea"
pubKey = (
    "895149364f4e81bdbc9094d0bd8346c6ebe10e00b6da70d067c265e976f9e4ec",
    "b67c8fee46c46c5cb51414023d736d42b6e9cf2c96c2f3aef0722b6a7ac1de9f",
)

# domain parameters defined by secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

# represnet public key by Uncompressed format
uPubKey = "04" + pubKey[0] + pubKey[1]

# represent public key by compressed format
if int(pubKey[1], 16) % 2 == 0:
    cPubKey = "02" + pubKey[0]
else:
    cPubKey = "03" + pubKey[0]

# transform Compressed format to (x, y) format
# p%4 = 3 mod 4
x = int(cPubKey[2:], 16)
a = (pow(x, 3, p) + 7) % p  # y^2
y = pow(a, (p + 1) // 4, p)  # y

prefix = int(cPubKey[:2], 16)
if (prefix == 2 and y & 1) or (prefix == 3 and not y & 1):
    y = (-y) % p

# print Public key
print("\n Public Key : (%s\n            %s" % (pubKey[0], pubKey[1]))

# print as uncompressed format
print("\nUncompressed (size=%d):\n%s" % (len(uPubKey) * 4, uPubKey))

# print as compressed format
print("\nCompressed format (size=%d):\n%s" % (len(cPubKey) * 4, cPubKey))

print("\nCompressed format --> Public key :")
print("\n Public Key : (%s,\n       %s)" % (hex(x)[2:], hex(y)[2:]))
