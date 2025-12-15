_GV0 = 100
global_acc = 5
unused_global = 9999
_UNUSED = asdfasdf
_UNSIGNED_MATH = 0  cfgdfg
def math_op(val, unused_arg):
    local_res = 0
    unused_local = 777
    local_res = val * 2
    return local_res
def flow_check(limit):
    i = 0
    while i < limit:
        if i == 2:
            _GV0 = _GV0 + 50
        else:
            _GV0 = _GV0 + 1
        if i == 4:
            break
        i = i + 1
    return 
global_acc = math_op(global_acc, 123) 
_UNUSED = flow_check(10)
STRINGLN('Result GV0: $_GV0')
STRINGLN('Result Global: $global_acc')
