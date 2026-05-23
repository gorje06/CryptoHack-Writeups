import hashlib
import json
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sympy.ntheory.residue_ntheory import discrete_log

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode("ascii")
    return plaintext.decode("ascii")

class Conn:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port))
        self.buf = b""

    def _fill_until(self, needle):
        while needle not in self.buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            self.buf += chunk

    def sendlineafter(self, prompt, data):
        self._fill_until(prompt)
        idx = self.buf.index(prompt) + len(prompt)
        self.buf = self.buf[idx:]
        self.sock.sendall(data + b"\n")

    def recvuntil(self, needle):
        self._fill_until(needle)
        idx = self.buf.index(needle) + len(needle)
        out, self.buf = self.buf[:idx], self.buf[idx:]
        return out

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

with Conn("socket.cryptohack.org", 13379) as io:
    chosen = "DH64"
    io.sendlineafter(b"Send to Bob: ", json.dumps({"supported": [chosen]}).encode())
    io.sendlineafter(b"Send to Alice: ", json.dumps({"chosen": chosen}).encode())

    io.recvuntil(b"Intercepted from Alice: ")
    alice = json.loads(io.recvuntil(b"}").decode())
    p = int(alice["p"][2:], 16)
    g = int(alice["g"][2:], 16)
    A = int(alice["A"][2:], 16)

    io.recvuntil(b"Intercepted from Bob: ")
    bob = json.loads(io.recvuntil(b"}").decode())
    B = int(bob["B"][2:], 16)

    io.recvuntil(b"Intercepted from Alice: ")
    alice = json.loads(io.recvuntil(b"}").decode())
    iv = alice["iv"]
    ct = alice["encrypted_flag"]

    # Solve discrete log (feasible with 64-bit prime)
    a = discrete_log(p, A, g)
    s = pow(B, a, p)
    print(decrypt_flag(s, iv, ct))
