from Crypto.Util.number import long_to_bytes

ct = 243251053617903760309941844835411292373350655973075480264001352919865180151222189820473358411037759381328642957324889519192337152355302808400638052620580409813222660643570085177957

# Binary search cube root of ct
lo, hi = 0, ct
while lo < hi:
    md = lo + hi >> 1
    if md * md * md < ct:
        lo = md + 1
    else:
        hi = md

print(long_to_bytes(lo).decode())
