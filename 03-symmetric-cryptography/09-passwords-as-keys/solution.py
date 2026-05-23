from Crypto.Cipher import AES
import requests
import hashlib

def decrypt(word):
    key = hashlib.md5(word).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

wordlist = requests.get("https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627e731268fb2935a731a618aa8e95cf465/words").content.splitlines()
ciphertext = bytes.fromhex(requests.get("https://aes.cryptohack.org/passwords_as_keys/encrypt_flag/").json()["ciphertext"])

for word in wordlist:
    plaintext = decrypt(word)
    try:
        print(plaintext.decode("utf-8"))
    except:
        continue
