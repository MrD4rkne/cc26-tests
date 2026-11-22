# 07tuples checkpoint: int, bool and tuple elements, read on both branches of an if.
x = input_int()
t = (x, True, (x + 1, x > 3))
if t[1]:
    print(t[0] + t[2][0])
else:
    print(0)
y = t[2][0] if t[2][1] else -t[0]
print(y)
