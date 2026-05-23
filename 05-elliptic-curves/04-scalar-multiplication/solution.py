def addPoints(p1, p2, a=497, p=9739):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    if p1 != p2:
        numerator = (p2[1] - p1[1]) % p
        denominator = pow(p2[0] - p1[0], -1, p)
        constant = (numerator * denominator) % p
    else:
        numerator = (3 * pow(p1[0], 2) + a) % p
        denominator = pow(2 * p1[1], -1, p)
        constant = (numerator * denominator) % p
    x3 = (pow(constant, 2) - p1[0] - p2[0]) % p
    y3 = (constant * (p1[0] - x3) - p1[1]) % p
    return [x3, y3]

def multiply_scalar(x1, y1, n, p):
    Q = [x1, y1]
    R = None
    while n > 0:
        if n % 2 == 1:
            R = addPoints(Q, R)
        Q = addPoints(Q, Q)
        n = n // 2
    return R

n = 7863
a = 497
b = 1768
p = 9739
x1 = 2339
y1 = 2213

answer = multiply_scalar(x1, y1, n, p)
print(f"crypto{{{answer[0]},{answer[1]}}}")
