x = 1
while x > 5:
    print(0)
while x < 4 and not (x == 2):
    print(x)
    x = x + 1 if x != 3 else 99
print(x)
