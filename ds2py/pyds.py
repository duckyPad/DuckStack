g_acc = 0
shadow_val = 99
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
def precedence_check(shadow_val):
    local_calc = 0
    local_calc = shadow_val + 1 << 2
    STRINGLN('[Func] Arg shadow_val: $shadow_val (Expect 5)')
    STRINGLN('[Func] Calc result: $local_calc (Expect 24 if Add > Shift)')
    return local_calc
STRINGLN('=== START TORTURE TEST ===')
STRINGLN('Global shadow_val is: $shadow_val')
neg_val = -5
abs_val = 0
if neg_val < 0:
    abs_val = 0 - neg_val
STRINGLN('Abs value of -5 is: $abs_val')
STRINGLN('--- Starting Loop Test ---')
i = 0
j = 0
while i < 2:
    i = i + 1
    STRINGLN('Outer Loop: $i')
    j = 0
    while 1:
        j = j + 1
        if j == 2:
            STRINGLN('Skipping 2...')
            continue
        if j > 3:
            STRINGLN('Breaking Inner...')
            break
        STRINGLN('Inner Loop: $j')
prec_result = precedence_check(5)
if shadow_val == 99:
    STRINGLN('[Pass] Global shadow_val remains 99.')
if shadow_val != 99:
    STRINGLN('[FAIL] Global shadow_val corrupted! Is: $shadow_val')
fact_in = 5
fact_out = factorial(fact_in)
STRINGLN('Factorial of 5 is: $fact_out')
STRINGLN('Tokenizer Check: This // is NOT a comment?')
_STR_PRINT_FORMAT = 2
mask_test = 255 & 15
STRINGLN('Hex 255 & 15 is: $mask_test (Expect f)')
STRINGLN('=== END TORTURE TEST ===')
HALT()
