# 07tuples checkpoint: a tuple live across a recursive call - root frames have to
# nest. Each level's t is a root; a frame not popped would shift all the others.
def f(n: int) -> int:
    t = (n,)
    if n == 0:
        return 0
    r = f(n - 1)
    return r + t[0]


print(f(input_int()))
