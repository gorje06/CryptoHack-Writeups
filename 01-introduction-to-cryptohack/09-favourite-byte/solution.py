hex_string = "73626960647f6b206821204f21254f7d694f762466206562212127234f726927756d"

# Decode the hex string into bytes
byte_data = bytes.fromhex(hex_string)

# Brute-force all possible single-byte keys (0 through 255)
for key in range(256):
    # XOR each byte in the data with the current key
    decoded_bytes = bytes(b ^ key for b in byte_data)

    # Check if the result looks like our flag
    if b"crypto{" in decoded_bytes:
        print(f"Key found: {hex(key)}")
        print(f"Flag: {decoded_bytes.decode('ascii')}")
        break
