import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

# Decode the hex string into bytes
byte_data = bytes.fromhex(hex_string)

# Encode the bytes into Base64
base64_data = base64.b64encode(byte_data)

# Decode the resulting byte string into a readable ASCII string
flag = base64_data.decode("ascii")
print(flag)
