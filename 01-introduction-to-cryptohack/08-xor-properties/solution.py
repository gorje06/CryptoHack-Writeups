# The given hex strings from the challenge
key1_hex = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
key2_xor_key3_hex = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
flag_xor_keys_hex = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

# Decode from hex to bytes
key1 = bytes.fromhex(key1_hex)
key2_xor_key3 = bytes.fromhex(key2_xor_key3_hex)
flag_xor_keys = bytes.fromhex(flag_xor_keys_hex)

# XOR the three byte strings together byte-by-byte
flag_bytes = bytes(a ^ b ^ c for a, b, c in zip(flag_xor_keys, key1, key2_xor_key3))

# Decode the resulting bytes back into a readable ASCII string
flag = flag_bytes.decode("ascii")
print(flag)
