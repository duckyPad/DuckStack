# duckStack Bytecode VM


expand arithmetics stack to 32 bit wide
keep call stack at 16 bit

change var_buf to 32 bit

32 bit PUSHC:
push MSB, left shift, push LSB



-----------------



For use in low-power MCUs to perform HID actions (macro scripting).

STM32, ESP32, RISC-V, etc.

simple, lightweight, but still somewhat general-purpose.


base on existing VM, add 32-bit arithmetics (stack width).


## Memory Map

general purpose RAM, and reserved variables near the end. flat address, although use two arrays in the VM, one for binary executible and other for RAM.


Flat 64KB address, byte addressable.

Execution starts at 0x0.

0x0 is **beginning** of memory map
0xffff **end** of memory map

purposefully not using "top" and "bottom" because it's confusing!

Top 


## Stack

Data Stack and Call Stack.

Also PC, Stack pointer, Frame pointer

32-bit stack width

function arguments and return values go on data stack.

## Instructions

Variable length, 1, 3, or 5 bytes.

1-byte instruction: Just the opcode itself

3-Byte instruction: Opcode + 2 bytes (as 2 u8 or 1 u16)

5-Byte instruction: Opcode + 4 bytes (as 4 u8, 2 u16, or 1 u32)

## Opcodes