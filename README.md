# DuckStack Bytecode Stack Machine

## Architecture

All 32 bit

* **Data Stack**

* **Call Stack**

* PC

* Frame Pointer
	* Points to the **memory address** of the **first pushed argument** on **data stack**?
	* When not in function call, points to **memory address** of **base of data stack**
	* Used to reference function arguments via an offset

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

## CPU Instructions

All reference to **"stack"** refers to **Data Stack**. Unless noted otherwise.

| Opcode<br>Name| Byte 0<br>Decimal | Byte 0<br>Hex |Comment | Byte 1| Byte 2|
|:-:|:-:|:-:|:-:|:-:|:-:|
| `NOP` |0|0x0 |Do nothing| | |
|`PUSHC16`|1|0x1 |Push a **16-bit** constant on stack| CONST_LSB | CONST_MSB |
|`PUSHI32`|2|0x2 |Read **4 Bytes** at `ADDR`<br>Push to stack as one **32-bit** number|ADDR_LSB |ADDR_MSB |
| `POP32` |3|0x3 |Pop one item off top of stack<br>Write **4 bytes** to ADDR|ADDR_LSB |ADDR_MSB |
| `BRZ` |4|0x4 |Pop one item off top of stack<br>If value is zero, jump to ADDR |ADDR_LSB |ADDR_MSB |
| `JMP` |5|0x5 |Unconditional Jump|ADDR_LSB |ADDR_MSB |
| `CALL`|6|0x6 |Jump to Subroutine<br>Push the **next instruction** (PC+3) to **call stack**<br>Then jump to ADDR |ADDR_LSB |ADDR_MSB |
| `RET` |7|0x7 |Return from Subroutine<br>Pop one item off **call stack**<br>Set PC to its value | | |
| `HALT`|8|0x8 |Stop execution| | |
| `VMVER`|255|0xFF| VM Version Check<br>Abort if mismath |VM VER||

## Binary Operator Instructions

Binary as in **involving two operands**.

All instructions here:

* Pop TWO items off arithmetic stack

* Topmost item is right-hand-side, lower item is left-hand-side.

* Perform operation

* Push result back on stack.

| Opcode<br>Name| Byte 0<br>Decimal | Byte 0<br>Hex |Comment |
|:--:|:--:|:--:|:--:|
|EQ |9|0x9 | Equal|
|NOTEQ|10 |0xa | Not equal|
|LT |11 |0xb | Less than|
| LTE |12 |0xc |Less than or equal|
|GT |13 |0xd | Greater than |
| GTE |14 |0xe | Greater than or equal|
| ADD |15 |0xf |Add |
| SUB |16 | 0x10 | Subtract |
| MULT|17 | 0x11 | Multiply |
| DIV |18 | 0x12 | Integer division |
| MOD |19 | 0x13 | Modulus |
| POW |20 | 0x14 | Power of |
|LSHIFT |21 | 0x15 |Logical left shift|
|RSHIFT |22 | 0x16 |Logical right shift |
|BITOR|23 | 0x17 |Bitwise OR|
|BITAND |24 | 0x18 |Bitwise AND |
| LOGIAND |25 | 0x19 |Logical AND |
|LOGIOR |26 | 0x1a |Logical OR|
| BITXOR | 51 | 0x33 | Bitwise XOR |


## TODO


## Changelog

* `VMVER` instruction: version number now on byte 1 (LSB)

* Adjusted starting address and entry offset for
	* User-defined Variables
	* PGVs
	* Reserved Variables

* Added 32-bit push constant
	* By combining `PUSH16`, `LSHIFT`, and `BITOR.