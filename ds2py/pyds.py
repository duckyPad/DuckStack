def print_result(value):
    myloc = 20
    lo2 = 3
    value = value + 100
    STRINGLN('Value is: $value, loc:$myloc, global:$sum')
def is_even(n, b, c):
    mylocal = n%2 + n +b + c
    test = mylocal /2
    if mylocal == 0:
        return 1
    return test
def nothing():
    return 
i = 1
sum = 0
eq = 9
while i <= 6:
    if is_even(i, i, i):
        sum = sum + i
    i = i + 1
print_result(sum)
