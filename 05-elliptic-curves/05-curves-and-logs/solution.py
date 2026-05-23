import hashlib

p = 9739
a = 497

def mod_inv(x, p):
    return pow(x, -1, p)

def elliptic_add(P, Q):
    if P == "O":
        return Q
    if Q == "O":
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == -y2 % p:
        return "O"
    if P == Q:
        lam = (3 * x1**2 + a) * mod_inv(2 * y1, p) % p
    else:
        lam = (y2 - y1) * mod_inv(x2 - x1, p) % p
    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(n, P):
    Q = "O"
    R = P
    while n:
        if n % 2 == 1:
            Q = elliptic_add(Q, R)
        R = elliptic_add(R, R)
        n //= 2
    return Q

G = (1804, 5368)
Q_A = (815, 3190)
n_B = 1829

S = scalar_mult(n_B, Q_A)
key = hashlib.sha1(str(S[0]).encode()).hexdigest()
print("crypto{" + key + "}")
