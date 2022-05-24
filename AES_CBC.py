# Advanced Encryption Standard algorithm practice
# Encoded mode Cipher Block Chain(CBC)
from Cryptodome.Cipher import AES
from Cryptodome import Random
import numpy as np

# make symmetric key. symmetric key uses 128, 192, 256 bits
secreteKey128 = b"0123456701234567"
secreteKey192 = b"012345670123456701234567"
secreteKey256 = b"01234567012345670123456701234567"

# use 128-bit key
secretKey = secreteKey128
plainText = "This is Plain text. It will be encrypted using AES with CBC module"
print("\n\n")
print("plainText :")
print(plainText)

# In CBC mode, we need padding because plain text needs to be multiple of 128 bits(16 bypte)
# insert NULL as padding, sender doesn't need to eliminate padding
n = len(plainText)
if (n % 16) != 0:
    n = n + 16 - (n % 16)
    plainText = plainText.ljust(n, "\0")

# initialization vector, iv should be sent to receiver
iv = Random.new().read(AES.block_size)
ivcopy = np.copy(iv)  # copy for receiver

# receiver encodes plainText with secretKey and iv
iv = Random.new().read(AES.block_size)
ivcopy = np.copy(iv)
aes = AES.new(secretKey, AES.MODE_CBC, iv)
cipherText = aes.encrypt(plainText.encode("ascii", "ignore"))
print("\n\n\n")
print("cryptography : ")
print(cipherText.hex())

# reciever can decode cryptography by secretKey, ivcopy
iv = ivcopy.tolist()
aes = AES.new(secretKey, AES.MODE_CBC, iv)
plainText2 = aes.decrypt(cipherText)
plainText2 = plainText2.decode()
print("\n\n\n")
print("decoded : ")
print(plainText2)
