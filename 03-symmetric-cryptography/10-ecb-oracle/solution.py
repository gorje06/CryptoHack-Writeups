import requests
import json
from textwrap import wrap

url = "https://aes.cryptohack.org/ecb_oracle/encrypt/"

def getCipher(url, payload):
    req = requests.get(url + payload + "/").content
    test = json.loads(req)
    ciphertext = wrap(test["ciphertext"], 32)
    return ciphertext[1]

flag = ""
payload = 31 * "41"
p = payload

while True:
    for i in range(33, 126):
        target = getCipher(url, payload)
        cp_p = p + format(i, "02x")
        tgt = getCipher(url, cp_p)
        if tgt == target:
            flag += chr(int(format(i, "02x"), 16))
            payload = payload[:-2]
            p = p[2:]
            p += format(i, "02x")
            print(f"[+] Flag: {flag}")
            if flag[-1] == "}":
                print(f"Flag: {flag}")
                exit()
            break
