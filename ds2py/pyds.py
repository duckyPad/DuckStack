global_val = 100
shadow_me = 999
unused_global = 5555
def test_scope(arg_used, arg_unused4, arg_unused2, arg_unused1):
    unused_local = 777
    local_val = 50
    shadow_me = 111
    STRINGLN('TIME: $_RTC_HOUR')
    STRINGLN('Read Global: $global_val')
    STRINGLN('Read Arg: $arg_used')
    STRINGLN('Read Shadowed Local: $shadow_me')
    shadow_me = shadow_me + 1
    STRINGLN('Modified Shadowed Local: $shadow_me')
    return arg_used + local_val
result = 0
result = test_scope(10, 20, 0,0)
STRINGLN('Global Shadow Check: $shadow_me')
STRINGLN('Function Return: $result')
