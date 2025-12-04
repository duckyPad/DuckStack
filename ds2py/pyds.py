_NEEDS_EPILOGUE = 6
_DEFAULTDELAY = 10
_DEFAULTCHARDELAY = 5
_CHARJITTER = 2
score = 0
multiplier = 2
bitmask = 255
complex_calc = 0
complex_calc = (10 + 5) * 2
score = complex_calc / 3
flags = 1
flags = flags << 2
flags = flags | 1
flags = flags & 7
OLED_CLEAR()
OLED_CIRCLE(64, 32, 10, 1)
OLED_RECT(0, 0, 127, 63, 0)
OLED_LINE(0, 0, 127, 63)
OLED_CURSOR(0, 0)
OLED_PRINT('Running: //Compiler_Test')
OLED_CURSOR(0, 10)
OLED_PRINT('Ver: $APP_VERSION')
OLED_UPDATE()
DELAY(500)
STRINGLN('Starting keyboard test...')
STRINGLN('    Line 1: Testing //Block')
STRINGLN('    Line 2: Still testing')
KEYDOWN('WINDOWS')
KEYDOWN('r')
KEYUP('r')
KEYUP('WINDOWS')
DELAY(200)
STRING('notepad')
KEYDOWN('ENTER')
KEYUP('ENTER')
DELAY(500)
KEYDOWN('SHIFT // dsffsd')
STRING('hello //uppercase')
KEYUP('SHIFT')
KEYDOWN('ENTER')
KEYUP('ENTER')
STRING('a')
STRING('a')
STRING('a')
STRING('a')
STRING('a')
STRING('a')
i = 0
loop_check = 0
while i < 5:
    if i == 2  or  i == 4:
        STRINGLN('Iteration $i: Even(ish)')
    if i == 3:
        break
    i = i + 1
    loop_check = loop_check + 1
def calculate_area(width, height):
    area = 0
    area = width * height
    _STR_PRINT_FORMAT = 2
    STRINGLN('Hex Area: $area')
    _STR_PRINT_FORMAT = 0
    return 
calculate_area(10, 5)
MOUSE_MOVE(100, 0)
DELAY(50)
MOUSE_MOVE(0, 100)
DELAY(50)
MOUSE_MOVE(-100, 0)
DELAY(50)
MOUSE_MOVE(0, -100)
MOUSE_WHEEL(5)
KEYDOWN('LMOUSE')
KEYUP('LMOUSE')
KEYDOWN('RMOUSE')
KEYUP('RMOUSE')
SWC_FILL(255, 0, 0)
SWC_SET(1, 0, 255, 0)
DELAY(100)
SWC_RESET(0)
_RANDOM_MIN = 1
_RANDOM_MAX = 100
rand_val = _RANDOM_INT
STRINGLN('Random Value: $rand_val')
STRINGLN('System Time ms: $_TIME_MS')
_STR_PRINT_PADDING = 5
STRINGLN('Padded Score: $score')
STRINGLN('Test Complete.')
