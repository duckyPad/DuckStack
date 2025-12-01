# DuckStack Bytecode Stack Machine

## Architecture

**32-bit** variables, arithmetics, and stack width.

**16-bit** addressing, 64KB max.

* Single **Data Stack**
* Program Counter (PC)
* Stack Pointer (SP)
	* Points to **currently occupied entry?**
* Frame Pointer (FP)

## Memory Map

* Flat memory map
* Byte-addressed

|Address|Purpose |Comment |
|:-:|:--:|:--:|
|`0000`<br>`EFFF` |Binary<br>Executable|60K Bytes|
|`F000`<br>`F7FF` |Data Stack|2048 Bytes<br>4 Bytes/Entry<br>512 Entries|
|`F800`<br>`F9FF` |User-defined<br>Global<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|
|`FA00`<br>`FBFF` |Unused|512 Bytes|
|`FC00`<br>`FCFF`|VM Scratch<br>Memory|256 Bytes<br>4 Bytes/Entry<br>64 Entries|
|`FD00`<br>`FDFF` |Persistent<br>Global<br>Variables|256 Bytes<br>4 Bytes/Entry<br>64 Entries |
|`FE00`<br>`FFFF` |Reserved<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|

* New entries **grow towards larger address**.

## Instruction Set

**Variable-length** between **1 to 5 bytes**.

* First byte (Byte 0): **Opcode**.

* Byte 1 to 4: **Optional payload**.

## CPU Instructions

* **1 stack item** = **1 uint32_t** = 4 **bytes**

* All multi-byte operations are **Little-endian**

* `PUSHR` / `POPR` **Offset** is a **byte-addressed signed 16-bit integer**
	* Positive: Towards larger address / TOS

|Name|Inst.<br>Size|Opcode<br>Byte 0|Comment|Payload<br>Byte 1-4|
|:-:|:-:|:-:|:-:|:-:|
|`NOP`|1|`0`/`0x0` |Do nothing|None|
|`PUSHC`|3|`1`/`0x1` |Push a **16-bit** constant on stack|2 Bytes:<br>`CONST_LSB`<br>`CONST_MSB` |
|`PUSHI`|3|`2`/`0x2` |Read **4 Bytes** at `ADDR`<br>Push to stack as one **32-bit** number|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`PUSHR`|3|`3`/`0x3`|Read **4 Bytes** at **offset from FP**<br>Push to stack as one **32-bit** number|2 Bytes:<br>`OFFSET_LSB`<br>`OFFSET_MSB`|
|`POPI`|3|`4`/`0x4` |Pop one item off TOS<br>Write **4 bytes** to `ADDR`|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`POPR`|3|`5`/`0x5`|Pop one item off TOS<br>Write as **4 Bytes** at **offset from FP**|2 Bytes:<br>`OFFSET_LSB`<br>`OFFSET_MSB`|
|`BRZ`|3|`6`/`0x6` |Pop one item off TOS<br>If value is zero, jump to `ADDR` |2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`JMP`|3|`7`/`0x7` |Unconditional Jump|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`CALL`|3|`8`/`0x8` |Construct 32b value `frame_info`:<br>Top 16b `current_FP`,<br>Bottom 16b `return_addr (PC+3)`.<br>Push `frame_info` to TOS<br>Set **FP** to TOS<br>Jump to `ADDR`|2 Bytes:<br>`ADDR_LSB`<br>`ADDR_MSB`|
|`RET`|3|`9`/`0x9` |`return_value` on TOS<br>Pop `return_value` into temp location<br>Pop items off TOS until `SP == FP`<br>Pop `frame_info`, restore **FP** and **PC**.<br>Pop off `ARG_COUNT` items<br>Push `return_value` back on TOS<br>Resumes execution at PC|2 Bytes:<br>`ARG_COUNT`<br>`Reserved`|
|`HALT`|1|`10`/`0xa` |Stop execution|None|
|`VMVER`|3|`255`/`0xff`| VM Version Check<br>Abort if mismatch |2 Bytes:<br>`VM_VER`<br>`Reserved`|

## Binary Operator Instructions

Binary as in **involving two operands**.

* All **single-byte** instruction

* Pop **TWO** items off TOS

* Top item is right-hand-side, lower item is left-hand-side.

* Perform operation

* Push result back on TOS

|Name|Opcode<br>Byte 0|Comment|
|:--:|:--:|:--:|
|EQ|`32`/`0x20`|Equal|
|NOTEQ|`33`/`0x21`|Not equal|
|LT|`34`/`0x22`|Less than|
|LTE|`35`/`0x23`|Less than or equal|
|GT|`36`/`0x24`|Greater than|
|GTE|`37`/`0x25`|Greater than or equal|
|ADD|`38`/`0x26`|Add|
|SUB|`39`/`0x27`|Subtract|
|MULT|`40`/`0x28`|Multiply|
|DIV|`41`/`0x29`|Integer division|
|MOD|`42`/`0x2a`|Modulus|
|POW|`43`/`0x2b`|Power of|
|LSHIFT|`44`/`0x2c`|Logical left shift|
|RSHIFT|`45`/`0x2d`|Logical right shift|
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
|DELAY|`64`/`0x40`| **Delay**<br>Pop ONE item<br>Delay amount in **milliseconds**|
|KUP|`65`/`0x41`|**Release Key**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|KeyType\|KeyCode\|`|
|KDOWN|`66`/`0x42`| **Press Key**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|KeyType\|KeyCode\|`|
|MSCL|`67`/`0x43`| **Mouse Scroll**<br>Pop ONE item<br>Scroll number of lines|
|MMOV|`68`/`0x44`|**Mouse Move**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|X\|Y\|`|
|SWCF|`69`/`0x45`| **Switch Color Fill**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Red\|Green\|Blue\|`<br>Set ALL LED color to the RGB value|
|SWCC|`70`/`0x46`| **Switch Color Change**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|N\|Red\|Green\|Blue\|`<br>Set N-th switch to the RGB value<br>If N is 0, set current switch.|
|SWCR|`71`/`0x47`| **Switch Color Reset**<br>Pop ONE item<br>If value is 0, reset color of current key<br>If value is between 1 and 20, reset color of that key<br>If value is 99, reset color of all keys.|
|STR|`72`/`0x48`|**Type String**<br>Pop ONE item as `ADDR`<br>Print zero-terminated string at `ADDR`|None||
|STRLN|`73`/`0x49`|**Type Line**<br>Pop ONE item as `ADDR`<br>Print zero-terminated string at `ADDR`<br>**Press ENTER at end**|
|OLED_CUSR|`74`/`0x4a`|**Set OLED Cursor**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|X\|Y\|`|
|OLED_PRNT|`75`/`0x4b`|**OLED Print**<br>Pop ONE item as `ADDR`<br>Print zero-terminated string at `ADDR` to OLED|None|
|OLED_UPDE|`76`/`0x4c`|**OLED Update**|
|OLED_CLR|`77`/`0x4d`|**OLED Clear**|
|OLED_REST|`78`/`0x4e`| **OLED Restore**|
|OLED_LINE|`79`/`0x4f`|**OLED Draw Line**<br>Pop ONE item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|x1\|y1\|x2\|y2\|`<br>Draw single-pixel line in-between|
|OLED_RECT|`80`/`0x50`|**OLED Draw Rectangle**<br>Pop TWO items<br>First item:<br>`\|Unused\|Unused\|Unused\|Fill\|`<br>Second Item:<br>`\|x1\|y1\|x2\|y2\|`<br>Draw rectangle between two points<br>Fill if `fill` is non-zero|
|OLED_CIRC|`81`/`0x51`|**OLED Draw Circle**<br>Pop ONE item<br>`fill, radius, x, y`<br>Draw circle with `radius` at `(x,y)`<br>Fill if `fill` is non-zero|
|SWQC|`82`/`0x52`|**Clear switch event queue**|
|PREVP|`83`/`0x53`| **Previous profile**|
|NEXTP|`84`/`0x54`| **Next profile**|
|GOTOP|`85`/`0x55`| **Goto Profile**<br>Pop ONE item **`n`**<br>Go to **`n-th`** profile|
|SLEEP|`86`/`0x56`| **Sleep**<br>Put duckyPad to sleep<br>Terminates execution|

## Calling Convention

* Multiple arguments, one return value.
* Supports nested and recursive calls
* **TOS** grows towards **larger address**

### Stack Set-up

Outside function calls, FP points to **bottom of stack.**

||...|
|:--:|:--:|
||`32-bit data`|
||...|
|`FP ->`|Bottom (`F000`)|

When calling a function: **`foo(a, b, c)`**

* **Caller** pushes 32-bit arguments **right to left** to stack
	* Don't push if no args.

|||
|:--:|:--:|
||`a`|
||`b`|
||`c`|
||...|
|`FP ->`|Bottom (`F000`)|

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
||Bottom (`F000`)|

### Function Arguments

Once in function, callee does required calculations.

To reference arguments, **FP + Byte_Offset** is used.

* **Positive** offset towards **larger address / TOS**.
* **Negative** offset towards **smaller address / bottom of stack**.
* `FP - 4` points to **leftmost argument**
* `FP - 8` points to **second from left**, etc.
* Use `PUSHR + Offset` and `POPR + Offset` to read/write to arguments.

|||
|:--:|:--:|
||...|
||`func_data`|
|`FP ->`|`Prev_FP \| Return_addr`|
|`FP - 4`|`a`|
|`FP - 8`|`b`|
|`FP - 12`|`c`|
||...|
||Bottom (`F000`)|

### Stack Unwinding

At end of a function, `return_value` is on TOS.

|||
|:--:|:--:|
||`return_value`|
||`temp data (if any)`|
|`FP ->`|`Prev_FP \| Return_addr`|
|`FP - 4`|`a`|
|`FP - 8`|`b`|
|`FP - 12`|`c`|
||...|
||Bottom (`F000`)|

**Callee** executes `RET n` instruction, which:

* Pops off `return_value` into temp location
* Pop items off TOS **until SP = FP**
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
|`FP ->`|Bottom (`F000`)|


## TODO

new opcode values
new opcode names
calling convention
single stack
internal registers
PUSHC16 zero extension or sign extension?
PUSHI POPI make sure little endian
binOPs: Signed or unsigned?
RSHIFT: logical or arithmetic?
comparison instructions: signed or unsigned?

new OLED instruction names

generate PGV save flag on DSVM itself not compiler

watch out for unused function return value clogging up stack, discard if no assign? in compiler

one-byte duckyscript commands, rewrite upper byte lower byte to 2ndLSB and LSB.

## Changelog

* `VMVER` instruction: version number now on byte 1 (LSB)

* Adjusted starting address and entry offset for
	* User-defined Variables
	* PGVs
	* Reserved Variables

* Added 32-bit push constant
	* By combining `PUSH16`, `LSHIFT`, and `BITOR.

* Opcode New Values

variable instruction length
