A = 486662
B = 1
p = 2**255 - 19

def montgomery_add(P, Q):
    (x1, y1), (x2, y2) = P, Q
    a = (y2 - y1) * pow(x2 - x1, -1, p)
    x3 = (B * pow(a, 2, p) - A - x1 - x2) % p
    y3 = (a * (x1 - x3) - y1) % p
    return x3, y3

def montgomery_dbl(P):
    (x1, y1) = P
    a = ((3 * pow(x1, 2, p) + 2 * A * x1 + 1) * pow(2 * B * y1, -1, p)) % p
    x3 = (B * pow(a, 2, p) - A - 2 * x1) % p
    y3 = (a * (x1 - x3) - y1) % p
    return x3, y3

def montgomery(k, P):
    k_bits = f'0{k:b}'  # Append a 0
    R0, R1 = P, montgomery_dbl(P)
    for i in range(2, len(k_bits)):
        if k_bits[i] == '0':
            R0, R1 = montgomery_dbl(R0), montgomery_add(R0, R1)
        else:
            R0, R1 = montgomery_add(R0, R1), montgomery_dbl(R1)
    return R0

y_sq = 9**3 + 486662 * (9**2) + 9
G = (9, 14781619447589544791020593568400998688726460613461647528896488183775558623740 1)

s = montgomery(0x1337c0decafe, G)
print('crypto{' + f'{s[0]}' + '}')
