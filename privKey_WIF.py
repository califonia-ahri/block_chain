import hashlib
import binascii

# transform private key to WIF format
privKey = "0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D"

# Base58 Encoding
s = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# add version prefix. x80 ~ priv key WIF
# when using public key as compressed form add '01' additionally
prefixPayload = "80" + privKey

# get Checksum. do double-SHA256 to version+payload
# add front 4 byte behind of prefixPayload
versionPayload = binascii.unhexlify(prefixPayload)
h = hashlib.sha256(hashlib.sha256(versionPayload).digest()).digest()
h = "".join("{:02x}".format(y) for y in h)
versionPayloadChecksum = prefixPayload + h[0:8]

# perform Base58Check
eKey = int(versionPayloadChecksum, 16)
base58 = ""
while 1:
    m, r = divmod(eKey, 58)
    base58 += s[r]
    if m == 0:
        break
    eKey = m

wif = base58[::-1]
print("\n개인키 (Hex): ", privKey.lower())
print("개인키 (WIF): ", wif)
