# 07tuples checkpoint: len of tuples of tuples, the empty one, and in a loop.
x = input_int()
t = ((x,), (x, x), (x, x, x), ())
print(len(t))
print(len(t[2]) * 100 + len(t[3]))
i = 0
s = 0
while i < 50:
    u = (i, (i, i))
    s = s + u[1][1]
    i = i + 1
print(s)
