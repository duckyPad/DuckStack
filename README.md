# DuckStack Bytecode Stack Machine

## Architecture

**32-bit** variables and arithmetics.

**16-bit** addressing, 64KB max.

* Single **Data Stack**
* Program Counter (PC)
* Stack Pointer (SP)
* Frame Pointer (FP)

## Memory Map

Flat memory map

|Address|Purpose |Comment |
|:-:|:--:|:--:|
|`0000`<br>`EFFF` |Binary<br>Executable|60K Bytes  |
|`F000`<br>`F7FF` |Data Stack|2048 Bytes<br>4 Bytes/Entry<br>512 Entries|
|`F800`<br>`F9FF` |User-defined<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|
|`FA00`<br>`FBFF` |Unused|512 Bytes|
|`FC00`<br>`FCFF`|Internal<br>Registers|256 Bytes<br>4 Bytes/Entry<br>64 Entries|
|`FD00`<br>`FDFF` |Persistent<br>Global<br>Variables|256 Bytes<br>4 Bytes/Entry<br>64 Entries |
|`FE00`<br>`FFFF` |Reserved<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|

* New entries **grow towards larger address**.
* All user-defined variables are global scope

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
* Use `PUSHR32 + Offset` and `POPR32 + Offset` to read/write to arguments.

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
|`FP ->`|`Prev_FP \| Return_addr`|
|`FP - 4`|`a`|
|`FP - 8`|`b`|
|`FP - 12`|`c`|
||...|
||Bottom (`F000`)|

**Callee** pops `return_value` and `frame_info` into internal registers.

**FP** is no longer valid.

|||
|:--:|:--:|
||Empty|
||Empty|
||`a`|
||`b`|
||`c`|
||...|
||Bottom (`F000`)|

**Callee** pops off all arguments (if any).

|||
|:--:|:--:|
||Empty|
||Empty|
||Empty|
||Empty|
||Empty|
||...|
||Bottom (`F000`)|

**Callee** pushes `return_value` then `frame_info` back on stack.

|||
|:--:|:--:|
||`frame_info`|
||`return_value`|
||...|
||Bottom (`F000`)|

**Callee** executes `RET` instruction, which:

* Pops off `frame_info`
	* Loads `previous FP` into **Frame Pointer**
	* Loads `return address` into **PC**
* Resumes execution at PC

|||
|:--:|:--:|
||`return_val`|
||...|
|`FP ->`|Bottom (`F000`)|

* Return value on TOS for caller to use

## CPU Instructions

|Name| Opcode<br>Byte 0 |Comment | Byte 1| Byte 2|
|:-:|:-:|:-:|:-:|:-:|
| `NOP` |`0`/`0x0` |Do nothing| | |
|`PUSHC16`|`1`/`0x1` |Push a **16-bit** constant on stack| CONST_LSB | CONST_MSB |
|`PUSHI32`|`2`/`0x2` |Read **4 Bytes** at `ADDR`<br>Push to stack as one **32-bit** number|ADDR_LSB |ADDR_MSB |
|`PUSHR32`|`3`/`0x3`|Read **4 Bytes** at **offset from FP**<br>Push to stack as one **32-bit** number<br>Offset: Signed, **byte addressable**<br>Positive: Towards larger address / TOS|OFFSET_LSB|OFFSET_MSB|
| `POPI32` |`4`/`0x4` |Pop one item off TOS<br>Write **4 bytes** to `ADDR`|ADDR_LSB |ADDR_MSB |
|`POPR32`|`5`/`0x5`|Pop one item off TOS<br>Write as **4 Bytes** at **offset from FP**<br>Offset: Signed, **byte addressable**<br>Positive: Towards larger address / TOS|OFFSET_LSB|OFFSET_MSB|
| `BRZ` |`6`/`0x6` |Pop one item off TOS<br>If value is zero, jump to `ADDR` |ADDR_LSB |ADDR_MSB |
| `JMP` |`7`/`0x7` |Unconditional Jump|ADDR_LSB |ADDR_MSB |
| `CALL`|`8`/`0x8` |Construct 32b value `frame_info`:<br>Top 16b `current_FP`,<br>Low 16b `return_addr`.<br>Push `frame_info` to TOS<br>Set **FP** to TOS<br>Jump to `ADDR`|ADDR_LSB |ADDR_MSB |
| `RET` |`9`/`0x9` |Pops off `frame_info`<br>Restore FP<br>Restore PC|| |
| `HALT`|`10`/`0xa` |Stop execution| | |
| `VMVER`|`255`/`0xff`| VM Version Check<br>Abort if mismath |VM VER||


Reserved between 0 and 31 decimal.

## Binary Operator Instructions

Binary as in **involving two operands**.

All instructions here:

* Pop TWO items off arithmetic stack

* Topmost item is right-hand-side, lower item is left-hand-side.

* Perform operation

* Push result back on stack.

|Name|Opcode<br>Byte 0|Comment|Byte 1|Byte2|
|:--:|:--:|:--:|:--:|:--:|
|EQ|`32`/`0x20`|Equal|||
|NOTEQ|`33`/`0x21`|Not equal|||
|LT|`34`/`0x22`|Less than|||
|LTE|`35`/`0x23`|Less than or equal|||
|GT|`36`/`0x24`|Greater than|||
|GTE|`37`/`0x25`|Greater than or equal|||
|ADD|`38`/`0x26`|Add|||
|SUB|`39`/`0x27`|Subtract|||
|MULT|`40`/`0x28`|Multiply|||
|DIV|`41`/`0x29`|Integer division|||
|MOD|`42`/`0x2a`|Modulus|||
|POW|`43`/`0x2b`|Power of|||
|LSHIFT|`44`/`0x2c`|Logical left shift|||
|RSHIFT|`45`/`0x2d`|Logical right shift|||
|BITOR|`46`/`0x2e`|Bitwise OR|||
|BITAND|`47`/`0x2f`|Bitwise AND|||
|LOGIAND|`48`/`0x30`|Logical AND|||
|LOGIOR|`49`/`0x31`|Logical OR|||
|BITXOR|`50`/`0x32`|Bitwise XOR|||

Reserved between 32 and 63 decimal.

# duckyScript Command Instructions

|Name| Opcode<br>Byte 0|Comment | Byte 1| Byte 2|
|:-------:|:----:|:----------:|:---------:|:---------:|
|DELAY|`64`/`0x40`| Pop one item off TOS<br>Delay the amount in milliseconds| | |
|KUP|`65`/`0x41`|**Release Key**<br>Pop ONE item<br>Upper byte: KEYTYPE<br>Lower byte: KEYCODE |||
|KDOWN|`66`/`0x42`| **Press Key**<br>Pop ONE item<br>Upper byte: KEYTYPE<br>Lower byte: KEYCODE |||
|MSCL|`67`/`0x43`| **Mouse Scroll**<br>Pop ONE item<br>Scroll number of lines || |
|MMOV|`68`/`0x44`|**Mouse Move**<br>Pop TWO items<br>Move X and Y|||
|SWCF|`69`/`0x45`| **Switch Color Fill**<br>Pop THREE items<br>Red, Green, Blue<br>Set ALL LED color to the RGB value | | |
|SWCC|`70`/`0x46`| **Switch Color Change**<br>Pop FOUR items<br>N, Red, Green, Blue<br>Set N-th switch to the RGB value<br>If N is 0, set current switch. | | |
|SWCR|`71`/`0x47`| **Switch Color Reset**<br>Pop one item off TOS<br>If value is 0, reset color of current key<br>If value is between 1 and 20, reset color of that key<br>If value is 99, reset color of all keys | | |
|STR|`72`/`0x48`|Print zero-terminated string at ADDR |ADDR_LSB |ADDR_MSB |
|STRLN|`73`/`0x49`|Same as above, presses ENTER at end |ADDR_LSB | ADDR_MSB |
|OLC|`74`/`0x4a`|**OLED_CURSOR**<br>Pop TWO items<br>X and Y<br>| | |
|OLP|`75`/`0x4b`|Print zero-terminated string at ADDR to OLED |ADDR_LSB |ADDR_MSB |
|OLU|`76`/`0x4c`|**OLED_UPDATE** | | |
|OLB|`77`/`0x4d`|**OLED_CLEAR**| | |
|OLR|`78`/`0x4e`| **OLED_RESTORE** | | |
|BCLR|`79`/`0x4f`|Clear switch event queue | | |
|PREVP|`80`/`0x50`| Previous profile | | |
|NEXTP|`81`/`0x51`| Next profile | | |
|GOTOP|`82`/`0x52`| Pop one item<br>Go to profile of its value | | |
|SLEEP|`83`/`0x53`| Put duckyPad to sleep<br>Terminates execution| | |
|OLED_LINE|`84`/`0x54`|OLED Draw Line<br>Pop FOUR items<br>`x1, y1, x2, y2`<br>Draw single-pixel line inbetween |||
|OLED_RECT|`85`/`0x55`|OLED Draw Rectangle<br>Pop FIVE items<br>`fill, x1, y1, x2, y2`<br>Draw rectangle between two points<br>Fill if `fill` is non-zero|||
|OLED_CIRC|`86`/`0x56`|OLED Draw Circle<br>Pop FOUR items<br>`fill, radius, x, y`<br>Draw circle with `radius` at `(x,y)`<br>Fill if `fill` is non-zero|||

Reserved between 64 and 95 decimal.

## TODO

new opcode values
new opcode names
calling convention
single stack

## Changelog

* `VMVER` instruction: version number now on byte 1 (LSB)

* Adjusted starting address and entry offset for
	* User-defined Variables
	* PGVs
	* Reserved Variables

* Added 32-bit push constant
	* By combining `PUSH16`, `LSHIFT`, and `BITOR.

* Opcode New Values