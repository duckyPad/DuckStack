global_counter = 0
bit_flags = 0
def complex_math(arg1, arg2):
    local_res = 0
    local_res = arg1 * 2
    local_res = local_res + arg2 / 5
    global_counter = global_counter + 1
    return local_res
STRINGLN('[TEST] String Block Check.')
STRINGLN('If you see this, blocks work.')
STRINGLN('Starting_Test...')
i = 0
while i < 5:
    if i > 0  and  i < 4:
        STRING('.')
    if i == 4:
        STRINGLN('[OK] Loop Finished.')
        break
    i = i + 1
    DELAY(10)
bit_flags = 1 << 4 
mask_check = bit_flags | 1
math_result = 0
math_result = complex_math(10, 100)
STRINGLN('Result (Dec): $math_result')
_STR_PRINT_FORMAT = 3
_STR_PRINT_PADDING = 4
STRINGLN('Result (HexPad): $math_result')
_STR_PRINT_FORMAT = 0
_STR_PRINT_PADDING = 0
_RANDOM_MIN = 50
_RANDOM_MAX = 60
rand_val = _RANDOM_INT
STRINGLN('Random(50-60): $rand_val')
KEYDOWN('SHIFT')
STRING('test')
KEYUP('SHIFT')
KEYDOWN('ENTER')
KEYUP('ENTER')
MOUSE_MOVE(100, 50)
MOUSE_WHEEL(-2)
STRING('Echo ')
STRING('Echo ')
STRING('Echo ')
KEYDOWN('ENTER')
KEYUP('ENTER')
_GV0 = _GV0 + 1
STRINGLN('Boot_Count: $_GV0')
STRINGLN('[SUCCESS] Torture test complete.')
