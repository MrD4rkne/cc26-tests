# more loop-carried variables than registers: some must spill
v0 = input_int()
v1 = v0 + 1
v2 = v1 + 1
v3 = v2 + 1
v4 = v3 + 1
v5 = v4 + 1
v6 = v5 + 1
v7 = v6 + 1
v8 = v7 + 1
v9 = v8 + 1
v10 = v9 + 1
v11 = v10 + 1
v12 = v11 + 1
v13 = v12 + 1
v14 = v13 + 1
i = 0
while i < 2:
    v0 = v1 + v14
    v1 = v2 + v13
    v2 = v3 + v12
    v3 = v4 + v11
    v4 = v5 + v10
    v5 = v6 + v9
    v6 = v7 + v8
    v7 = v0 - v1
    i = i + 1
print(v0 + v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9 + v10 + v11 + v12 + v13 + v14)
