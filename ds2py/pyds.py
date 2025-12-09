myVar = 100
counter = 1
def scopeCheck(myVard):
    STRINGLN('[FUNC] Arg myVard: $myVard')
    localVar = 777
    localVar = localVar + 1
    counter = counter + 1
    STRINGLN('[FUNC] LocalVar: $localVar')
    STRINGLN('[FUNC] Global Counter: $counter')
    return 
STRINGLN('[MAIN] Start Global: $myVar')
STRINGLN('[MAIN] Start Counter: $counter')
_UNUSED = scopeCheck(50)
STRINGLN('[MAIN] End Global: $myVar')
STRINGLN('[MAIN] End Counter: $counter')
