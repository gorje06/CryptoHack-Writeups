"""MOV attack on non-supersingular elliptic curve: Pohlig-Hellman + CADO-NFS + CRT."""
from collections import namedtuple
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import inverse

p = 1331169830894825846283645180581
a_curve = (-35) % p
b_curve = 98
O = None
Point = namedtuple("Point", "x y")

Gx, Gy = 479691812266187139164535778017, 568535594075310466177352868412
Ax, Ay = 1110072782478160369250829345256, 800079550745409318906383650948
Bx, By = 1290982289093010194550717223760, 762857612860564354370535420319

q1 = 2 * 7 * 271 * 23687
q2 = 1153763334005213

# Values computed with CADO-NFS for the large prime factor
alpha = 757655375998782
beta = 849398457004196

def on_curve(P):
    if P is O:
        return True
    return (P.y * P.y - (P.x**3 + a_curve * P.x + b_curve)) % p == 0

def neg(P):
    if P is O:
        return O
    return Point(P.x, (-P.y) % p)

def add(P, Q):
    if P is O:
        return Q
    if Q is O:
        return P
    if P.x == Q.x and (P.y + Q.y) % p == 0:
        return O
    if P == Q:
        lam = (3 * P.x * P.x + a_curve) * inverse(2 * P.y, p) % p
    else:
        lam = (Q.y - P.y) * inverse(Q.x - P.x, p) % p
    rx = (lam * lam - P.x - Q.x) % p
    ry = (lam * (P.x - rx) - P.y) % p
    return Point(rx, ry)

def mul(P, n):
    n = int(n)
    R, Q = O, P
    while n:
        if n & 1:
            R = add(R, Q)
        Q = add(Q, Q)
        n >>= 1
    return R

def bsgs_prime(h, g, fac):
    table = {}
    cur = O
    m = int(fac**0.5) + 1
    for j in range(m):
        table[cur] = j
        cur = add(cur, g)
    step = mul(g, m)
    cur = h
    for i in range(m + 1):
        if cur in table:
            return i * m + table[cur]
        cur = add(cur, neg(step))
    raise ValueError("BSGS failed")

def pohlig_hellman(P, G, order, factors):
    logs, mods = [], []
    for fac in factors:
        cof = order // fac
        g = mul(G, cof)
        h = mul(P, cof)
        logs.append(bsgs_prime(h, g, fac) % fac)
        mods.append(fac)
    return crt(logs, mods)

def crt(residues, moduli):
    x = 0
    M = 1
    for a, m in zip(residues, moduli):
        t = ((a - x) * inverse(M, m)) % m
        x += M * t
        M *= m
    return x % M

def main():
    G = Point(Gx, Gy)
    A = Point(Ax, Ay)
    B = Point(Bx, By)

    # Project to subgroup of order q1
    G1 = mul(G, q2)
    A1 = mul(A, q2)

    # Solve smooth part with Pohlig-Hellman
    alice_secret_1 = pohlig_hellman(A1, G1, q1, factors=[2, 7, 271, 23687])

    # Solve large prime part using precomputed CADO-NFS values
    alice_secret_2 = (beta * inverse(alpha, q2)) % q2

    # Combine with CRT
    alice_secret = crt([alice_secret_1, alice_secret_2], [q1, q2])
    assert mul(G, alice_secret) == A, "Secret verification failed"

    shared_x = mul(B, alice_secret).x
    print("alice_secret =", alice_secret)
    print("shared_x =", shared_x)

    iv_hex = "eac58c26203c04f68d63dc2c58d79aca"
    ct_hex = "bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d"

    key = hashlib.sha1(str(shared_x).encode("ascii")).digest()[:16]
    pt = unpad(AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex)).decrypt(bytes.fromhex(ct_hex)), 16)
    print("flag:", pt.decode())

if __name__ == "__main__":
    main()
