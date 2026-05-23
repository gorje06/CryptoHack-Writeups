n = 28151
for i in range(2, n):
    x = i
    cnt = 1
    while True:
        x = x * i % n
        cnt += 1
        if x == 1:
            break
    if cnt == n - 1:
        print("Result:", i)
        break
