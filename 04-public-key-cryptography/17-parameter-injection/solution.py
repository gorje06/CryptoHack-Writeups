#!/usr/bin/env python3
import json
import socket
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

class SimpleTelnet:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port))
        self.buffer = b""

    def read_until(self, delimiter):
        while delimiter not in self.buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            self.buffer += chunk
        idx = self.buffer.index(delimiter) + len(delimiter)
        result, self.buffer = self.buffer[:idx], self.buffer[idx:]
        return result

    def write(self, data):
        self.sock.sendall(data)

HOST = "socket.cryptohack.org"
PORT = 13371

tn = SimpleTelnet(HOST, PORT)

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

Alice = readline().decode().split()
for i in range(len(Alice)):
    if Alice[i][0] == "{":
        Alice = json.loads("".join(Alice[i:]))
        break

p = int(Alice["p"], 16)
g = int(Alice["g"], 16)
A = int(Alice["A"], 16)

json_send(Alice)

b = 123
B = pow(g, b, p)

Bob = readline().decode().split()
for i in range(len(Bob)):
    if Bob[i][0] == "{":
        Bob = json.loads("".join(Bob[i:]))
        break

fake_Bob = {"B": hex(B)}
json_send(fake_Bob)

FLAG = readline().decode().split()
for i in range(len(FLAG)):
    if FLAG[i][0] == "{":
        FLAG = json.loads("".join(FLAG[i:]))
        break

shared_secret = pow(A, b, p)
print(decrypt_flag(shared_secret, FLAG["iv"], FLAG["encrypted_flag"]))
