hex_string = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
ciphertext = bytes.fromhex(hex_string)

# The repeating key we discovered
key = b"myXORkey"

# Decrypt by XORing each byte of the ciphertext with the corresponding byte of the repeating key
flag_bytes = bytes(c ^ key[i % len(key)] for i, c in enumerate(ciphertext))

# Decode to get the readable flag
flag = flag_bytes.decode("ascii")
print(flag)
