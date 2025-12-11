#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "main.h"

uint8_t str_print_format;
uint8_t str_print_padding;
uint8_t bin_buf[BIN_BUF_SIZE];
uint32_t defaultdelay_value;
uint32_t defaultchardelay_value;
uint32_t charjitter_value;
uint32_t rand_min, rand_max;
uint32_t loop_size;
uint8_t epilogue_actions;
uint8_t allow_abort;
uint8_t kb_led_status;
uint8_t last_stack_op_result;
uint8_t disable_autorepeat;
uint32_t pgv_buf[PGV_COUNT];
uint16_t var_buf[VAR_BUF_SIZE];
int16_t utc_offset_minutes;
uint8_t dsvm_version = 2;
uint32_t this_dsb_file_size;

/*
  Stack grows from larger address to smaller address
  SP points to next available slot
*/
typedef struct
{
  uint8_t* sp;
  uint8_t* top_addr;
  uint8_t* lower_bound;
  uint16_t size_bytes;
} my_stack;

my_stack data_stack;

void stack_init(my_stack* ms, uint8_t* top_addr, uint16_t size_bytes)
{
  ms->top_addr = top_addr;
  ms->sp = top_addr - sizeof(uint32_t);
  ms->size_bytes = size_bytes;
  ms->lower_bound = ms->top_addr - ms->size_bytes;
  memset(ms->lower_bound, 0, size_bytes);
}

uint8_t stack_push(my_stack* ms, uint32_t in_value)
{
  if(ms->sp < ms->lower_bound)
    return EXE_STACK_OVERFLOW;
  memcpy(ms->sp, &in_value, sizeof(uint32_t));
  ms->sp -= sizeof(uint32_t);
  return EXE_OK;
}

uint8_t stack_pop(my_stack* ms, uint32_t *out_value)
{
  uint8_t* next_sp = ms->sp + sizeof(uint32_t);
  if(next_sp >= ms->top_addr)
    return EXE_STACK_UNDERFLOW;
  ms->sp += sizeof(uint32_t);
  memcpy(out_value, ms->sp, sizeof(uint32_t));
  return EXE_OK;
}

#include <stdio.h>
#include <string.h>

void stack_print(my_stack* ms)
{
    printf("\n=== STACK DUMP ===\n");
    printf(" Size: %u bytes\n", ms->size_bytes);
    printf("  Ptr       |   Hex      |  Dec       | Marker\n");
    printf(" -----------+------------+------------+-------\n");

    // Start looking from the high address (Base) down to the SP
    // Note: We start at top_addr - 4 because top_addr is the exclusive upper bound
    uint8_t* current_ptr = ms->top_addr - sizeof(uint32_t);

    // If SP is at the initial position, the stack is empty
    if (ms->sp == (ms->top_addr - sizeof(uint32_t))) {
        printf(" [ EMPTY STACK ]\n");
        printf(" %p |            |            | <--- SP (Next Slot)\n", (void*)ms->sp);
        printf("==================\n\n");
        return;
    }

    // Iterate downwards until we hit the SP
    while (current_ptr > ms->sp)
    {
        uint32_t val;
        // Use memcpy to prevent alignment faults, matching your push/pop logic
        memcpy(&val, current_ptr, sizeof(uint32_t));

        printf(" %p | 0x%08X | %-10u |", (void*)current_ptr, val, val);

        if (current_ptr == ms->top_addr - sizeof(uint32_t)) {
            printf(" <--- BASE");
        }
        
        // The last pushed value is located right above the current SP
        if (current_ptr == ms->sp + sizeof(uint32_t)) {
            printf(" <--- TOP (Last Data)");
        }

        printf("\n");
        
        // Move to the next 32-bit slot (downwards)
        current_ptr -= sizeof(uint32_t);
    }

    // Show where the SP is currently pointing (the next empty slot)
    printf(" %p | [FREESLOT] |            | <--- SP (Next Slot)\n", (void*)ms->sp);
    printf("==================\n\n");
}

uint16_t make_uint16(uint8_t b0, uint8_t b1)
{
  return b0 | (b1 << 8);
}

uint32_t make_uint32(uint8_t* base_addr)
{
  // little endian, [0] lsb, [3] msb
    return  (uint32_t)base_addr[0]        |
           ((uint32_t)base_addr[1] << 8)  |
           ((uint32_t)base_addr[2] << 16) |
           ((uint32_t)base_addr[3] << 24);
}

uint8_t load_dsb(char* dsb_path)
{
  FILE *dsb_file = fopen(dsb_path, "r");
  if(dsb_file == NULL)
    return EXE_DSB_FOPEN_FAIL;
  memset(bin_buf, 0, BIN_BUF_SIZE);
  this_dsb_file_size = fread(bin_buf, 1, BIN_BUF_SIZE, dsb_file);
  fclose(dsb_file);
  if(this_dsb_file_size == 0)
    return EXE_DSB_FREAD_ERROR;
  if(bin_buf[0] != OP_VMINFO)
    return EXE_DSB_INCOMPATIBLE_VERSION;
  if(bin_buf[1] != dsvm_version)
    return EXE_DSB_INCOMPATIBLE_VERSION;
  return EXE_OK;
}

void run_dsb(exe_context* er, char* dsb_path)
{
  uint8_t dsb_load_result = load_dsb(dsb_path);
  printf("DSB load: %d\n", dsb_load_result);
  if(dsb_load_result)
  {
    er->result = dsb_load_result;
    er->next_pc = INSTRUCTION_SIZE_BYTES;
    return;
  }
  uint16_t current_pc = 0;
  
}

exe_context execon;

int main()
{
  printf("hello world!\n");
  run_dsb(&execon, "../ds2py/out.dsb");
  return 0;
}