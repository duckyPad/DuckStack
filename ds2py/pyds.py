def factorial(n):
    if n <= 1:
        return 1
    prev = n - 1
    sub_res = factorial(prev)
    return n * sub_res
STRINGLN('Starting Recursion Test...')
input = 5
result = factorial(input)
STRINGLN('Factorial of $input is: $result')
if result == 120:
    STRINGLN('SUCCESS: Stack unwound correctly.')
else:
    STRINGLN('FAILURE: Result mismatch.')
