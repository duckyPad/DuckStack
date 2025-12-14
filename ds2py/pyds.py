g_counter = 0
g_result = 0
g_shadow_me = 9999
g_flags = 0
def math_calc(a, b):
    local_res = 0
    local_res = (a * 2) + (b / 2) - (a % 3)
    g_shadow_me = 1
    local_res = local_res + g_shadow_me
    return local_res
def factorial(n):
    if n <= 1:
        return 1
    temp = 0
    temp = factorial(n - 1)
    return n * temp
STRINGLN('Starting System Test...')
STRINGLN('Checking Math...')
g_result = math_calc(10, 20)
if g_result == 30:
    STRINGLN('[PASS] Math & Scoping')
else:
    STRINGLN('[FAIL] Math & Scoping: Got $g_result')
if g_shadow_me == 9999:
    STRINGLN('[PASS] Global Shadowing Integrity')
else:
    STRINGLN('[FAIL] Global Shadowing: Var clobbered!')
g_result = factorial(5) 
STRINGLN('Factorial of 5 is: $g_result')
bit_val = 1
bit_val = bit_val << 4
bit_val = bit_val | 1
bit_val = bit_val & 240
if bit_val == 16  and  g_shadow_me > 0:
    STRINGLN('[PASS] Bitwise Logic')
STRINGLN('Starting Loop Test...')
i = 0
while 1:
    i = i + 1
    if i == 2:
        STRINGLN('- Skipping 2')
        continue
    STRINGLN('- Count: $i')
    if i >= 4:
        break
STRINGLN('Testing IO...')
MOUSE_MOVE(100, -50)
DELAY(100)
MOUSE_MOVE(-100, 50)
MOUSE_WHEEL(2)
KEYDOWN('CTRL')
STRING('c')
KEYUP('CTRL')
OLED_CLEAR()
OLED_RECT(1, 0, 0, 32, 32)
OLED_CIRCLE(0, 5, 16, 16)
OLED_PRINT('Done.')
OLED_UPDATE()
_STR_PRINT_FORMAT = 3
_STR_PRINT_PADDING = 4
STRINGLN('Hex check (Should be 001E): $g_result')
_UNSIGNED_MATH = 1
neg_check = 0 - 1
STRINGLN('Unsigned -1 is: $neg_check')
_UNSIGNED_MATH = 0
STRINGLN('Test Complete.')
STRINGLN('Sending Report to admin@example.com...')
