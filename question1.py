from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256

def xor(a, b):
    return bytes(x ^ y for x,y in zip(a,b))

def Init(key, nonce):
    ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder= "big"))
    return AES.new(key, AES.MODE_CTR, counter=ctr), nonce

def Update(previous):
    zero_key = b'\00'*16
    ctr = Counter.new(128, initial_value=int.from_bytes(previous, byteorder="big"))
    return AES.new(zero_key, AES.MODE_CTR)

def stateful_encrypt(plaintext, key, nonce):
    cipher, nonce = Init(key, nonce)
    ciphertext = xor(plaintext, cipher.encrypt(bytes([0]*len(plaintext))))
    return ciphertext

question1text = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."
key = bytes.fromhex("0205f285961decd343ef9f9f9f9fcebc")
nonce = bytes.fromhex("0c69d61d0f768968c956238af12aeba1")

ciphertext = stateful_encrypt(question1text, key, nonce)
print(ciphertext)