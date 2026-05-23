#!/usr/bin/env python3
import hashlib
from Crypto.Util.number import bytes_to_long, inverse
from ecdsa.ecdsa import Public_key, Private_key, generator_192
import json
import socket

def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()

g = generator_192

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("socket.cryptohack.org", 13381))

    print(f"<: {sock.recv(64)}")

    query = b'{"option":"sign_time"}'
    print(f">: {query}")
    sock.sendall(query)

    res = json.loads(sock.recv(256))
    print(f"<: {res}")

    r = int(res["r"], 16)
    s = int(res["s"], 16)
    msg = res["msg"]

    # Server bug: n is shadowed by minutes value, so k ∈ [1, minutes]
    k_max = int(msg.split(":")[-1], 10)

    for k in range(1, k_max):
        if (k * g).x() == r:
            break
    else:
        exit("error: couldnt determine k")

    print(f" : k = {k}")

    hsh = sha1(msg.encode())
    m = bytes_to_long(hsh)

    # Recover private key: secret = (s*k - m) / r mod n
    secret = ((s * k) - m) * inverse(r, g.order()) % g.order()
    print(f" : secret = {secret}")

    pubkey = Public_key(g, g * secret)
    privkey = Private_key(pubkey, secret)

    msg_unlock = "unlock"
    sig = privkey.sign(bytes_to_long(sha1(msg_unlock.encode())), k)

    query = json.dumps({
        "option": "verify",
        "msg": msg_unlock,
        "r": hex(sig.r),
        "s": hex(sig.s)
    })
    print(f">: {query}")
    sock.sendall(query.encode())

    res = json.loads(sock.recv(256))
    print(f"<: {res}")
