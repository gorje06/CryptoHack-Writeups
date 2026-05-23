from collections import namedtuple
from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import unpad
import hashlib
import math

Point = namedtuple("Point", "x y")
O = "Origin"

p = 310717010502520989590157367261876774703
a, b = 2, 3
G = Point(
    179210853392303317793440285562762725654,
    105268671499942631758568591033409611165,
)
B = Point(
    272640099140026426377756188075937988094,
    51062462309521034358726608268084433317,
)

def point_inverse(P):
    if P == O:
        return P
    return Point(P.x, (-P.y) % p)

def point_add(P, Q):
    if P == O:
        return Q
    if Q == O:
        return P
    if Q == point_inverse(P):
        return O
    if P == Q:
        lam = (3 * P.x**2 + a) * inverse(2 * P.y, p) % p
    else:
        lam = (Q.y - P.y) * inverse((Q.x - P.x) % p, p) % p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam * (P.x - Rx) - P.y) % p
    return Point(Rx, Ry)

def scalar_mult(P, n):
    R, Q = O, P
    while n:
        if n & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        n >>= 1
    return R

def bsgs(base, target, order):
    m = int(math.isqrt(order)) + 1
    table = {}
    cur = O
    for j in range(m):
        key = None if cur == O else (cur.x, cur.y)
        table[key] = j
        cur = point_add(cur, base)
    step = scalar_mult(base, m)
    gamma = target
    for i in range(m):
        key = None if gamma == O else (gamma.x, gamma.y)
        if key in table:
            return i * m + table[key]
        gamma = point_add(gamma, point_inverse(step))
    raise ValueError("BSGS failed")

def primes_up_to(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = 0
    return [i for i in range(2, n + 1) if sieve[i]]

def smooth_multiple(bound):
    M = 1
    for q in primes_up_to(bound):
        e = 1
        while q**e <= bound:
            e += 1
        M *= q ** (e - 1)
    return M

def exact_order(P, smooth_bound=10**6):
    N = smooth_multiple(smooth_bound)
    for q in primes_up_to(smooth_bound):
        while N % q == 0 and scalar_mult(P, N // q) == O:
            N //= q
    if scalar_mult(P, N) != O:
        raise RuntimeError("Increase smooth_bound")
    return N

def factor_prime_powers(n):
    factors = []
    for q in primes_up_to(int(n**0.5) + 1):
        if n % q == 0:
            e = 0
            while n % q == 0:
                n //= q
                e += 1
            factors.append(q**e)
    if n > 1:
        factors.append(n)
    return factors

def pohlig_hellman(target, base, order):
    residues, moduli = [], []
    for fac in factor_prime_powers(order):
        cof = order // fac
        g = scalar_mult(base, cof)
        h = scalar_mult(target, cof)
        residues.append(bsgs(g, h, fac))
        moduli.append(fac)
    return crt(residues, moduli)

def crt(residues, moduli):
    x, M = 0, 1
    for m in moduli:
        M *= m
    for r, m in zip(residues, moduli):
        Mi = M // m
        x = (x + r * Mi * pow(Mi, -1, m)) % M
    return x

def decrypt(shared_secret, iv_hex, ct_hex):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    pt = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv_hex)).decrypt(bytes.fromhex(ct_hex))
    try:
        return unpad(pt, 16)
    except ValueError:
        return pt

def solve(pub_x, pub_y, iv, encrypted):
    P = Point(pub_x, pub_y)
    print(f"\nPublic key x = {pub_x}")
    print("Finding generator order...")
    order = exact_order(G, smooth_bound=10**6)
    print(f"|G| = {order} ({len(factor_prime_powers(order))} prime-power factors)")
    n = pohlig_hellman(P, G, order)
    assert scalar_mult(G, n) == P
    secret = scalar_mult(B, n).x
    flag = decrypt(secret, iv, encrypted)
    print(f"FLAG: {flag.decode()}")

if __name__ == "__main__":
    solve(
        280810182131414898730378982766101210916,
        291506490768054478159835604632710368904,
        "07e2628b590095a5e332d397b8a59aa7",
        "8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af",
    )
    solve(
        226489025719260531208585965886202809498,
        194951558282077081965660065239912869555,
        "006ed17cb92a027fb63a3fc07895e7fe",
        "d5722efb399c93dd03c18481994d978509beded3915236ec80f47193281213655e9f5d5ea94222b6d254da325fa2cabb",
    )
