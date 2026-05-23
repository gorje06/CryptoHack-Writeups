from Crypto.Cipher import AES
from textwrap import wrap
import requests
import json
import binascii

url = "https://aes.cryptohack.org/ecbcbcwtf/"

def getPlaintext(url, ciphertext):
    req = requests.get(url + "decrypt/" + ciphertext + "/").content
    return json.loads(req)["plaintext"]

def getFlagCipher():
    req = requests.get(url + "encrypt_flag/").content
    test = json.loads(req)
    ciphertext = wrap(test["ciphertext"], 32)
    iv = ciphertext[0]
    ciphertext = "".join(ciphertext[1:])
    return ciphertext, iv

def toIntList(string):
    return [i for i in binascii.unhexlify(string)]

ciphertext, iv = getFlagCipher()
ct1, ct2 = wrap(ciphertext, 32)[0], wrap(ciphertext, 32)[1]

plaintext = getPlaintext(url, ct1)
ct1_list = toIntList(ct1)
pt1 = toIntList(plaintext)
iv_list = toIntList(iv)

pt = ""
for x, y in zip(pt1, iv_list):
    pt += chr(x ^ y)

pt2 = getPlaintext(url, ct2)
pt2_list = toIntList(pt2)
for x, y in zip(ct1_list, pt2_list):
    pt += chr(x ^ y)

print(pt)
