x = input_int()
y = input_int()
if not (x < 0) and (y == 3 or x > 100):
    print(x)
else:
    print(y)
b = x < y
c = not b
print(1 if b else 0)
print(1 if c else 0)
print(1 if c else 2)
