# 06fun1: a call in a loop test. n and i are live across the call in the
# loop header, so they must survive the caller-saved registers it clobbers.
def square(x):
    return x * x


n = input_int()
i = 0
while square(i) < n:
    print(i)
    i = i + 1
print(i)
print(n)
