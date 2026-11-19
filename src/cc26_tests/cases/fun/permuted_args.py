# 06fun1: arguments passed in permuted order. Each parameter arrives in one
# argument register and must leave in another (%rdi <-> %rsi, ...), so the
# argument moves must not overwrite a value that is still to be passed.
def weigh(a, b, c, d, e, f):
    return a + 10 * b + 100 * c + 1000 * d + 10000 * e + 100000 * f


def swap(a, b, c, d, e, f):
    return weigh(b, a, d, c, f, e)


def rotate(a, b, c, d, e, f):
    return weigh(f, a, b, c, d, e)


print(swap(1, 2, 3, 4, 5, 6))
print(rotate(1, 2, 3, 4, 5, 6))
print(swap(input_int(), 0, 0, 0, 0, input_int()))
