STRINGLN('--- START TEST ---')
STRINGLN('[SEC 1] Math & Logic')
a = 10
b = 20
c = 0
c = a + b * 2
STRINGLN('TEST 1 (PEMDAS): $c')
c = b / 3
STRINGLN('TEST 2 (IntDiv): $c')
c = a - b
STRINGLN('TEST 3 (Signed): $c')
_UNSIGNED_MATH = 1
STRINGLN('TEST 4 (Unsigned Cast): $c')
_UNSIGNED_MATH = 0
STRINGLN('[SEC 2] Control Flow')
i = 0
STRINGLN('Loop Start:')
while i < 6:
    if i == 2:
        i = i + 1
        continue
    if i == 5:
        break
    STRINGLN('Iter: $i')
    i = i + 1
STRINGLN('Loop End.')
STRINGLN('[SEC 3] Functions')
globalVar = 999
def scopeTest(arg1):
    globalVar = 111
    STRINGLN('Inside Func Local: $globalVar')
    STRINGLN('Inside Func Arg: $arg1')
    return globalVar + arg1
result = 0
_UNUSED = scopeTest(50)
result = scopeTest(50)
STRINGLN('Return Value: $result')
STRINGLN('Global Unchanged: $globalVar')
STRINGLN('[SEC 4] Recursion (Factorial)')
def factorial(n):
    if n <= 1:
        return 1
    sub = n - 1
    rec = factorial(sub)
    return n * rec
fact5 = factorial(5)
STRINGLN('Fact(5): $fact5')
STRINGLN('[SEC 5] Bitwise')
mask = 255
val = 43690
shift = 1
resAnd = val & mask
STRINGLN('Bitwise AND: $resAnd')
resShift = shift << 4
STRINGLN('Left Shift: $resShift')
STRINGLN('[SEC 6] Formatting')
hexVal = 255
_STR_PRINT_FORMAT = 2
STRINGLN('Hex Lower: $hexVal')
_STR_PRINT_FORMAT = 3
_STR_PRINT_PADDING = 4
STRINGLN('Hex Pad: $hexVal')
_STR_PRINT_FORMAT = 0
_STR_PRINT_PADDING = 0
STRINGLN('--- END TEST ---')
