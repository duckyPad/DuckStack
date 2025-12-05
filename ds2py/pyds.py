def print_result(value):
    STRINGLN('Value is: $value')
def is_even(n):
    mylocal = n%2
    if mylocal == 0:
        return 1
    return 0
i = 1
sum = 0
while i <= 6:
    if is_even(i):
        sum = sum + i
    i = i + 1
print_result(sum)
