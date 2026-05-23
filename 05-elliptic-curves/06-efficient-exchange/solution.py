from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

p = 9739
a = 497
b = 1768

def mod_inv(x, p):
    return pow(x, -1, p)

def elliptic_add(P, Q):
    if P == "O":
        return Q
    if Q == "O":
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
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

# Alice's compressed public key
alice_x = 4726
parity = 0  # even y

# Recover y from x using curve equation
y_sq = (alice_x**3 + a * alice_x + b) % p
alice_y = pow(y_sq, (p + 1) // 4, p)
if alice_y % 2 != parity:
    alice_y = p - alice_y

Q_A = (alice_x, alice_y)

iv = "cd9da9f1c60925922377ea952afc212c"
ciphertext = "febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8"

# Try possible values of Bob's private key
for i in range(10000):
    try:
        S = scalar_mult(i, Q_A)
        if S != "O":
            result = decrypt_flag(S[0], iv, ciphertext)
            print(result)
            print(i)
            break
    except Exception:
        pass
