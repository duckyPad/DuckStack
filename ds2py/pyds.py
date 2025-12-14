STRINGLN('Starting Test...')
STRINGLN('Constant Check: 5 (Should be 5)')
a = 10
b = 20
result = 0
result = a + b * 2 
STRINGLN('Math Precedence Result: $result')
negative = -50
positive = 25
signed_res = negative + positive
STRINGLN('Signed Math (-25): $signed_res')
flags = 1
flags = flags << 2
flags = flags | 1
STRINGLN('Bitwise Ops (5): $flags')
i = 0
STRINGLN('Testing While Loop')
STRINGLN('Expect 0, 1, skip 2, 3, 4')
while i < 5:
    if i == 2:
        STRINGLN('Skipping Two...')
        i = i + 1
        continue
    if i == 10:
        break
    STRINGLN('Loop Index: $i')
    i = i + 1
global_var = 999
def scope_test(arg1, arg2):
    global_var = 1
    local_sum = arg1 + arg2 + global_var
    STRINGLN('Inside Func - Local Shadow: $global_var')
    STRINGLN('Inside Func - Arg Sum: $local_sum')
    return local_sum
STRINGLN('--- Calling Scope Test (10, 20) ---')
func_res = scope_test(10, 20)
STRINGLN('Returned Value (31): $func_res')
STRINGLN('Global Var Unchanged (999): $global_var')
def factorial(n):
    if n <= 1:
        return 1
    sub_result = factorial(n - 1)
    return n * sub_result
fact_input = 5
fact_res = factorial(fact_input)
STRINGLN('Factorial of 5 (120): $fact_res')
_RANDOM_MIN = 1
_RANDOM_MAX = 10
rng = _RANDOM_INT
STRINGLN('Random Number (1-10): $rng')
_STR_PRINT_FORMAT = 2
hex_val = 255
STRINGLN('Hex ff: $hex_val')
_STR_PRINT_FORMAT = 0
STRING('Testing Repeats...')
STRING('Testing Repeats...')
STRING('Testing Repeats...')
STRING('Testing Repeats...')
MOUSE_MOVE(100, 50)
DELAY(50)
OLED_CLEAR()
OLED_RECT(1, 0, 0, 128, 64)
OLED_UPDATE()
STRINGLN('Tests Complete.')
