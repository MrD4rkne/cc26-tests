# A tuple held across calls to a function that allocates (and so may collect):
# it must be a root, not a register or a plain stack slot.
def make(n: int) -> tuple[int, tuple[int]]:
    return (n, (n * 2,))


held = make(input_int())
i = 0
total = 0
while i < 20000:
    t = make(i)
    total = total + t[1][0] - t[0]
    i = i + 1
print(held[0] + held[1][0])
print(total)
