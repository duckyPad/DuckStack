_UNSIGNED_MATH = 0
_STR_PRINT_FORMAT = 1
STRINGLN('--- SIGNED MATH (Default) ---')
val_neg = -16
res_shift = val_neg >> 1
STRINGLN('Signed Shift (-16 >> 1): $res_shift')
res_div = val_neg / 2
STRINGLN('Signed Div (-16 / 2): $res_div')
res_mod = -10 % 3
STRINGLN('Signed Mod (-10 % 3): $res_mod')
res_pow = (-2) ** 2
STRINGLN('Signed Pow (-2 ^ 2): $res_pow')
STRINGLN('')
_UNSIGNED_MATH = 1
_STR_PRINT_FORMAT = 0
STRINGLN('--- UNSIGNED MATH ---')
u_val = -16
u_shift = u_val >> 1
STRINGLN('Unsigned Shift (0xFFFFFFF0 >> 1): $u_shift')
u_div = u_val / 2
STRINGLN('Unsigned Div (0xFFFFFFF0 / 2): $u_div')
u_mod = u_val % 17
STRINGLN('Unsigned Mod (0xFFFFFFF0 % 17): $u_mod')
base = 2
exp = 31
u_pow = base ** exp
STRINGLN('Unsigned Pow (2 ^ 31): $u_pow')
STRINGLN('')
STRINGLN('--- PRINT FORMATS ---')
test_val = -1
_STR_PRINT_FORMAT = 0
STRINGLN('Format 0 (Unsigned): $test_val')
_STR_PRINT_FORMAT = 1
STRINGLN('Format 1 (Signed): $test_val')
_STR_PRINT_FORMAT = 2
STRINGLN('Format 2 (Hex Lower): $test_val')
_STR_PRINT_FORMAT = 3
STRINGLN('Format 3 (Hex Upper): $test_val')
