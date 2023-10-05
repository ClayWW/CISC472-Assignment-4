
#LSFR that updates the current state of the register, takes in the register L
#Creates feedback bit by XORing the 24th, 23rd, 22nd, and 17th bit and then appends the bit onto the state L
def lsfr(L):
    bit24 = (L >> 23) & 1 #24th bit
    bit23 = (L >> 22) & 1 #23rd bit
    bit22 = (L >> 21) & 1 #22nd bit
    bit17 = (L >> 16) & 1 #17th bit

    feedback_bit = bit24 ^ bit23 ^ bit22 ^ bit17 #XOR the bits we just collected to create the feedback bit

    L<<=1 #shift the entire register to the left by 1
    L|=feedback_bit #append the feedback bit to the shifted register
    L &= 0xFFFFFF #ensure that the register is still 24 bits

    return L #return the newly updated register

#NSFR that updates the current state of the register, takes in the register N and an extra bit
#Uses a combination of XORs, ANDs, and the extra bit in order to create the feedback bit and then appends it to the register
def nsfr(N, extra_bit):
    N1 = N & 1 #1st bit
    N2 = (N >> 1) & 1 #2nd bit
    N3 = (N >> 2) & 1 #3rd bit
    N5 = (N >> 4) & 1 #5th bit
    N6 = (N >> 5) & 1 #6th bit
    N10 = (N >> 9) & 1 #10th bit
    N12 = (N >> 11) & 1 #12th bit
    N15 = (N >> 14) & 1 #15th bit
    N18 = (N >> 17) & 1 #18th bit
    N20 = (N >> 19) & 1 #20th bit
    N22 = (N >> 21) & 1 #22nd bit
    N24 = (N >> 23) & 1 #24th bit

    #create the new feedback bit using a combination of XORs and ANDs
    new_N = (extra_bit ^ N1 ^ N2 ^ N5 ^ N15 ^ N20 ^ (N3 & N6) ^ (N10 & N12) ^ (N18 & N22 & N24)) & 1

    N <<= 1 #shift the entire register to the left by 1
    N |= new_N #append the new feedback bit to the register
    N &= 0xFFFFFF #ensure that the register is still 24 bits

    return N #return the newly updated register

#Filter function that takes in a list of 10 bits that then uses XORs and ANDs to create a result bit that is returned
def filter(bitlist):
    z, y, x8, x7, x6, x5, x4, x3, x2, x1 = bitlist #break down the bit list into individual variables
    result_bit = z ^ y ^ (x1 & x2) ^ (x3 & x4) ^ (x5 & x6) ^ (x7 & x8) #calculate the result bit using XORs and ANDs
    return result_bit & 1 #make sure the result bit is just one bit and return it

#iteration of baby grain incorporating the above functions
#Takes in two registers, L and N
def babyGrain(L, N):
    extra_bit = (L >> 23) & 1 #take the MSB from L that will be used as input for the nsfr function
    L = lsfr(L) #update L through the LSFR
    N = nsfr(N, extra_bit) #update N through the NSFR using the extra bit taken from L

    z = (L >> 0) & 1 #1st bit of L
    y = (N >> 1) & 1 #2nd bit of N
    x8 = (N >> 4) & 1 #5th bit of N
    x7 = (L >> 1) & 1 #2nd bit of L
    x6 = (L >> 5) & 1 #6th bit of L
    x5 = (L >> 11) & 1 #12th bit of L
    x4 = (N >> 14) & 1 #15th bit of N
    x3 = (L >> 17) & 1 #18th bit of L
    x2 = (L >> 19) & 1 #20th bit of L
    x1 = (L >> 23) & 1 #24th bit of L

    bitlist = [z, y, x8, x7, x6, x5, x4, x3, x2, x1] #create the bitlist using the bits we just gathered

    output = filter(bitlist) #use the filter function to find the output bit of this iteration

    return output #return the output bit
