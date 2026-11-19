# 06fun1: a call as a statement whose result is thrown away. Its side
# effects (print, input) still happen, and a stays live across it.
def noisy(x):
    print(x)
    return input_int()


a = input_int()
noisy(a)
noisy(a + 1)
print(a)
print(noisy(a + 2))
