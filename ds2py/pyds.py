global_counter = 100
def factorial(n):
    local_n = n
    if local_n <= 1:
        return 1
    next_n = local_n - 1
    recurse_result = factorial(next_n)
    result = local_n * recurse_result
    return result
def flow_test(limit):
    i = 0
    sum = 0
    while 1:
        i = i + 1
        if i > limit:
            STRINGLN('[Flow] Limit reached, breaking...')
            break
        if i == 3:
            STRINGLN('[Flow] Skipping 3 (Continue check)...')
            continue
        is_even = i % 2
        if is_even == 0:
            continue
        else:
            sum = sum + i
            STRINGLN('[Flow] Added odd number: $i')
    return sum
STRINGLN('=========================')
STRINGLN('STARTING COMPILER TEST')
STRINGLN('=========================')
STRINGLN('[Test 1] Recursion (Factorial 5)...')
fact_input = 5
fact_res = factorial(fact_input)
STRINGLN('Result: $fact_res')
if fact_res == 120:
    STRINGLN('>> SUCCESS: Recursion holds up.')
else:
    STRINGLN('>> FAILURE: Expected 120. Stack likely corrupted.')
STRINGLN('-------------------------')
STRINGLN('[Test 2] Complex Flow (Sum odds to 7, skip 3)...')
flow_res = flow_test(7)
STRINGLN('Result: $flow_res')
if flow_res == 13:
    STRINGLN('>> SUCCESS: Control flow logic is sound.')
else:
    STRINGLN('>> FAILURE: Expected 13. Jump targets likely wrong.')
STRINGLN('-------------------------')
STRINGLN('[Test 3] Scope Check...')
STRINGLN('Global Var is: $global_counter')
if global_counter == 100:
    STRINGLN('>> SUCCESS: Globals preserved.')
else:
    STRINGLN('>> FAILURE: Global var overwritten by stack operations.')
STRINGLN('=========================')
STRINGLN('TEST COMPLETE')
STRINGLN('=========================')
