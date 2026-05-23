p = 65537
a = 273246787654
power = 65536

# Fermat's Little Theorem: a^(p-1) ≡ 1 (mod p)
print(pow(a, power, p))
