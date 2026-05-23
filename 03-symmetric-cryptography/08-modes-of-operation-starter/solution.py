import requests

response = requests.get("http://aes.cryptohack.org/block_cipher_starter/encrypt_flag/")
ciphertext = response.json()['ciphertext']
response = requests.get("http://aes.cryptohack.org/block_cipher_starter/decrypt/" + ciphertext)
print(bytes.fromhex(response.json()['plaintext']).decode('utf-8'))
