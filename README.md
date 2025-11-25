# DuckStack Bytecode Stack Machine

## Architecture

16-bit addressing, 64KB max.

32-bit variables and arithmetics.

* **Data Stack**
* **Call Stack**
* PC
* Frame Pointer

## Memory Map

Flat memory map

|Addr|Purpose|Comment|
|:---:|:---:|:---:|
|`0000`<br>`EFFF`|Binary<br>Executable|60K Bytes|
|`F000`<br>`F7FF`|Data<br>Stack|2048 Bytes<br>4 Bytes Per Entry<br>512 Entries|
|`F800`<br>`F9FF`|Call<br>Stack|512 Bytes<br>4 Bytes Per Entry<br>128 Entries|
|`FA00`<br>`FBFF`|User-defined<br>Variables|512 Bytes<br>4 Bytes Per Entry<br>128 Entries|
|`FC00`<br>`FD7F`|Unused|384 Bytes|
|`FD80`<br>`FDFF`|Persistent<br>Global<br>Variables|128 Bytes<br>4 Bytes Per Entry<br>32 Entries|
|`FE00`<br>`FFFF`|Reserved<br>Variables|512 Bytes<br>4 Bytes Per Entry<br>128 Entries|

New entries **grow towards larger address**.

## Calling Convention

* Multiple arguments, one return value.
* Supports nested and recursive calls

### Stack Set-up

When not in function calls, FP points to **bottom of data stack.**

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
||...|
||`32-bit data`|
||...|
|`FP ->`|Bottom (`F000`)|

</td><td>

||
|:--:|
|...|
|Bottom (`F800`)|

</td></tr> </table>

When calling a function: **`foo(a, b, c)`**

* Caller pushes 32-bit arguments **right to left** onto **data stack**
	* If no arguments, push one dummy value?

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
||`a`|
||`b`|
||`c`|
||...|
|`FP ->`|Bottom (`F000`)|

</td><td>

||
|:--:|
|...|
|Bottom (`F800`)|

</td></tr> </table>

Caller then executes `CALL` instruction, which:

* Pushes **current FP** to **call stack**
* Pushes **next instruction (PC+3)** to **call stack**
* Sets **FP** to **top of data stack**
* Jumps to the function address

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
|`FP ->`|`a`|
||`b`|
||`c`|
||...|
||Bottom (`F000`)|

</td><td>

||
|:--:|
|`Return_Addr = PC+3`|
|`Prev_FP = 0xF000`|
|...|
|Bottom (`F800`)|

</td></tr> </table>

### Arguments and Local Variables

Once in function, callee does required calculations.

To reference arguments (and local variables in the future?), **FP + Byte_Offset** is used.

* Positive offset towards top of stack.
* Negative offset towards bottom of stack.
* `FP` points to **leftmost argument**
* `FP - 4` points to **second from left**, etc.
* Use `PUSHL + Offset` and `PUSHL + Offset` read/write to arguments/locals.

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
||...|
||`func_data`|
|`FP ->`|`a`|
|`FP - 4`|`b`|
|`FP - 8`|`c`|
||...|
||Bottom (`F000`)|

</td><td>

||
|:--:|
|`Return_Addr = PC+3`|
|`Prev_FP = 0xF000`|
|...|
|Bottom (`F800`)|

</td></tr> </table>

### Stack Unwinding

At end of a function, **return value** is on top of **data stack**.

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
||`return_val`|
|`FP ->`|`a`|
|`FP - 4`|`b`|
|`FP - 8`|`c`|
||...|
||Bottom (`F000`)|

</td><td>

||
|:--:|
|`Return_Addr = PC+3`|
|`Prev_FP = 0xF000`|
|...|
|Bottom (`F800`)|

</td></tr> </table>

Callee writes the return value to the **rightmost argument slot** (lowest on stack) using `POPL` instruction.

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
||`return_val`|
|`FP ->`|`a`|
|`FP - 4`|`b`|
|`FP - 8`|`return_val`|
||...|
||Bottom (`F000`)|

</td><td>

||
|:--:|
|`Return_Addr = PC+3`|
|`Prev_FP = 0xF000`|
|...|
|Bottom (`F800`)|

</td></tr> </table>

Callee then pops off everything until the **exactly one item** (return value) is on top.

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
|`FP - 8`|`return_val`|
||...|
||Bottom (`F000`)|

</td><td>

||
|:--:|
|`Return_Addr = PC+3`|
|`Prev_FP = 0xF000`|
|...|
|Bottom (`F800`)|

</td></tr> </table>

Callee executes `RET` instruction, which:

* Pops off **return address (PC+3)** off **call stack** into **PC**
* Pops off **Previous FP** off **call stack** into **Frame Pointer**
* Resumes execution at PC
* Return value on top of stack

<table>
<tr><th>Data Stack </th><th>Call Stack</th></tr>
<tr><td>

|||
|:--:|:--:|
||`return_val`|
||...|
|`FP ->`|Bottom (`F000`)|

</td><td>

||
|:--:|
|...|
|Bottom (`F800`)|

</td></tr> </table>

## CPU Instructions

All reference to **"stack"** refers to **Data Stack**. Unless noted otherwise.

|Name| Opcode<br>Byte 0 |Comment | Byte 1| Byte 2|
|:-:|:-:|:-:|:-:|:-:|
| `NOP` |`0`/`0x0` |Do nothing| | |
|`PUSHC16`|`1`/`0x1` |Push a **16-bit** constant on stack| CONST_LSB | CONST_MSB |
|`PUSHI32`|`2`/`0x2` |Read **4 Bytes** at `ADDR`<br>Push to stack as one **32-bit** number|ADDR_LSB |ADDR_MSB |
| `POP32` |`3`/`0x3` |Pop one item off top of stack<br>Write **4 bytes** to ADDR|ADDR_LSB |ADDR_MSB |
| `BRZ` |`4`/`0x4` |Pop one item off top of stack<br>If value is zero, jump to ADDR |ADDR_LSB |ADDR_MSB |
| `JMP` |`5`/`0x5` |Unconditional Jump|ADDR_LSB |ADDR_MSB |
| `CALL`|`6`/`0x6` |Jump to Subroutine<br>Pushes **current FP** to **call stack**<br>Push the **next instruction** (PC+3) to **call stack**<br>Jump to ADDR |ADDR_LSB |ADDR_MSB |
| `RET` |`7`/`0x7` |Return from Subroutine<br>Pop off return address off **call stack** into PC<br>Pop off **Previous FP** off **call stack** into **Frame Pointer**<br>Resume execution at PC<br>Return value on top of **data stack**| | |
| `HALT`|`8`/`0x8` |Stop execution| | |
|`PUSHL32`|`9`/`0x9`|Read **4 Bytes** at **offset from frame pointer**<br>Push to stack as one **32-bit** number|OFFSET_LSB|OFFSET_MSB|
|`POPL32`|`10`/`0xa`|Pop one item off top of stack<br>Write as **4 Bytes** at **offset from frame pointer**|OFFSET_LSB|OFFSET_MSB|
| `VMVER`|`255`/`0xFF`| VM Version Check<br>Abort if mismath |VM VER||

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
|DELAY|`64`/`0x40`| Pop one item off top of stack<br>Delay the amount in milliseconds| | |
|KUP|`65`/`0x41`|**Release Key**<br>Pop ONE item<br>Upper byte: KEYTYPE<br>Lower byte: KEYCODE |||
|KDOWN|`66`/`0x42`| **Press Key**<br>Pop ONE item<br>Upper byte: KEYTYPE<br>Lower byte: KEYCODE |||
|MSCL|`67`/`0x43`| **Mouse Scroll**<br>Pop ONE item<br>Scroll number of lines || |
|MMOV|`68`/`0x44`|**Mouse Move**<br>Pop TWO items<br>Move X and Y|||
|SWCF|`69`/`0x45`| **Switch Color Fill**<br>Pop THREE items<br>Red, Green, Blue<br>Set ALL LED color to the RGB value | | |
|SWCC|`70`/`0x46`| **Switch Color Change**<br>Pop FOUR items<br>N, Red, Green, Blue<br>Set N-th switch to the RGB value<br>If N is 0, set current switch. | | |
|SWCR|`71`/`0x47`| **Switch Color Reset**<br>Pop one item off top of stack<br>If value is 0, reset color of current key<br>If value is between 1 and 20, reset color of that key<br>If value is 99, reset color of all keys | | |
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

* Figure out details of PUSHL and POPL instructions

## Changelog

* `VMVER` instruction: version number now on byte 1 (LSB)

* Adjusted starting address and entry offset for
	* User-defined Variables
	* PGVs
	* Reserved Variables

* Added 32-bit push constant
	* By combining `PUSH16`, `LSHIFT`, and `BITOR.

* Opcode New Values