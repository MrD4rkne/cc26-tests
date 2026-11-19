# a non-bool atom as a test is Python truthiness: compared against False (0),
# so 3 and -7 are true, not just 1 (x must be even, or the while never ends)
x = input_int()
if x:
    print(1)
else:
    print(0)
if 5:
    print(2)
y = x - 3
print(10 if y else 20)
print(30 if not y else 40)
while x:
    print(x)
    x = x - 2
print(50 if x else 60)
z = x - 7
if z:
    print(z)
