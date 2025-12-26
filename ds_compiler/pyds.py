alpha = 10
beta = 32
result = alpha + beta
if result == 42:
    _DSVM_DUMMY = STRING('The answer is $result!')
else:
    _DSVM_DUMMY = STRING('Error: $result is wrong.')
_DSVM_DUMMY = HALT()
