t = True
f = False
one = 1
zero = 0

and_tt = t and t
print(1 if and_tt else 0)
and_tf = t and f
print(1 if and_tf else 0)
and_ft = f and t
print(1 if and_ft else 0)
and_ff = f and f
print(1 if and_ff else 0)
