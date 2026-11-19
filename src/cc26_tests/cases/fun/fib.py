# - a recursive function (`fib`) and a pair of mutually recursive functions (`even`/`odd`) compile and agree with CPython
def fib(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


print(fib(0))
print(fib(1))
print(fib(2))
print(fib(3))
print(fib(20))
