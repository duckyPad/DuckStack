result = 0
counter = 0
shadow_test = 999
def factorial(n):
    if n <= 1:
        return 1
    prev_step = 0
    val_minus_one = n - 1
    prev_step = factorial(val_minus_one)
    return n * prev_step
def hardware_check(arg1):
    shadow_test = 50
    MOUSE_MOVE(10, -10)
    DELAY(100)
    OLED_CLEAR()
    OLED_RECT(1, 0, 0, 32, 32)
    OLED_UPDATE()
    return shadow_test + arg1
STRINGLN('Starting Stress Test...')
math_check = (5 * 2) + (8 >> 2)
STRINGLN('Math Check (Expect 12): $math_check')
while counter < 3:
    STRINGLN('Loop Index: $counter')
    f_input = counter + 1
    result = factorial(f_input)
    STRINGLN('Factorial Result: $result')
    if (counter & 1) == 0:
        STRINGLN('Status: Even')
    if (counter & 1) != 0:
        STRINGLN('Status: Odd')
    counter = counter + 1
hw_result = 0
hw_result = hardware_check(10)
STRINGLN('Local Shadow Result (Expect 60): $hw_result')
STRINGLN('Global Shadow Var (Expect 999): $shadow_test')
STRINGLN('Test Complete.')
