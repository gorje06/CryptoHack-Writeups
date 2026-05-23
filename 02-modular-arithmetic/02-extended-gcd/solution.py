def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

p = 26513
q = 32321
g, u, v = extended_gcd(p, q)

# ax + by = gcd(p,q)
print("Coefficients: crypto{%d,%d}" % (u, v))
print("Greatest Common Divisor: %d" % (g))
