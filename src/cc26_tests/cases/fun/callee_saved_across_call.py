# 06fun1 final check: callee-saved registers are not clobbered.
# a is live across the call to f, and x is live across print inside f:
# under callee-saved-only registers both want %rbx, so f must save it.
def f(x):
    print(x)
    print(x)
    return x


a = input_int()
b = f(5)
print(a)
print(b)
