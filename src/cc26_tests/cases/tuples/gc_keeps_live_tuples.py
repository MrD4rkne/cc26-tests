# Far more garbage than a heap holds, so the collector runs many times: the
# live tuple and the one inside it must survive every copy intact.
x = input_int()
keep = (x, (x + 1, True))
i = 0
while i < 20000:
    junk = (i, (i, i))
    keep = (keep[0] + junk[1][0] - i + 1, keep[1])
    i = i + 1
print(keep[0])
print(keep[1][0])
print(1 if keep[1][1] else 0)
