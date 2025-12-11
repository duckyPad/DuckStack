true_val = 1
not_true =  not true_val
STRINGLN('!1 is $not_true')
false_val = 0
not_false =  not false_val
STRINGLN('!0 is $not_false')
if not false_val:
    STRINGLN('Correct path')
else:
    STRINGLN('Wrong path')
DELAY(3+, not, 9)
