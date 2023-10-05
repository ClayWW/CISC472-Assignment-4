from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad

#xor operation that takes in two strings of bytes
def xor(a, b):
    return bytes(x ^ y for x,y in zip(a,b))


def Init(key, nonce):
    cipher = AES.new(key, AES.MODE_ECB) 
    return cipher.encrypt(nonce) 

def Update(previous):
    zero_key = b'\00'*16 
    new_cipher = AES.new(zero_key, AES.MODE_ECB) 
    return new_cipher.encrypt(previous) 

def stateful_sc(plaintext, key, nonce):
    keystream = Init(key, nonce)
    ciphertext_blocks = []
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        encrypted_block = xor(block, keystream[:len(block)])
        ciphertext_blocks.append(encrypted_block)
        keystream = Update(keystream)

    return b''.join(ciphertext_blocks)

def SC(input_block):
    zero_key = b'\00'*16 
    cipher = AES.new(zero_key, AES.MODE_ECB)
    return cipher.encrypt(input_block)


def ctr_sc(plaintext, nonce):
    ciphertext_blocks = []
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        counter = i // 16
        counter_bytes = counter.to_bytes(16, byteorder="big")
        input_block = xor(nonce, pad(counter_bytes, 16))
        keystream = SC(input_block)
        encrypted_block = xor(block, keystream)
        ciphertext_blocks.append(encrypted_block)

    return b''.join(ciphertext_blocks)


question1text = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."
textforless = "match this short length"
question1bytes = question1text.encode('iso-8859-1')
textforless_bytes = textforless.encode('iso-8859-1')
key = bytes.fromhex("0205f285961decd343ef9f9f9f9fcebc")
nonce = bytes.fromhex("0c69d61d0f768968c956238af12aeba1")

ciphertext = stateful_sc(question1bytes, key, nonce)
ciphertext_hex = ciphertext.hex()
print(ciphertext_hex)

print("\n")

question1btext = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."
nonce2 = bytes.fromhex("4a438deb82ced2faf3bd19fb4546c0ba")
question2bytes = question1btext.encode('iso-8859-1')
ciphertext2 = ctr_sc(question2bytes, nonce2)
ciphertext2_hex = ciphertext2.hex()
print(ciphertext2_hex)
