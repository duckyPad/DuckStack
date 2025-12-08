unused_global = 12345
gShadow = -1
_GV0 = 42
def unused_fn(a, b, c, d, e, f, g, h):
    never_used = a + b + c + d + e + f + g + h
    return 0
def noop():
    dead = 1
    return 
    dead = 2
def fact(n, unused1, unused2):
    tmp_unused = 999
    if n <= 1:
        return 1
    return n * fact(n - 1, unused2, unused1)
def mix8(a, b, c, d, e, f, g, h):
    unused_local = d + e
    t = 0
    u = 0
    u = f << 1
    t = a + b * 2 - c
    t = t ^ u
    if t == 0:
        return 7
    return (t + h) >> 1
def sum_skip(limit, step, junk):
    i = 0
    acc = 0
    while 1:
        i = i + step
        if i > limit:
            break
        if i % 3 == 0:
            continue
        acc = acc + i
    return acc
x = mix8(1, 2, fact(4, 0, 0), 4, 5, 6, 7, 8)
y = fact(5, 111, 222)
z = sum_skip(10, 1, 999)
fact(3, 0, 0)
noop()
if x != 0  and  y > 0:
    STRINGLN('x=$x y=$y z=$z gv0=$_GV0 magic=7')
never = 0
while never:
    STRINGLN('unreachable loop body')
HALT()
