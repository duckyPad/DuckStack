# DuckStack Bytecode Virtual Machine

DuckStack is a simple **stack-based bytecode VM** for executing compiled **duckyScript** binaries.

[duckyPad](https://dekunukem.github.io/duckyPad-Pro/doc/landing.html) uses it for HID macro scripting.

## ⚠️⚠️ UNDER ACTIVE DEVELOPMENT ⚠️⚠️

This VM is **under developement** and specs may change at any time!

Public beta is expected **Jan 2026**.

## Features

* 32-Bit Data Path, 16-bit Addressing.
* Flexible Executable & Stack Region
* Variable-length Instructions
* Function Arguments, Locals, & Recursions.
* HID-specific Instructions

## Table of Contents

- [How to Use](#how-to-use)
    - [Compile](#compile)
    - [Execute](#execute)
- [Architecture Overview](#architecture-overview)
    - [Memory Map](#memory-map)
- [Instruction Set](#instruction-set)
    - [CPU Instructions](#cpu-instructions)
    - [Binary Operators](#binary-operators)
    - [Unary Operators](#unary-operators)
    - [duckyScript Commands](#duckyscript-commands)
- [Calling Convention](#calling-convention)
    - [Stack Set-up](#stack-set-up)
    - [Arguments / Locals](#arguments--locals)
    - [Stack Unwinding](#stack-unwinding)
- [Questions or Comments?](#questions-or-comments)

## How to Use

### Compile

* Download / clone this repo
* Prepare a duckyScript source file `test.txt`
	* Learn More: [Writing duckyScript](https://dekunukem.github.io/duckyPad-Pro/doc/duckyscript_info.html)
```
VAR foo = 5 * 8 + 2
STRING The answer is: $foo!
```
* In `ds_compiler` directory, run:

`python3 ./dsvm_make_bytecode.py test.txt test.dsb`

* Output file can have any extension.
	* I like to use `.dsb` for duckyScript Binary

Output:

```
--------- Assembly Listing, Resolved: ---------
0    VMVER     2     0x2
3    PUSHC16   5     0x5           ;VAR value = 5 * 8 + 2
6    PUSHC16   8     0x8           ;VAR value = 5 * 8 + 2
9    MULT
10   PUSHC16   2     0x2           ;VAR value = 5 * 8 + 2
13   ADD
14   POPI      63488 0xf800        ;VAR value = 5 * 8 + 2
17   PUSHC16   22    0x16          ;STRING The answer is: $value!
20   STR                           ;STRING The answer is: $value!
21   HALT
22   DATA: b'The answer is: \x1f\x00\xf8\x1f!\x00'
----------------------------
Wrote 43 bytes to 'test.dsb'
```

### Execute

An VM written in C is provided.

It is similar to what's used in real duckyPads, but uses dummy values for reserved variables and placeholders for hardware commands.

----

In `ds_c_vm` folder, run `python3 ./compile.py` to compile the source. (Or write your own Makefile)

Run the VM: `./main test.dsb`

Output:

```
>>>>> STRING: The answer is: 42!
Execution Complete
```

Set `PRINT_DEBUG` to 1 in `main.h` for execution and stack trace.

## Architecture Overview

duckStack uses **32-bit** variables, arithmetics, and stack width.

Addressing is **16-bit**, executable 64KB max.

* Single **Data Stack**
* Program Counter (PC)
	* 16-bit byte-addressed
* Stack Pointer (SP)
	* 16-bit byte-addressed
	* Points to **the next free stack slot**
* Frame Pointer (FP)
	* Points to current function base frame

### Memory Map

* Flat memory map
* Byte-addressed

|Address|Purpose|Size|Comment|
|:-:|:--:|:--:|:--:|
|`0000`<br>`F7FF` |Shared<br>**Executable**<br>and **Stack**|63488 Bytes|See Notes Below|
|`F800`<br>`F9FF` |User-defined<br>Global<br>Variables|512 Bytes<br>4 Bytes/Entry<br>128 Entries|ZI Data|
|`FA00`<br>`FAFF` |Scratch<br>Memory|256 Bytes|General-purpose<br>User-accessible|
|`FB00`<br>`FCFF` |Unused|512 Bytes||
|`FD00`<br>`FDFF` |Persistent<br>Global<br>Variables|256 Bytes<br>4 Bytes/Entry<br>64 Entries |Non-volatile Data<br>Saved on SD card|
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
* All multi-byte operations are **Little-endian**

### CPU Instructions

* **1 stack item** = 4 **bytes**

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
|`PEEK8`|1|`12`/`0xc` |Pop **ONE** item off TOS as `ADDR`<br>`ADDR <= 0xFAFF`<br>Read **ONE byte** at `ADDR`<br>Push on stack|None|
|`POKE8`|1|`13`/`0xd` |Pop **TWO** item off TOS<br>First `VAL`, then `ADDR`.<br>`ADDR <= 0xFAFF`<br>Write **ONE** byte (LSB of `VAL`) to `ADDR`|None|
|`PUSH0`|1|`14`/`0xe` |Push `0` to TOS|None|
|`DROP`|1|`15`/`0xf` |Discard **ONE** item off TOS|None|
|`DUP`|1|`16`/`0x10` |**Duplicate the item** on TOS|None|
|`RANDINT`|1|`17`/`0x11` |Pop **TWO** item off TOS<br>First `Upper`, then `Lower`.<br>Push a random number inbetween (**inclusive**) on TOS|None|
|`VMVER`|3|`255`/`0xff`| VM Version Check<br>Abort if mismatch |2 Bytes:<br>`VM_VER`<br>`Reserved`|

### Binary Operators

Binary as in **involving two operands**.

* All **single-byte** instructions
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
|`EQ`|`32`/`0x20`|Equal|
|`NOTEQ`|`33`/`0x21`|Not Equal|
|`LT`|`34`/`0x22`|⚠️Less Than|
|`LTE`|`35`/`0x23`|⚠️Less Than or Equal|
|`GT`|`36`/`0x24`|⚠️Greater Than|
|`GTE`|`37`/`0x25`|⚠️Greater Than or Equal|
|`ADD`|`38`/`0x26`|Add|
|`SUB`|`39`/`0x27`|Subtract|
|`MULT`|`40`/`0x28`|Multiply|
|`DIV`|`41`/`0x29`|⚠️Integer Division|
|`MOD`|`42`/`0x2a`|⚠️Modulus|
|`POW`|`43`/`0x2b`|Power of|
|`LSHIFT`|`44`/`0x2c`|Left shift|
|`RSHIFT`|`45`/`0x2d`|⚠️Right shift<br>Signed Mode: Arithmetic (sign-extend)<br>Unsigned Mode: Logical (0-extend)|
|`BITOR`|`46`/`0x2e`|Bitwise OR|
|`BITXOR`|`47`/`0x2f`|Bitwise XOR|
|`BITAND`|`48`/`0x30`|Bitwise AND|
|`LOGIAND`|`49`/`0x31`|Logical AND|
|`LOGIOR`|`50`/`0x32`|Logical OR|

### Unary Operators

* All **single-byte** instruction
* Pop **ONE** items off TOS
* Perform operation
* Push result back on TOS

|Name|Opcode<br>Byte 0|Comment|
|:--:|:--:|:--:|
|`BITINV`|`55`/`0x37`|Bitwise Invert|
|`LOGINOT`|`56`/`0x38`|Logical NOT|
|`USUB`|`57`/`0x39`|Unary Minus|

### duckyScript Commands

* All **single-byte** instruction

|Name|Opcode<br>Byte 0|Comment|
|:-------:|:----------:|:---------:|
|`DELAY`|`64`/`0x40`| **Delay**<br>Pop **ONE** item<br>Delay amount in **milliseconds**|
|`KDOWN`|`65`/`0x41`| **Press Key**<br>Pop **ONE** item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|KeyType\|KeyCode\|`|
|`KUP`|`66`/`0x42`|**Release Key**<br>Pop **ONE** item<br>`\|MSB\|B2\|B1\|LSB`<br>`\|Unused\|Unused\|KeyType\|KeyCode\|`|
|`MSCL`|`67`/`0x43`| **Mouse Scroll**<br>Pop **ONE** item<br>Scroll number of lines|
|`MMOV`|`68`/`0x44`|**Mouse Move**<br>Pop **TWO** items: `x` then `y`|
|`SWCF`|`69`/`0x45`| **Switch Color Fill**<br>Pop **THREE** items<br>`Red, Green, Blue`<br>Set ALL LED color to the RGB value|
|`SWCC`|`70`/`0x46`| **Switch Color Change**<br>Pop **FOUR** item<br>`N, Red, Green, Blue`<br>Set N-th switch to the RGB value<br>If N is 0, set current switch.|
|`SWCR`|`71`/`0x47`| **Switch Color Reset**<br>Pop **ONE** item<br>If value is 0, reset color of current key<br>If value is between 1 and 20, reset color of that key<br>If value is 99, reset color of all keys.|
|`STR`|`72`/`0x48`|**Type String**<br>Pop **ONE** item as `ADDR`<br>Print zero-terminated<br>string at `ADDR`|None||
|`STRLN`|`73`/`0x49`|**Type Line**<br>Pop **ONE** item as `ADDR`<br>Print zero-terminated<br>string at `ADDR`<br>**Press ENTER at end**|
|`OLED_CUSR`|`74`/`0x4a`|**OLED Set Cursor**<br>Pop **TWO** items: `x` then `y`||
|`OLED_PRNT`|`75`/`0x4b`|**OLED Print**<br>Pop **ONE** item as `ADDR`<br>Print zero-terminated<br>string at `ADDR` to OLED|None|
|`OLED_UPDE`|`76`/`0x4c`|**OLED Update**|
|`OLED_CLR`|`77`/`0x4d`|**OLED Clear**|
|`OLED_REST`|`78`/`0x4e`| **OLED Restore**|
|`OLED_LINE`|`79`/`0x4f`|**OLED Draw Line**<br>Pop **FOUR** items<br>`x1, y1, x2, y2`<br>Draw single-pixel line in-between|
|`OLED_RECT`|`80`/`0x50`|**OLED Draw Rectangle**<br>Pop **FIVE** items<br>`fill, x1, y1, x2, y2`<br>Draw rectangle between two points<br>Fill if `fill` is non-zero|
|`OLED_CIRC`|`81`/`0x51`|**OLED Draw Circle**<br>Pop **FOUR** items<br>`fill, radius, x, y`<br>Draw circle with `radius` at `(x,y)`<br>Fill if `fill` is non-zero|
|`BCLR`|`82`/`0x52`|**Clear switch event queue**|
|`SKIPP`|`83`/`0x53`| **Skip Profile**<br>Pop **ONE** item as `n`<br>Increment/Decrement `n`<br>profiles from the current one|
|`GOTOP`|`84`/`0x55`| **Goto Profile**<br>Pop **ONE** item as `ADDR`<br>Retrieve zero-terminated string at `ADDR`<br>If it is a **valid integer `n`** **AND maps to existing profile**<br>Go to `n`th profile.<br>Otherwise jump to the profile with the string name|
|`SLEEP`|`85`/`0x56`| **Sleep**<br>Put duckyPad to sleep<br>Terminates execution|
|`RANDCHR`|`86`/`0x57`| **Random Character**<br>See notes below.|

#### RANDCHR Instruction

* Pops **ONE** item (4 bytes)
	* LSB: `char_type`
	* Second Byte: `stream_type`.
	* BOTH are **bitmasks**.
* `char_type`
	* Bit 0: Letter Lowercase (a-z)
	* Bit 1: Letter Uppercase (A-Z)
	* Bit 2: Digits (0-9)
	* Bit 3: Symbols (\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\})
* `stream_type`
	* Bit 0: Type via Keyboard
	* Bit 1: Print on OLED (Don't forget `OLED_UPDATE`)

## String Encoding

The following commands involves user-provided strings:

* `STRING`
* `STRINGLN`
* `OLED_PRINT`
* `GOTO_PROFILE`

Strings are **zero-terminated** and appended at the **end of the binary executable**.

The **starting address** of a string is **pushed onto stack** before calling one of those commands, who pops off the address and fetch the string there.

Identical strings are deduplicated and share the same address.

```
STRING Hello World!
STRINGLN Hello World!
OLED_PRINT Hi there!
```
```
0    VMVER     2     0x2
3    PUSHC16   16    0x10          ;STRING Hello World!
6    STR                           ;STRING Hello World!
7    PUSHC16   16    0x10          ;STRINGLN Hello World!
10   STRLN                         ;STRINGLN Hello World!
11   PUSHC16   29    0x1d          ;OLED_PRINT Hi there!
14   OLED_PRNT                     ;OLED_PRINT Hi there!
15   HALT
16   DATA: b'Hello World!\x00'
29   DATA: b'Hi there!\x00'
```

-----------

When user **prints an variable**, its info is embedded into the string between **two separator bytes**.

* `0x1f` for **Global Variables**
	* Contains: **Little-endian** memory address
* `0x1e` for **Local Variables and Arguments inside functions**
	* Contains: **FP-Relative Offset**
```
VAR foo = 5
STRING The number is: $foo!
```
```
0    VMVER     2     0x2
3    PUSHC16   5     0x5           ;VAR foo = 5
6    POPI      63488 0xf800        ;VAR foo = 5
9    PUSHC16   14    0xe           ;STRING The number is: $foo!
12   STR                           ;STRING The number is: $foo!
13   HALT
14   DATA: b'The number is: \x1f\x00\xf8\x1f!\x00'
```

When VM encounters the separator byte, it reads the value from **memory address** or **FP-relative** and inserts it into the string.

## Run-time Exceptions

Exceptions such as Division-by-Zero, Stack Over/Underflow, etc, result in immediate termination of the VM execution.

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

### Arguments / Locals

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

## Questions or Comments?

Please feel free to [open an issue](https://github.com/dekuNukem/duckstack/issues), ask in the [official duckyPad discord](https://discord.gg/4sJCBx5), or email `dekuNukem`@`gmail`.`com`!

## To mention in doc

* built-in functions
	* POKE8() and PEEK8()
	* RANDCHR(chr_info)
* Mild optimisations, smaller code size.
* `THEN` no longer required
* AugAssign operator `+=, -=, etc`
* RANDINT() function