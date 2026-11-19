# not on ints: Python truthiness, so not 2 is 0 (a low-bit flip would give 3)
x = input_int()
y = not x
print(y)
z = 0
w = not z
print(w)
print(1 if not x else 2)
