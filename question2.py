def lsfr(L):
    bit24 = (L >> 23) & 1
    bit23 = (L >> 22) & 1
    bit22 = (L >> 21) & 1
    bit17 = (L >> 16) & 1

    feedback_bit = bit24 ^ bit23 ^ bit22 ^ bit17

    L>>=1

    L|=(feedback_bit << 23)

    return L