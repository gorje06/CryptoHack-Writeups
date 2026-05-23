#!/usr/bin/env python3

A1 = 11
M1 = 6
A2 = 8146798528947
M2 = 17

def main() -> None:
    # We can simply calculate the modulo of the multiplication of the two numbers
    x = A1 % M1
    y = A2 % M2
    result = min(x, y)
    print(result)

if __name__ == "__main__":
    main()
