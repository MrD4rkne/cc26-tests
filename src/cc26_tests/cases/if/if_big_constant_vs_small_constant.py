# cmpq $5000000000, $5 needs both constants in registers; one scratch is not enough.
if 5 < 5000000000:
    print(1)
else:
    print(0)
if 5000000000 < 5:
    print(1)
else:
    print(0)
a = 5 >= 5000000000
print(a)
b = 5000000000 == 5000000000
print(b)
