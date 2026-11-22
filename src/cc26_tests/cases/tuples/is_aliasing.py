# 07tuples checkpoint: `is` compares addresses. x is not a constant, so CPython
# does not fold the two equal literals into one object either.
x = 3
t1 = (x, 7)
t2 = t1
t3 = (x, 7)
print(1 if t1 is t2 else 0)
print(1 if t1 is t3 else 0)
print(1 if not (t1 is t3) else 0)
