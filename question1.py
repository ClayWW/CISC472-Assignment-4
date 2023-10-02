from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

#xor operation that takes in two strings of bytes
def xor(a, b):
    return bytes(x ^ y for x,y in zip(a,b))

#initialize AES cipher using a 128 bit key and 128 bit nonce
def Init(key, nonce):
    ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder= "big"))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher, nonce

#updates the cipher (which is being used as the keystream in this situation)
#takes in the previous state of the cipher and updates it by incrementing the nonce
#for each block of plaintext. Also returns the updated nonce so that there are no
#repeated keystreams
def Update(previous):
    zero_key = b'\00'*16
    #updated_nonce = (int.from_bytes(previous, byteorder="big")+1).to_bytes(16, byteorder="big")
    ctr = Counter.new(128, initial_value=int.from_bytes(previous, byteorder="big"))
    cipher = AES.new(zero_key, AES.MODE_CTR,  counter=ctr)
    return cipher

#encrypts a plaintext block using a stateful cipher
#takes in the plaintext, a 128 bit key, and a 128 bit nonce
#breaks the plaintext into blocks and then uniquely encodes each block
#while updating the nonce used for each block so that two blocks are not
#encrypted using the same keystream
def stateful_encrypt(plaintext, key, nonce):
    cipher, nonce = Init(key, nonce)
    ciphertext_blocks = []

    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        keystream = cipher.encrypt(bytes([0]*len(block)))
        print(keystream)
        ciphertext_blocks.append(xor(block, keystream))
        cipher = Update(keystream)

    return b''.join(ciphertext_blocks)

question1text = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."
textforless = "match this short length"
question1bytes = question1text.encode('iso-8859-1')
textforless_bytes = textforless.encode('iso-8859-1')
key = bytes.fromhex("0205f285961decd343ef9f9f9f9fcebc")
nonce = bytes.fromhex("0c69d61d0f768968c956238af12aeba1")

ciphertext = stateful_encrypt(question1bytes, key, nonce)
ciphertext_hex = ciphertext.hex()
print(ciphertext_hex)

print("\n")

ciphertext_2 = stateful_encrypt(textforless_bytes, key, nonce)
ciphertext_2hex = ciphertext_2.hex()
print(ciphertext_2hex)

print(f"Length of question1bytes in bytes: {len(question1bytes)}") 
print(f"Length of question1bytes in bits: {len(question1bytes) * 8}")

print(f"Length of ciphertext in bytes: {len(ciphertext)}")  
print(f"Length of ciphertext in bits: {len(ciphertext) * 8}") 

print(f"Length of ciphertext_hex in characters: {len(ciphertext_hex)}")  
print(f"Length of ciphertext_hex in bits: {len(ciphertext_hex) * 4}")  



print(f"Length of question1bytes in bytes: {len(textforless_bytes)}") 
print(f"Length of question1bytes in bits: {len(textforless_bytes) * 8}")

print(f"Length of ciphertext in bytes: {len(ciphertext_2)}")  
print(f"Length of ciphertext in bits: {len(ciphertext_2) * 8}") 

print(f"Length of ciphertext_hex in characters: {len(ciphertext_2hex)}")  
print(f"Length of ciphertext_hex in bits: {len(ciphertext_2hex) * 4}")  
