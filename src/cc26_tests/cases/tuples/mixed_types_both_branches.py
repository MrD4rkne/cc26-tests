# 07tuples checkpoint: int, bool and tuple elements, read on both branches of an if.
# Two inputs, so the condition t[1] is true once and false once.
i = 0
while i < 2:
    x = input_int()
    t = (x, x > 3, (x + 1, x > 3))
    if t[1]:
        print(t[0] + t[2][0])
    else:
        print(t[2][0] - t[0])
    y = t[2][0] if t[2][1] else -t[0]
    print(y)
    i = i + 1
