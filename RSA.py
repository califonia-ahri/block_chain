# Public Key(RSA) Algorithm
import Cryptodome.Cipher.PKCS1_OAEP as oaep
from Cryptodome.PublicKey import RSA

# create pair of Public key and Private key
# Owner own Private key and open Public key
keyPair = RSA.generate(2048)
privKey = keyPair.exportKey()
pubKey = keyPair.publickey()

# check p,q,e,d of keyPari
keyObj = RSA.importKey(privKey)
print("p = ", keyObj.p)
print("q = ", keyObj.q)
print("e = ", keyObj.e)
print("d = ", keyObj.d)

# plainText to encode
plainText = "This is Plain text. It will be encrypted using RSA"
print()
print("원문 : ")
print(plainText)

# encrypt plaintext with public key
encryptor = oaep.new(pubKey)
cipherText = encryptor.encrypt(plainText.encode())
print("\n")
print("암호문 : ")
print(hex(cipherText[0]))

# decode cipher text with private key
key = RSA.importKey(privKey)
decryptor = oaep.new(key)
plainText2 = decryptor.decrypt(cipherText)
plainText = plainText2.decode()
print("\n")
print("해독문 : ")
print(plainText2)
