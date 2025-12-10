global_res = 0
def factorial(n):
    acc = 1
    i = 1
    while i <= n:
        acc = acc * i
        i = i + 1
    return acc
STRINGLN('Starting Calculation...')
global_res = factorial(5)
_STR_PRINT_FORMAT = 3
STRINGLN('Result (0x78 expected): $global_res')
if global_res == 120:
    STRINGLN('Test Passed!')
    DELAY(500)
    KEYDOWN('WINDOWS')
    KEYDOWN('r')
    KEYUP('r')
    KEYUP('WINDOWS')
    DELAY(200)
    STRINGLN('notepad')
