def add0() -> int:
    return 7


def add1(a: int) -> int:
    return a + 7


def add2(a: int, b: int) -> int:
    return a + b + 7


def add3(a: int, b: int, c: int) -> int:
    return a + b + c + 7


def add4(a: int, b: int, c: int, d: int) -> int:
    return a + b + c + d + 7


def add5(a: int, b: int, c: int, d: int, e: int) -> int:
    return a + b + c + d + e + 7


def add6(a: int, b: int, c: int, d: int, e: int, f: int) -> int:
    return a + b + c + d + e + f + 7


a = 2
b = 3
c = 5
d = 7
e = 11
f = 13

print(add0())
print(add1(a))
print(add2(a, b))
print(add3(a, b, c))
print(add4(a, b, c, d))
print(add5(a, b, c, d, e))
print(add6(a, b, c, d, e, f))
