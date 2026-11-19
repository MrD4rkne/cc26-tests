# 06fun1: deep, non-tail recursion with two parameters, one nested
# recursive call as an argument: stresses the stack and its alignment.
def ack(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))


print(ack(0, 0))
print(ack(1, 2))
print(ack(2, 3))
print(ack(input_int(), input_int()))
