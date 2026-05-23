def gcd(a, b):          # maybe will be useful later
    if a < b:           # check and invert a, b if a<b
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a

print(gcd(66528, 52920))
