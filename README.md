# DuckStack

## Architecture

* **Data Stack**: 32 Bit wide

* **Call Stack**: 16 Bit wide

* PC: 32 bit

* Frame Pointer: 32 bit, points to an address on data stack

## Memory Map

Flat memory map

|Addr|Purpose|Comment|
|:---:|:---:|:---:|
|`0000`<br>`EFFF`|Binary<br>Executable|60K Bytes|
|`F000`<br>`F7FF`|Data<br>Stack|2048 Bytes<br>4 Bytes Per Entry<br>512 Entries|
|`F800`<br>`F9FF`|Call<br>Stack|512 Bytes<br>2 Bytes Per Entry<br>256 Entries|
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

## TODO

* Endianness of PUSHI32 and POP32

* Consistent Endianness

## Changelog

* `VMVER` instruction: version number now on byte 1 (LSB)

* Adjusted starting address and entry offset for
	* User-defined Variables
	* PGVs
	* Reserved Variables

