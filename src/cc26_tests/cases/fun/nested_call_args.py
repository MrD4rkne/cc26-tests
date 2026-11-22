# 06fun1: calls nested as arguments. The inner calls run left to right
# (each reads input), and a stays live across all of them.
def f(x: int) -> int:
    return x + input_int()


def g(x: int, y: int) -> int:
    return 2 * x - y


def add(x: int, y: int) -> int:
    return x + y


a = input_int()
print(add(f(a), g(f(a), a)))
print(a)
