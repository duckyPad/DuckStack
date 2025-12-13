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