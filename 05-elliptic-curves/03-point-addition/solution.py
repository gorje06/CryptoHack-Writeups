def point_addition(P, Q, a, p):
    if P != Q:
        s = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
    else:
        s = (3 * P[0]**2 + a) * pow(2 * P[1], -1, p) % p
    x = (s**2 - P[0] - Q[0]) % p
    y = (s * (P[0] - x) - P[1]) % p
    return (x, y)

p = 9739
a = 497
b = 1768

# Sanity checks
X = (5274, 2841)
Y = (8669, 740)
assert point_addition(X, Y, a, p) == (1024, 4440)
assert point_addition(X, X, a, p) == (7284, 2107)

P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

S = point_addition(P, point_addition(P, point_addition(Q, R, a, p), a, p), a, p)
print(f"crypto{{{S[0]},{S[1]}}}")
