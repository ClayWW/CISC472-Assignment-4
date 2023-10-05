def lsfr(L):
    bit24 = (L >> 23) & 1
    bit23 = (L >> 22) & 1
    bit22 = (L >> 21) & 1
    bit17 = (L >> 16) & 1

    feedback_bit = bit24 ^ bit23 ^ bit22 ^ bit17

    L>>=1

    L|=(feedback_bit << 23)

    return L

def nsfr(N, extra_bit):
    N1 = N & 1
    N2 = (N >> 1) & 1
    N3 = (N >> 2) & 1
    N5 = (N >> 4) & 1
    N6 = (N >> 5) & 1
    N10 = (N >> 9) & 1
    N12 = (N >> 11) & 1
    N15 = (N >> 14) & 1
    N18 = (N >> 17) & 1
    N20 = (N >> 19) & 1
    N22 = (N >> 21) & 1
    N24 = (N >> 23) & 1

    new_N = (extra_bit ^ N1 ^ N2 ^ N5 ^ N15 ^ N20 ^ (N3 & N6) ^ (N10 & N12) ^ (N18 & N22 & N24)) & 1

    N >>= 1

    N |= (new_N << 23)

    return N

def filter(z, y, x8, x7, x6, x5, x4, x3, x2, x1):
    result_bit = z ^ y ^ (x1 & x2) ^ (x3 & x4) ^ (x5 & x6) ^ (x7 & x8)
    return result_bit & 1

def babyGrain(L, N):
    extra_bit = L >> 23
    L = lsfr(L)
    N = nsfr(N, extra_bit)

    z = (L >> 0) & 1
    y = (N >> 1) & 1
    x8 = (N >> 4) & 1
    x7 = (N >> 3) & 1
    x6 = (L >> 1) & 1
    x5 = (N >> 0) & 1
    x4 = (L >> 5) & 1
    x3 = (L >> 10) & 1
    x2 = (L >> 16) & 1
    x1 = (N >> 23) & 1

    output = filter(z, y, x8. x7, x6, x5, x4, x3, x2, x1)

    return output