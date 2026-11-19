# 06fun1: a return inside an if inside a loop. Nothing runs after it, and
# the loop's variables must not be live at the jump to the conclusion.
def find(target):
    i = 0
    while i < 100:
        if i * i == target:
            return i
        i = i + 1
    return -1


print(find(input_int()))
print(find(input_int()))
print(find(0))
