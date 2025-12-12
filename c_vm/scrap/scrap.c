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