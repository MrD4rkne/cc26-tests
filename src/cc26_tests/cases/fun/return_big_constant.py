def add(x):
    return x + 5000000000


def sub(x):
    return x - 5000000000


def mul(x):
    return x * 4294967296


def left(x):
    return 5000000000 - x


x = input_int()
print(add(x))
print(sub(x))
print(mul(x))
print(left(x))
