# - a recursive function (`fib`) and a pair of mutually recursive functions (`even`/`odd`) compile and agree with CPython
def odd(x: int) -> bool:
    return x == 1 or (x >= 1 and not (even(x - 1)))


def even(x: int) -> bool:
    return x == 0 or (x >= 1 and not (odd(x - 1)))


i = 0
while i <= 10:
    if odd(i):
        print(0)
    else:
        print(1)
    if even(i):
        print(1)
    else:
        print(0)
    i = i + 1
