# the right operand reads input: evaluating it would shift what the last print reads
x = input_int()
if x > 0 or input_int() > 0:
    print(1)
else:
    print(0)
y = x < 0 and input_int() > 0
print(1 if y else 0)
print(input_int())
