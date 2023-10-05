from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad

#xor operation that takes in two strings of bytes
def xor(a, b):
    return bytes(x ^ y for x,y in zip(a,b))

#initialize AES cipher using a 128 bit key and 128 bit nonce
def Init(key, nonce):
    cipher = AES.new(key, AES.MODE_ECB) #create the cipher and initialize it with the key and the nonce
    return cipher.encrypt(nonce) #return the newly initialized cipher

#updates the cipher (which is being used as the keystream in this situation)
#takes in the previous state of the cipher and updates it by incrementing the nonce
#for each block of plaintext. Also returns the updated nonce so that there are no
#repeated keystreams
def Update(previous):
    zero_key = b'\00'*16 #use a zero key so that the cipher is initialized with the previous keystream (previous state)
    new_cipher = AES.new(zero_key, AES.MODE_ECB) #pass the previous keystream into the cipher to create a new (updated) keystream
    return new_cipher.encrypt(previous) #return the fresh cipher

def stateful_sc(plaintext, key, nonce):
    keystream = Init(key, nonce)
    ciphertext_blocks = []
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        encrypted_block = xor(block, keystream[:len(block)])
        ciphertext_blocks.append(encrypted_block)
        keystream = Update(keystream)

    return b''.join(ciphertext_blocks)

#encrypts a plaintext block using a stateful cipher
#takes in the plaintext, a 128 bit key, and a 128 bit nonce
#breaks the plaintext into blocks and then uniquely encodes each block
#while updating the nonce used for each block so that two blocks are not
#encrypted using the same keystream
'''
def stateful_sc(plaintext, key, nonce):
    keystream = Init(key, nonce) #create the cipher
    ciphertext_blocks = [] #create the array that holds the encrypted blocks
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16] #create the block by taking the next 16 bytes of plaintext
        is_last_block = (i + 16) >= len(plaintext) #check to see if this iteration is handling the final block or not
        if(len(block) < 16): #case for the final block if it is not a full block
            full_keystream = cipher.encrypt(bytes([0]*16)) #create a full keystream that is 128 bits
            keystream = full_keystream[:len(block)] #truncate the keystream to match the size of the block
            encrypted_block = xor(block, keystream) #xor the truncated keystream with the block
            ciphertext_blocks.append(encrypted_block) #add the encrypted block to the array
            #do not need to update the cipher because being in this first if means that we are done after this
        else: #case for either a full block or a final block that is full
            keystream = cipher.encrypt(bytes([0]*16))
            encrypted_block = xor(block, keystream) #xor the keystream with the block
            ciphertext_blocks.append(encrypted_block) #add the encrypted block to the array
            if not is_last_block: #no need to update the keystream if we're on the final block
                cipher = Update(keystream) #pass the keystream into the update function to generate a fresh keystream for the next block

    return b''.join(ciphertext_blocks) #join all the ciphertext blocks together and return
'''
def secure_PRP(key, input_block):
    cipher = AES.new(key, AES.MODE_CBC, iv=0x00)
    return cipher.encrypt(input_block)


def ctr_sc(plaintext, key, nonce):
    ciphertext_blocks = []
    for i in range(0, len(plaintext), 16):

        block = plaintext[i:i+16]
        counter = i // 16
        input_block = nonce + counter
        zero_key = b'\x00'*16
        keystream = secure_PRP(zero_key,input_block)
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

ciphertext_2 = stateful_sc(textforless_bytes, key, nonce)
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


question1btext = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."