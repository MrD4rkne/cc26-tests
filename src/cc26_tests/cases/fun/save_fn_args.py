# - a function whose parameter is still needed after a call inside its body


def f(a, b, c):
    print(a)
    print(b)
    print(c)


f(1, 2, 3)
