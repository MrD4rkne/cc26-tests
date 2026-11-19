# the test calls input_int every iteration: its temporary stays in the test
count = 0
while input_int() - 1 > 0:
    count = count + 1
print(count)
