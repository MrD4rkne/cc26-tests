# 06fun1: a parameter and a local, both live across a call, with input in
# between. Both need callee-saved registers or stack slots.
def h(x):
    print(x)
    return x * 2


def g(p):
    q = input_int()
    r = h(p + q)
    return p * 100 + q * 10 + r


print(g(input_int()))
