# 07tuples checkpoint: a tuple built in a function, returned and passed back in.
def mk(a: int, b: int) -> tuple[int, tuple[int, int]]:
    return (a + b, (a, b))


def snd(p: tuple[int, tuple[int, int]]) -> int:
    return p[1][1]


r = mk(input_int(), 10)
print(r[0])
print(snd(r))
print(len(r) + len(r[1]))
