_DEFAULTDELAY = 20
_DEFAULTCHARDELAY = 5
_CHARJITTER = 10
_ALLOW_ABORT = 1
_DONT_REPEAT = 0
DELAY(600)
OLED_CLEAR()
OLED_CURSOR(0, 0)
OLED_PRINT('duckyScript Compiler Workout')
OLED_CURSOR(0, 12)
OLED_PRINT('KeyID=$_THIS_KEYID')
OLED_CURSOR(0, 24)
OLED_PRINT('Model=$_DP_MODEL')
OLED_CURSOR(0, 36)
OLED_PRINT('t(ms)=$_TIME_MS')
OLED_LINE(0, 49, 127, 49)
OLED_RECT(0, 52, 45, 63, 1)
OLED_CIRCLE(105, 57, 5, 0)
OLED_UPDATE()
SWC_FILL(8, 8, 8)
SWC_SET(1, 255, 0, 0)
SWC_SET(2, 0, 255, 0)
SWC_SET(3, 0, 0, 255)
DELAY(120)
SWC_RESET(1)
SWC_RESET(2)
SWC_RESET(3)
STRINGLN('==== duckyScript Compiler Workout ====')
STRINGLN('If you can read this, typing works.')
STRINGLN('This is a STRINGLN_BLOCK.')
STRINGLN('Each line should type and press ENTER.')
STRINGLN('Line 3: symbols !@#$%^&*()_+-=[]{};\':",.<>/?')
STRING('This is a STRING_BLOCK: it should not press ENTER between lines,')
STRING('but it *should* type all text as-is.')
KEYDOWN('ENTER')
KEYUP('ENTER')
a = 7
b = 3
add = a + b
sub = a - b
mul = a * b
div = a / b
mod = a % b
pow = a ** b
bit_and = a & b
bit_or  = a | b
bit_xor = a ^ b
shl = a << 2
shr = 128 >> 3
gt0 = a > 0
lt0 = b < 0
logic_and = gt0  and  lt0
logic_or  = gt0  or  lt0
STRINGLN('a=$a b=$b')
STRINGLN('add=$add sub=$sub mul=$mul div=$div mod=$mod pow=$pow')
STRINGLN('and=$bit_and or=$bit_or xor=$bit_xor shl=$shl shr=$shr')
STRINGLN('gt0=$gt0 lt0=$lt0 &&=$logic_and ||=$logic_or')
foo = 65409
neg = 0 - 127
_STR_PRINT_FORMAT = 0
STRINGLN('fmt0 unsigned foo=$foo')
_STR_PRINT_FORMAT = 1
STRINGLN('fmt1 signed foo=$foo neg=$neg')
_STR_PRINT_FORMAT = 2
STRINGLN('fmt2 hex-lower foo=$foo')
_STR_PRINT_FORMAT = 3
STRINGLN('fmt3 HEX-UPPER foo=$foo')
_STR_PRINT_FORMAT = 0
_STR_PRINT_PADDING = 2
year = 2025
month = 8
day = 5
STRINGLN('padded date $year-$month-$day')
_STR_PRINT_PADDING = 0
amount = 100
DELAY(amount*2+5)
STRINGLN('REPEAT demo line')
STRINGLN('REPEAT demo line')
STRINGLN('REPEAT demo line')
STRINGLN('REPEAT demo line')
_RANDOM_MIN = 10
_RANDOM_MAX = 20
r = _RANDOM_INT
STRINGLN('random[10..20]=$r')
_GV0 = _GV0 + 1
STRINGLN('persistent _GV0 now=$_GV0')
_KEYPRESS_COUNT = 0
STRINGLN('keypress_count reset to $_KEYPRESS_COUNT')
spam = mod
if spam == 0:
    STRINGLN('spam==0 branch')
elif spam == 1:
    STRINGLN('spam==1 branch')
else:
    STRINGLN('spam==other branch (spam=$spam)')
i = 0
while i < 8:
    i = i + 1
    if i == 3:
        STRINGLN('i=$i -> CONTINUE')
        continue
    STRINGLN('loop i=$i')
    if i == 6:
        STRINGLN('i=$i -> LBREAK')
        break
def clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v
def fib(n):
    fa = 0
    fb = 1
    k = 0
    while k < n:
        t = fa + fb
        fa = fb
        fb = t
        k = k + 1
    return fa
def is_even(x):
    if x % 2 == 0:
        return 1
    return 0
c1 = clamp(5, 0, 10)
c2 = clamp(0 - 5, 0, 10)
c3 = clamp(50, 0, 10)
STRINGLN('clamp: $c1 $c2 $c3')
f10 = fib(10)
STRINGLN('fib(10)=$f10')
e7 = is_even(7)
e8 = is_even(8)
STRINGLN('even(7)=$e7 even(8)=$e8')
if 0:
    KEYDOWN('CTRL')
    KEYDOWN('c')
    KEYUP('c')
    KEYUP('CTRL')
    KEYDOWN('CTRL')
    KEYDOWN('v')
    KEYUP('v')
    KEYUP('CTRL')
    KEYDOWN('WINDOWS')
    KEYUP('WINDOWS')
    KEYDOWN('TAB')
    KEYUP('TAB')
    KEYDOWN('ESC')
    KEYUP('ESC')
    KEYDOWN('F1')
    KEYUP('F1')
    KEYDOWN('MK_MUTE')
    KEYUP('MK_MUTE')
    KEYDOWN('ALT')
    KEYDOWN('KP_1')
    KEYUP('KP_1')
    KEYDOWN('KP_7')
    KEYUP('KP_7')
    KEYDOWN('KP_2')
    KEYUP('KP_2')
    KEYUP('ALT')
    MOUSE_MOVE(20, 10)
    KEYDOWN('LMOUSE')
    KEYUP('LMOUSE')
    MOUSE_WHEEL(-3)
    KEYDOWN('RMOUSE')
    KEYUP('RMOUSE')
    NEXT_PROFILE()
    PREV_PROFILE()
    GOTO_PROFILE(NumPad)
    DP_SLEEP()
OLED_RESTORE()
SWC_RESET(99)
STRINGLN('==== DONE ====')
HALT()
