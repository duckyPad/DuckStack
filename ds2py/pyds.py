myVar = 100
counter = 1
def scopeCheck(myVar):
    STRINGLN('[FUNC] Arg myVar: $myVar')
    localVar = 777 + myVar
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
