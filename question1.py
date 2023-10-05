from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad

#xor operation that takes in two strings of bytes
def xor(a, b):
    return bytes(x ^ y for x,y in zip(a,b))

#1a

#Initializes our first keystream using a 128 bit key and 128 bit nonce
#initialies cipher with the key and AES ECB mode and returns the encryption of our nonce which is our keystream
def Init(key, nonce):
    cipher = AES.new(key, AES.MODE_ECB) #initalize cipher with key
    return cipher.encrypt(nonce) #return keystream (encryption of nonce using cipher)

#Updates our keystream by taking in the previous state (128 bit keystream) and generating a new one through permutation
def Update(previous):
    zero_key = b'\00'*16 #use a 0 key because we are more concerned with the permutation
    new_cipher = AES.new(zero_key, AES.MODE_ECB) #initalize cipher with 0 key
    return new_cipher.encrypt(previous)  #return the next keystream which is the encryption of our previous keystream using a zero key

#Stateful cipher that takes in a plaintext of arbitrary size, a 128 bit key, and a 128 bit nonce
#Breaks the plaintext into 16 byte blocks and xors each them with a unique keystream before joining the blocks back together and returning
def stateful_sc(plaintext, key, nonce):
    keystream = Init(key, nonce) #initialize the first keystream using the actual key
    ciphertext_blocks = [] #array to hold ciphertext blocks post XORing
    for i in range(0, len(plaintext), 16): #loop for the size of the plaintext in 16 byte jumps
        block = plaintext[i:i+16] #the block is created by taking the next 16 bytes of plaintext or whatever plaintext is left
        encrypted_block = xor(block, keystream[:len(block)]) #xor the block with the keystream but truncate the keystream so that it matches the length of the block
        ciphertext_blocks.append(encrypted_block) #add the XORed block to the array
        keystream = Update(keystream) #update the keystream for the next block using the previous keystream

    return b''.join(ciphertext_blocks) #join all the XORed blocks together and return


#1b

#secure_PRP takes in only the 128 bit input block (the xored nonce and counter) and returns a unique keystream
def SC(input_block):
    zero_key = b'\00'*16  #zero key because we only care about permutation
    cipher = AES.new(zero_key, AES.MODE_ECB) #initalize cipher with zero key
    return cipher.encrypt(input_block) #encrypt our input block using the zero keyed cipher to generate a unique keystream



#counter based stream cipher that takes in a plaintext of arbitrary size and a nonce
#breaks the plaintext into 16 byte blocks and creates a unique keystream using the nonce and a counter that increments for each block
#xors the block with the unique keystream and then adds all the XORed blocks together before returning
def ctr_sc(plaintext, nonce):
    ciphertext_blocks = [] #array to hold XORed blocks
    for i in range(0, len(plaintext), 16): #loop through the plaintext in jumps of 16 bytes
        block = plaintext[i:i+16] #create the block by taking the next 16 bytes of plaintext or however much plaintext is left
        counter = i // 16 #establish counter value for whatever block we are on, each block increments counter
        counter_bytes = counter.to_bytes(16, byteorder="big") #turn the counter into bytes for the XORing with the nonce
        input_block = xor(nonce, pad(counter_bytes, 16)) #XOR the nonce and the counter(padded) to get a unique 128 bit value to pass into the SC() to generate a unique keystream
        keystream = SC(input_block) #generate keystream with new input block
        encrypted_block = xor(block, keystream) #xor the block with the keystream
        ciphertext_blocks.append(encrypted_block) #add the xored block to the array

    return b''.join(ciphertext_blocks) #join all of the XORed blocks together and return


#1a
question1text = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."
question1bytes = question1text.encode('iso-8859-1')
key = bytes.fromhex("0205f285961decd343ef9f9f9f9fcebc")
nonce = bytes.fromhex("0c69d61d0f768968c956238af12aeba1")

ciphertext = stateful_sc(question1bytes, key, nonce)
ciphertext_hex = ciphertext.hex()
print(ciphertext_hex)

print("\n")

#1b
question1btext = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad."
nonce2 = bytes.fromhex("4a438deb82ced2faf3bd19fb4546c0ba")
question2bytes = question1btext.encode('iso-8859-1')

ciphertext2 = ctr_sc(question2bytes, nonce2)
ciphertext2_hex = ciphertext2.hex()
print(ciphertext2_hex)
