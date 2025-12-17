# DuckStack Bytecode Stack Machine

DuckStack is a domain-specific stack-based bytecode VM for executing compiled **duckyScript** binary on 32-bit microcontrollers.

## Architecture

**32-bit** variables, arithmetics, and stack width.

**16-bit** addressing, 64KB max.

* Single **Data Stack**
* Program Counter (PC)
	* 16-bit byte-addressed
* Stack Pointer (SP)
	* 16-bit byte-addressed
	* Points to **the next free stack slot**
* Frame Pointer (FP)
	* Points to current function base frame

## Memory Map

* Flat memory map
* Byte-addressed

|Address|Purpose|Size|Comment|
|:-:|:--:|:--:|:--:|
|`0000`<br>`F7FF` |Shared<br>**Executable**<br>and **Stack**|63488 Bytes|See Notes Below|
|`F800`<br>`F9FF` |User-defined<br>Global<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|ZI Data|
|`FA00`<br>`FCFF` |Unused|768 Bytes||
|`FD00`<br>`FDFF` |Persistent<br>Global<br>Variables|256 Bytes<br>4 Bytes/Entry<br>64 Entries |NV Data<br>Saved on SD card|
|`FE00`<br>`FFFF` |VM<br>Reserved<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|Read/Adjust<br>VM Settings|

* Binary executable is loaded at `0x0`
* Stack grows from `0xF7FF` towards **smaller address**
	* Each item **4 bytes long**
	* In actual implementation, SP can be **4-byte aligned** for better performance.
* Smaller executable allows larger stack, vise versa.

## Instruction Set

**Variable-length** between **1 to 3 bytes**.

* First byte (Byte 0): **Opcode**.

* Byte 1 & 2: **Optional payload**.

* ⚠️Integer arithmetics are **signed** BY DEFAULT
	* Set reserved variable `_UNSIGNED_MATH = 1` to switch to **unsigned mode**

## CPU Instructions

* **1 stack item** = 4 **bytes**

* All multi-byte operations are **Little-endian**

* `PUSHR` / `POPR` **Offset** is a **byte-addressed signed 16-bit integer**
	* Positive: Towards larger address / Base of Stack
	* Negative: Towards smaller address / Top of Stack (TOS)

|Name|Inst.<br>Size|Opcode<br>Byte 0|Comment|Payload<br>Byte 1-2|
|:-:|:-:|:-:|:-:|:-:|
|`NOP`|1|`0`/`0x0` |Do nothing|None|
|`PUSHC16`|3|`1`/`0x1` |Push an **positive 16-bit (0-65535)** constant on stack<br>For negative numbers, push absolute value then use `USUB`.|2 Bytes:<br>`CONST_LSB`<br>`CONST_MSB` |
|`PUSHI`|3|`2`/`0x2` |Read **4 Bytes** at `ADDR`<br>Push to stack as one **32-bit** number|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`PUSHR`|3|`3`/`0x3`|Read **4 Bytes** at **offset from FP**<br>Push to stack as one **32-bit** number|2 Bytes:<br>`OFFSET_LSB`<br>`OFFSET_MSB`|
|`POPI`|3|`4`/`0x4` |Pop one item off TOS<br>Write **4 bytes** to `ADDR`|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`POPR`|3|`5`/`0x5`|Pop one item off TOS<br>Write as **4 Bytes** at **offset from FP**|2 Bytes:<br>`OFFSET_LSB`<br>`OFFSET_MSB`|
|`BRZ`|3|`6`/`0x6` |Pop one item off TOS<br>If value is zero, jump to `ADDR` |2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`JMP`|3|`7`/`0x7` |Unconditional Jump|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`ALLOC`|3|`8`/`0x8` |Push `n` blank entries to stack<br>Used to allocate local variables<br>on function entry|2 Bytes:<br>`n_LSB`<br>`n_MSB`|
|`CALL`|3|`9`/`0x9` |Construct 32b value `frame_info`:<br>Top 16b `current_FP`,<br>Bottom 16b `return_addr (PC+3)`.<br>Push `frame_info` to TOS<br>Set **FP** to TOS<br>Jump to `ADDR`|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`RET`|3|`10`/`0xa` |`return_value` on TOS<br>Pop `return_value` into temp location<br>Pop items until TOS is `FP`<br>Pop `frame_info`, restore **FP** and **PC**.<br>Pop off `ARG_COUNT` items<br>Push `return_value` back on TOS<br>Resumes execution at PC|2 Bytes:<br>`ARG_COUNT`<br>`Reserved`|
|`HALT`|1|`11`/`0xb` |Stop execution|None|
|`VMVER`|3|`255`/`0xff`| VM Version Check<br>Abort if mismatch |2 Bytes:<br>`VM_VER`<br>`Reserved`|

## Binary Operator Instructions

Binary as in **involving two operands**.

* All **single-byte** instruction

* Pop **TWO** items off TOS

* Top item is right-hand-side, lower item is left-hand-side.

* Perform operation

* Push result back on TOS

-----

* ⚠️ = Affected by current **Arithmetic Mode**
	* Default: Signed
	* Unsigned mode if `_UNSIGNED_MATH = 1`

|Name|Opcode<br>Byte 0|Comment|
|:--:|:--:|:--:|
|EQ|`32`/`0x20`|Equal|
|NOTEQ|`33`/`0x21`|Not Equal|
|LT|`34`/`0x22`|⚠️Less Than|
|LTE|`35`/`0x23`|⚠️Less Than or Equal|
|GT|`36`/`0x24`|⚠️Greater Than|
|GTE|`37`/`0x25`|⚠️Greater Than or Equal|
|ADD|`38`/`0x26`|Add|
|SUB|`39`/`0x27`|Subtract|
|MULT|`40`/`0x28`|Multiply|
|DIV|`41`/`0x29`|⚠️Integer Division|
|MOD|`42`/`0x2a`|⚠️Modulus|
|POW|`43`/`0x2b`|Power of|
|LSHIFT|`44`/`0x2c`|Left shift|
|RSHIFT|`45`/`0x2d`|⚠️Right shift<br>Signed Mode: Arithmetic (sign-extend)<br>Unsigned Mode: Logical (0-extend)|
|BITOR|`46`/`0x2e`|Bitwise OR|
|BITXOR|`47`/`0x2f`|Bitwise XOR|
|BITAND|`48`/`0x30`|Bitwise AND|
|LOGIAND|`49`/`0x31`|Logical AND|
|LOGIOR|`50`/`0x32`|Logical OR|

## Unary Operators

* All **single-byte** instruction

* Pop **ONE** items off TOS

* Perform operation

* Push result back on TOS

|Name|Opcode<br>Byte 0|Comment|
|:--:|:--:|:--:|
|BITINV|`55`/`0x37`|Bitwise Invert|
|LOGINOT|`56`/`0x38`|Logical NOT|
|USUB|`57`/`0x39`|Unary Minus|

## duckyScript Command Instructions

* All **single-byte** instruction

|Name|Opcode<br>Byte 0|Comment|
|:-------:|:----------:|:---------:|
|DELAY|`64`/`0x40`| **Delay**<br>Pop **ONE** item<br>Delay amount in **milliseconds**|
|KDOWN|`65`/`0x41`| **Press Key**<br>Pop **ONE** item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|KeyType\|KeyCode\|`|
|KUP|`66`/`0x42`|**Release Key**<br>Pop **ONE** item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|KeyType\|KeyCode\|`|
|MSCL|`67`/`0x43`| **Mouse Scroll**<br>Pop **ONE** item<br>Scroll number of lines|
|MMOV|`68`/`0x44`|**Mouse Move**<br>Pop **TWO** items: `x` then `y`|
|SWCF|`69`/`0x45`| **Switch Color Fill**<br>Pop **THREE** items<br>`Red, Green, Blue`<br>Set ALL LED color to the RGB value|
|SWCC|`70`/`0x46`| **Switch Color Change**<br>Pop **FOUR** item<br>`N, Red, Green, Blue`<br>Set N-th switch to the RGB value<br>If N is 0, set current switch.|
|SWCR|`71`/`0x47`| **Switch Color Reset**<br>Pop **ONE** item<br>If value is 0, reset color of current key<br>If value is between 1 and 20, reset color of that key<br>If value is 99, reset color of all keys.|
|STR|`72`/`0x48`|**Type String**<br>Pop **ONE** item as `ADDR`<br>Print zero-terminated<br>string at `ADDR`|None||
|STRLN|`73`/`0x49`|**Type Line**<br>Pop **ONE** item as `ADDR`<br>Print zero-terminated<br>string at `ADDR`<br>**Press ENTER at end**|
|OLED_CUSR|`74`/`0x4a`|**OLED Set Cursor**<br>Pop **TWO** items: `x` then `y`||
|OLED_PRNT|`75`/`0x4b`|**OLED Print**<br>Pop **ONE** item as `ADDR`<br>Print zero-terminated<br>string at `ADDR` to OLED|None|
|OLED_UPDE|`76`/`0x4c`|**OLED Update**|
|OLED_CLR|`77`/`0x4d`|**OLED Clear**|
|OLED_REST|`78`/`0x4e`| **OLED Restore**|
|OLED_LINE|`79`/`0x4f`|**OLED Draw Line**<br>Pop **FOUR** items<br>`x1, y1, x2, y2`<br>Draw single-pixel line in-between|
|OLED_RECT|`80`/`0x50`|**OLED Draw Rectangle**<br>Pop **FIVE** items<br>`fill, x1, y1, x2, y2`<br>Draw rectangle between two points<br>Fill if `fill` is non-zero|
|OLED_CIRC|`81`/`0x51`|**OLED Draw Circle**<br>Pop **FOUR** items<br>`fill, radius, x, y`<br>Draw circle with `radius` at `(x,y)`<br>Fill if `fill` is non-zero|
|BCLR|`82`/`0x52`|**Clear switch event queue**|
|SKIPP|`83`/`0x53`| **Skip Profile**<br>Pop **ONE** item as `n`<br>Increment/Decrement `n`<br>profiles from current the one|
|GOTOP|`84`/`0x55`| **Goto Profile by NAME**<br>Pop **ONE** item as `ADDR`<br>Go to profile name as<br>zero-terminated string at `ADDR`|
|SLEEP|`85`/`0x56`| **Sleep**<br>Put duckyPad to sleep<br>Terminates execution|
|WAITK|`86`/`0x57`| **Wait for Keypress**<br>Pop **ONE** item as `KeyID`<br>Block until the key is pressed<br> 0 = Any key|

## Calling Convention

* Multiple arguments, one return value.
* Supports nested and recursive calls
* **TOS** grows towards **smaller address**

### Stack Set-up

Outside function calls, FP points to **base of stack.**

||...|
|:--:|:--:|
||`32-bit data`|
||...|
|`FP ->`|Base (`F7FF`)|

When calling a function: **`foo(a, b, c)`**

* **Caller** pushes 32-bit arguments **right to left** to stack
	* Don't push if no args.

|||
|:--:|:--:|
||`a`|
||`b`|
||`c`|
||...|
|`FP ->`|Base (`F7FF`)|

Caller then executes `CALL` instruction, which:

* Constructs a 32b value `frame_info`
	* Top 16b: `current_FP`
	* Bottom 16b: `return_address`
* Pushes `frame_info` to TOS
* Sets **FP** to TOS
* Jumps to the function address

|||
|:--:|:--:|
|`FP ->`|`Prev_FP \| Return_addr`|
||`a`|
||`b`|
||`c`|
||...|
||Base (`F7FF`)|

### Function Arguments

Once in function, callee uses `ALLOC n` to make space for local variables.

To reference arguments and locals, **FP + Byte_Offset** is used.

* **Negative** offset towards **smaller address / TOS / locals**.
	* `FP - 4` points to **first local**, etc
* **Positive** offset towards **larger address / base of stack / args**.
	* `FP + 4` points to **leftmost argument**, etc
* Use `PUSHR + Offset` and `POPR + Offset` to read/write to args and locals.

|||
|:--:|:--:|
||...|
|`FP - 8`|`localvar_2`|
|`FP - 4`|`localvar_1`|
|`FP ->`|`Prev_FP \| Return_addr`|
|`FP + 4`|`a`|
|`FP + 8`|`b`|
|`FP + 12`|`c`|
||...|
||Base (`F7FF`)|

### Stack Unwinding

At end of a function, `return_value` is on TOS.

* If no explicit `RETURN` statement, **0 is returned**.

|||
|:--:|:--:|
||`return_value`|
||`temp data`|
|`FP - 8`|`localvar_2`|
|`FP - 4`|`localvar_1`|
|`FP ->`|`Prev_FP \| Return_addr`|
|`FP + 4`|`a`|
|`FP + 8`|`b`|
|`FP + 12`|`c`|
||...|
||Base (`F7FF`)|

**Callee** executes `RET n` instruction, which:

* Pops off `return_value` into temp location
* Pop off items until `frame_info` is on **TOS**
	* AKA `SP + 4 == FP`
* Pops off `frame_info`
	* Loads `previous FP` into **FP**
	* Loads `return address` into **PC**
* Pops off `n` arguments
* Pushes `return_value` back on TOS
* Resumes execution at PC
* Return value now on TOS for caller to use

|||
|:--:|:--:|
||`return_val`|
||...|
|`FP ->`|Base (`F7FF`)|


## To Do

* generate PGV save flag on DSVM itself not compiler
	* double check epilogue actions, which one by compiler which one by VM. probably most can be determined on runtime.
* Implement WAIT_KEY
* Implement in-VM epilogue actions
* negative shift counts?
* POW negative exponent?
* allow inline comments?
* GOTO_PROFILE works with both string names, numbers, and a single variable. NO EXPREESIONS, assign to a variable beforehand!
* SKIP_PROFILE n, jump ahead or back n profiles. Preprocess PREVP AND NEXTP into it

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