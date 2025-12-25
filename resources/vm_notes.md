
## Ideas

PEEK and POKE commands?

PEEK8 PEEK32
POKE8 POKE32

write to any address

in single-arg non-str commands, preprocess to remove spaces after first word?



## To Do


## Done

* new opcode values
* new opcode names
* calling convention
* single stack
* internal registers
* PUSHC16 zero extension or sign extension?
* PUSHI POPI make sure little endian
* binOPs: Signed or unsigned?
* RSHIFT: logical or arithmetic?
* comparison instructions: signed or unsigned?
* new OLED instruction names
* watch out for unused function return value clogging up stack, discard if no assign? in compiler
* one-byte duckyscript commands, rewrite upper byte lower byte to 2ndLSB and LSB.
* what does SP point to? next free byte or current entry?
* reserved variable to switch signed or unsigned mode?
* VM runtime traps
	* stack underflow / overflow
	* invalid opcode
	* invalid PC
	* invalid alignment
	* version mismatch
	* divide zero
* `PUSHC16` zero extend or sign extend? Depend on mode?
* default signed or unsigned ?
* mention function always return 0 if not specified
* $ no longer required for variables, EXCEPT in printing commands
* allow inline comments?
* logical NOT operator
* SW bitfield
* GOTO_PROFILE works with both string names, numbers, and a single variable. NO EXPREESIONS, assign to a variable beforehand!
* SKIP_PROFILE n, jump ahead or back n profiles. Preprocess PREVP AND NEXTP into it
* Implement in-VM epilogue actions
* negative shift counts?
* POW negative exponent?
* allow inline comments?
* generate PGV save flag on DSVM itself not compiler
	* double check epilogue actions, which one by compiler which one by VM. probably most can be determined on runtime.


## Changelog

* increase sampling rate?

* `VMVER` instruction: version number now on byte 1 (LSB)

* Adjusted starting address and entry offset for
	* User-defined Variables
	* PGVs
	* Reserved Variables

* Added 32-bit push constant
	* By combining `PUSH16`, `LSHIFT`, and `BITOR.

* Opcode New Values

variable instruction length

## Symbol searching

first pass: treat as valid as long as is in any symbol table

when generating address, double check against global variable table?  classify_name()

error if try to read a variable name without it being ever assigned to?

## Variable Scoping

* A variable declared at root level has **global scope** and can be accessed inside functions.
	* All non-function variables have **Global Scope**
	* INCLUDING THOSE DECLARED WITHIN LOOPS AND IF STATEMENTS

* A variable declared **inside a function** only has scope **within that function**

* If a local variable has the same name as a global variable, **local variable** takes priority.