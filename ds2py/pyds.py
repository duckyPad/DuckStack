myglobal = 4
def foo(a, b):
    mylocal = a * b + myglobal
    return mylocal
def bar(c, d):
    mylocal = c + d
    return mylocal
test = foo(3, 5)
test = bar(test, test)
