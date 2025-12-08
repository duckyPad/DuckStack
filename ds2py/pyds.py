g = 10
unused_global = 123
def no_args():
    local = 1
    unused_local = 999
    return 
    local = 42
def add(a, b, unused_arg):
    tmp = a + b
    if tmp == 0:
        return 0
    return tmp
def factorial(n):
    acc = 1
    while n > 1:
        acc = acc * n
        n = n - 1
        if n == 2:
            n = n - 1
            continue
    return acc
i = 0
result = 0
unused_main_local = -1
no_args()
result = add(1, 2, 3)
STRINGLN('add(1,2,3) = $result')
result = add(-1, 1, 0)
STRINGLN('add(-1,1,0) = $result')
result = add(g, 1, unused_global)
STRINGLN('add(g,1,unused_global) = $result')
result = factorial(5)
STRINGLN('factorial(5) = $result')
factorial(0)
while i < 5  and  result != 0:
    i = i + 1
    if i == 3:
        break
HALT()
