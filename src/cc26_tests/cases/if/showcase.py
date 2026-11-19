# Everything at once: nested expressions (RCO), left-to-right side effects,
# reassignment (SSA), user names that look like temporaries, big constants.

# side effects nested inside non-commutative operators: order is observable
a = input_int() - (input_int() - -(input_int() * input_int()))
print(a)

# reassignment reading the old version several times
a = a * a - (a - -a)
print(a)
a = -(a + a) - -(-a * 2)
print(a)

# user variables named like temporaries, reassigned inside nested expressions
tmp = input_int()
tmp1 = -(tmp + a) * (tmp - 1)
tmp = (tmp1 - tmp) * -(tmp + (tmp1 - (tmp * 3)))
tmp1 = tmp1 - -(tmp * tmp1) + tmp
print(tmp)
print(tmp1)

# big constants inside nested expressions
big = 3_000_000_000
b = (big + input_int()) * -(3_000_000_000 - (big - input_int()))
print(b)

# a deeply nested expression printed directly, mixing everything above
print(-(((a - tmp) * (tmp1 + 2)) - -(b - (input_int() * -(a - (tmp - 1))))))

# self-assignment and a final chain of versions
a = a
a = a - (a - (a - (a - 1)))
print(a)
