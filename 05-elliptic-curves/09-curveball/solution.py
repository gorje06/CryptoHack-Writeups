#!/usr/bin/env python3
# CVE-2020-0601 (CurveBall) attack
import fastecdsa
from fastecdsa.point import Point
from fastecdsa.curve import P256
import json
from pwn import *

# Bing public key from trusted_certs
Bing_pub = Point(
    0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531,
    0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A,
    curve=P256
)

# Choose our own private key d, compute fake generator G' = d^-1 * Q_Bing
# so that d * G' = Q_Bing — Windows accepts because Q = d*G' is valid
d = 2
d_inv = pow(d, -1, P256.q)
custom_generator = d_inv * Bing_pub

payload = {
    "private_key": d,
    "host": "www.definitely-not-bing.com",
    "curve": "secp256r1",
    "generator": [custom_generator.x, custom_generator.y]
}

r = remote("socket.cryptohack.org", 13382)
r.sendlineafter(b"Welcome to my secure search engine backed by trusted certificate library!\n", json.dumps(payload).encode())
log.success(r.recvline().decode())
