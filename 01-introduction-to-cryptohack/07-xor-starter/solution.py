original_string = "label"
xor_key = 13

# List comprehension to XOR each character and join them back into a string
new_string = "".join(chr(ord(char) ^ xor_key) for char in original_string)

# Format as the required flag
flag = f"crypto{{{new_string}}}"
print(flag)
