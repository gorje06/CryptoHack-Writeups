import requests
import json
from Crypto.Util.strxor import strxor

def get_cookie():
    url = 'https://aes.cryptohack.org/flipping_cookie/get_cookie/'
    response = requests.get(url)
    return response.json()

def get_flag(cookie, iv):
    url = 'https://aes.cryptohack.org/flipping_cookie/check_admin/'
    response = requests.get(url + '/' + cookie + '/' + iv)
    return response.json()

data = get_cookie()['cookie']
iv = bytes.fromhex(data[:32])
text = b'admin=False;expi'
forge_text = b'admin=True;expir'
xor_result = strxor(iv, text)
forge_iv = strxor(xor_result, forge_text).hex()
print(get_flag(data[32:], forge_iv)["flag"])
