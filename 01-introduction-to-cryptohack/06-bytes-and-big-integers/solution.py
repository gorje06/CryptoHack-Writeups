from Crypto.Util.number import long_to_bytes

big_int = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

# Convert the long integer directly to bytes
byte_data = long_to_bytes(big_int)

# Decode the bytes into a readable ASCII string
flag = byte_data.decode("ascii")
print(flag)
