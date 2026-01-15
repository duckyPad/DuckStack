uint32_t* dsvm_get_physical_addr(uint16_t vm_addr)
{
  // 1. Executable, Stack, Global Vars, and Scratch Memory
  // Range: 0x0000 to 0xF7FF
  // Buffer: bin_buf (Map 1:1)
  if (vm_addr <= SCRATCH_MEM_END_ADDRESS_INCLUSIVE)
    return (uint32_t *)&bin_buf[vm_addr];
  
  // 2. Reserved Region
  // Range: 0xF800 to 0xFBFF
  // Action: Invalid Access
  if (vm_addr < PGV_START_ADDRESS)
    return NULL;

  // 3. Persistent Global Variables
  // Range: 0xFC00 to 0xFDFF (approx, depends on PGV_COUNT)
  // Buffer: pgv_buf (Offset relative to PGV_START_ADDRESS)
  if (vm_addr <= PGV_END_ADDRESS_INCLUSIVE)
    return (uint32_t *)&pgv_buf[vm_addr - PGV_START_ADDRESS];

  // 4. VM Reserved Variables (MemIO)
  // Range: 0xFE00 to 0xFFFF
  // Buffer: memIO_buf (Offset relative to INTERAL_VAR_START_ADDRESS)
  if (vm_addr >= INTERAL_VAR_START_ADDRESS)
    return (uint32_t *)&memIO_buf[vm_addr - INTERAL_VAR_START_ADDRESS];

  // Fallback for any gaps (e.g. between PGV end and IO start if PGV count changes)
  return NULL;
}


char* make_str(uint16_t str_start_addr)
{
  uint16_t curr_addr = str_start_addr;
  uint8_t this_char, lsb, msb;
  memset(read_buffer, 0, READ_BUF_SIZE);
  while(1)
  {
    this_char = read_byte(curr_addr);
    if(this_char == 0)
      break;

    if(this_char == MAKESTR_VAR_BOUNDARY_IMM)
    {
      curr_addr++;
      lsb = read_byte(curr_addr);
      curr_addr++;
      msb = read_byte(curr_addr);
      curr_addr++;
      char* format_spec_start = bin_buf+curr_addr;
      char* 
      memset(format_spec_buf, 0, FORMAT_SPEC_BUF_SIZE);
      if(*format_spec_start != MAKESTR_VAR_BOUNDARY_IMM)
        copy_format_specifier(format_spec_start, format_spec_buf, FORMAT_SPEC_BUF_SIZE, MAKESTR_VAR_BOUNDARY_IMM);
      exit(0);
      // here
      curr_addr++;
      uint16_t var_addr = make_uint16(lsb, msb);
      uint32_t var_value = memread_u32(var_addr);
      memset(make_str_buf, 0, STR_BUF_SIZE);
      // my_snprintf
      strcat(read_buffer, make_str_buf);
      continue;
    }
    if(this_char == MAKESTR_VAR_BOUNDARY_REL)
    {
      curr_addr++;
      lsb = read_byte(curr_addr);
      curr_addr++;
      msb = read_byte(curr_addr);
      curr_addr++;
      curr_addr++;
      int16_t fp_offset = (int16_t)make_uint16(lsb, msb);
      uint32_t var_value;
      stack_read_fp_rel(&data_stack, fp_offset, &var_value);
      memset(make_str_buf, 0, STR_BUF_SIZE);
      // my_snprintf
      strcat(read_buffer, make_str_buf);
      continue;
    }
    memset(make_str_buf, 0, STR_BUF_SIZE);
    snprintf(make_str_buf, STR_BUF_SIZE, "%c", this_char);
    strcat(read_buffer, make_str_buf);
    curr_addr++;
  }
  return read_buffer;
}



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

    printf("frame_info: %08x\n", frame_info);
    printf("Unimplemented opcode: %d\n", opcode);longjmp(jmpbuf, EXE_UNIMPLEMENTED);


printf("BIN_BUF_SIZE: 0x%04x %d\n", BIN_BUF_SIZE, BIN_BUF_SIZE);
printf("MAX_BIN_SIZE: 0x%04x %d\n", MAX_BIN_SIZE, MAX_BIN_SIZE);


FUNCTION addargs(a, b, c)
    VAR myloc = a + b + c
    VAR dummy = 99
    VAR another = 255
    return myloc *2
END_FUNCTION

VAR result = addargs(5, 10, 15)

STRING result is: $result


get_partial_varname_addr

FUNCTION test(wtf, b, c, d)
    VAR what = 90
    STRINGLN Args: $wtf, $b, $c, $d, $what
END_FUNCTION

VAR hello = test(10, 20, 30, 40)


  printf("DSB size: %d Bytes\n", this_dsb_size);
  printf("Stack size: %d Bytes\n", data_stack_size_bytes);