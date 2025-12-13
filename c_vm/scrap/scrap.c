 stack_push(&data_stack, 65535);
  stack_push(&data_stack, 6);
  stack_pop(&data_stack, NULL);
  stack_print(&data_stack);

  int panic_code = setjmp(jmpbuf);
  if(panic_code != 0)
  {
    printf("VM Crashed! Panic: %d\n", panic_code);
    return;
  }
  

  // while(1)
  // {
  //   ;
  // }

uint32_t make_uint32(uint8_t* base_addr)
{
  // little endian, [0] lsb, [3] msb
    return  (uint32_t)base_addr[0]        |
           ((uint32_t)base_addr[1] << 8)  |
           ((uint32_t)base_addr[2] << 16) |
           ((uint32_t)base_addr[3] << 24);
}


uint8_t read_byte(uint16_t addr)
{
  if (addr >= 0xf801 && addr <= 0xf9ff)
    longjmp(jmpbuf, EXE_ILLEGAL_ADDR);
  if (addr >= 0xfc00 && addr <= 0xfcff)
    longjmp(jmpbuf, EXE_ILLEGAL_ADDR);
  return bin_buf[addr];
}


void memwrite_u32(uint16_t addr, uint32_t value)
{
  if (addr <= USER_VAR_END_ADDRESS_INCLUSIVE)
  {
    write_uint32_as_4B(&bin_buf[addr], value);
    return;
  }
  // if (is_pgv(addr))
  //   return DUMMY_DATA_REPLACE_ME;
  // if (addr >= INTERAL_VAR_START_ADDRESS)
  //   return DUMMY_DATA_REPLACE_ME;
  // return DUMMY_DATA_REPLACE_ME;
  printf("memwrite_u32: %04x %d\n", addr, value);
  longjmp(jmpbuf, EXE_ILLEGAL_ADDR);
}

FUNCTION add2(a, b)
    RETURN a+b
END_FUNCTION



VAR result = add2(5, 10)

