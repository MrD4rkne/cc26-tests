# a, b, c are live across the print call inside the loop: callee-saved or stack
a = input_int()
b = input_int()
c = a + b
i = 0
while i < 3:
    print(a + i)
    i = i + 1
print(a + b + c)
