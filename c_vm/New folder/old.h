
#ifndef ds_vm_h
#define ds_vm_h

#include <stdint.h>
#include <string.h>

#define OP_NOP 0
#define OP_PUSHC16 1
#define OP_PUSHI32 2
#define OP_POP 3
#define OP_BRZ 4
#define OP_JMP 5
#define OP_CALL 6
#define OP_RET 7
#define OP_HALT 8
#define OP_EQ 9
#define OP_NOTEQ 10
#define OP_LT 11
#define OP_LTE 12
#define OP_GT 13
#define OP_GTE 14
#define OP_ADD 15
#define OP_SUB 16
#define OP_MULT 17
#define OP_DIV 18
#define OP_MOD 19
#define OP_POW 20
#define OP_LSHIFT 21
#define OP_RSHIFT 22
#define OP_BITOR 23
#define OP_BITAND 24
#define OP_LOGIAND 25
#define OP_LOGIOR 26
#define OP_DELAY 27
#define OP_KUP 28
#define OP_KDOWN 29
#define OP_MSCL 30
#define OP_MMOV 31
#define OP_SWCF 32
#define OP_SWCC 33
#define OP_SWCR 34
#define OP_STR 35
#define OP_STRLN 36
// #define OP_EMUK 37
#define OP_OLC 38
#define OP_OLP 39
#define OP_OLU 40
#define OP_OLB 41
#define OP_OLR 42
#define OP_BCLR 43
#define OP_PREVP 44
#define OP_NEXTP 45
#define OP_GOTOP 46
#define OP_SLEEP 47

#define OP_OLED_LINE 48
#define OP_OLED_RECT 49
#define OP_OLED_CIRCLE 50

#define OP_BITXOR 51


#define OP_VMINFO 255

//--------------

#define EXE_BIN_START_ADDRESS 0x0
#define EXE_BIN_END_ADDRESS_INCLUSIVE 0xefff

#define DATA_STACK_START_ADDRESS 0xf000
#define DATA_STACK_BYTE_WIDTH 4
#define DATA_STACK_END_ADDRESS_INCLUSIVE 0xf7ff
#define DATA_STACK_SIZE_BYTES (DATA_STACK_END_ADDRESS_INCLUSIVE-DATA_STACK_START_ADDRESS+1)

#define CALL_STACK_START_ADDRESS 0xf800
#define CALL_STACK_BYTE_WIDTH 4
#define CALL_STACK_END_ADDRESS_INCLUSIVE 0xf9ff
#define CALL_STACK_SIZE_BYTES (CALL_STACK_END_ADDRESS_INCLUSIVE-CALL_STACK_START_ADDRESS+1)

#define USER_VAR_START_ADDRESS 0xFA00
#define USER_VAR_BYTE_WIDTH 4
#define USER_VAR_END_ADDRESS_INCLUSIVE 0xFBFF

#define PGV_COUNT 32
#define PGV_START_ADDRESS 0xFD80
#define PGV_BYTE_WIDTH 4
#define PGV_END_ADDRESS_INCLUSIVE 0xFDFF

#define INTERAL_VAR_START_ADDRESS 0xFE00
#define INTERAL_VAR_BYTE_WIDTH 4
#define INTERAL_VAR_END_ADDRESS_INCLUSIVE 0xFFFF

// ----------
#define INSTRUCTION_SIZE_BYTES 3
#define BIN_BUF_SIZE 0xffff
// ----------

#define EXE_OK 0

#define EXE_ACTION_SLEEP 1
#define EXE_ACTION_PREV_PROFILE 2
#define EXE_ACTION_NEXT_PROFILE 3
#define EXE_ACTION_GOTO_PROFILE 4

#define EXE_HALT 10
#define EXE_ABORTED 11

#define EXE_ERROR_CODE_START 20
#define EXE_UNKNOWN_OPCODE EXE_ERROR_CODE_START
#define EXE_DSB_INCOMPATIBLE_VERSION (EXE_ERROR_CODE_START + 1)
#define EXE_DSB_FOPEN_FAIL (EXE_ERROR_CODE_START + 2)
#define EXE_DSB_FREAD_ERROR (EXE_ERROR_CODE_START + 3)
#define EXE_STACK_OVERFLOW (EXE_ERROR_CODE_START + 4)
#define EXE_STACK_UNDERFLOW (EXE_ERROR_CODE_START + 5)
#define EXE_DIVISION_BY_ZERO (EXE_ERROR_CODE_START + 6)

typedef struct
{
  uint8_t result;
  uint16_t next_pc;
  uint8_t data;
  uint8_t epilogue_actions;
} ds3_exe_result;

#define DEFAULT_CMD_DELAY_MS 20
#define DEFAULT_CHAR_DELAY_MS 20

#define EPILOGUE_SAVE_LOOP_STATE 0x1
#define EPILOGUE_SAVE_COLOR_STATE 0x2
#define EPILOGUE_NEED_OLED_RESTORE 0x4
#define EPILOGUE_DONT_AUTO_REPEAT 0x8
#define EPILOGUE_SAVE_GV 0x10

#define MAX(a, b) ((a) > (b) ? (a) : (b))

extern uint8_t bin_buf[BIN_BUF_SIZE];
extern uint8_t allow_abort;
extern uint8_t kb_led_status;
extern uint32_t pgv_buf[PGV_COUNT];

extern uint8_t str_print_format;
extern uint8_t str_print_padding;

void run_dsb(ds3_exe_result* er, uint8_t this_key_id, char* dsb_path, uint8_t is_cached, uint8_t* dsb_cache);

#define STR_PRINT_FORMAT_DEC_UNSIGNED    0
#define STR_PRINT_FORMAT_DEC_SIGNED      1
#define STR_PRINT_FORMAT_HEX_LOWER_CASE  2
#define STR_PRINT_FORMAT_HEX_UPPER_CASE  3

#define NEOPIXEL_COUNT 20

#define DUMMY_VALUE 69

uint8_t dsvm_version = 1

#endif

