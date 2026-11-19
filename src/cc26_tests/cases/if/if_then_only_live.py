# v is live only in the then-branch: it must survive the j<cc>, or w takes its register
a = input_int()
v = a + 1
w = a + 2
if a > 0:
    print(v)
else:
    print(w)
print(a)
