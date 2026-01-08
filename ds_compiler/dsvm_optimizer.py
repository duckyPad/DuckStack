from dsvm_common import *

def optimize_pass(instruction_list, arg_and_var_dict):
    optimized_list = []
    i = 0
    while i < len(instruction_list):
        current_instr = instruction_list[i]
        
        # Lookahead for peephole optimizations
        if i + 1 < len(instruction_list):
            next_instr = instruction_list[i + 1]
            
            # PUSH0 + DROP -> Remove both
            if current_instr.opcode == OP_PUSH0 and next_instr.opcode == OP_DROP:
                i += 2
                continue

            # POPI/POPR [X] + PUSHI/PUSHR [X] -> DUP + POPI/POPR [X]
            # This handles both Global (POPI) and Local (POPR) variables
            is_same_mem_save_load = (current_instr.opcode == OP_POPI and next_instr.opcode == OP_PUSHI) or (current_instr.opcode == OP_POPR and next_instr.opcode == OP_PUSHR)
            if is_same_mem_save_load and current_instr.payload == next_instr.payload:
                optimized_list.append(dsvm_instruction(opcode=OP_DUP))
                optimized_list.append(current_instr)
                i += 2
                continue

        # PUSHC16 0 -> PUSH0
        if current_instr.opcode in pushc_instructions and current_instr.payload == 0:
            optimized_list.append(dsvm_instruction(opcode=OP_PUSH0, label=current_instr.label, comment=current_instr.comment))
            i += 1
            continue
        if current_instr.opcode in pushc_instructions and current_instr.payload == 1:
            optimized_list.append(dsvm_instruction(opcode=OP_PUSH1, label=current_instr.label, comment=current_instr.comment))
            i += 1
            continue
        if current_instr.opcode == OP_ALLOC and current_instr.payload in arg_and_var_dict and len(arg_and_var_dict[current_instr.payload]['locals']) == 0:
            i += 1
            continue

        optimized_list.append(current_instr)
        i += 1
    
    return optimized_list

def optimize_full_assembly_from_context_dict(ctx_dict):
    arg_and_var_dict = ctx_dict['func_arg_and_local_var_lookup']
    ctx_dict["root_assembly_list"] = optimize_pass(ctx_dict["root_assembly_list"], arg_and_var_dict)
    for key in ctx_dict['func_assembly_dict']:
        ctx_dict['func_assembly_dict'][key] = optimize_pass(ctx_dict['func_assembly_dict'][key], arg_and_var_dict)

def replace_dummy_with_drop(instruction_list):
    for this_instruction in instruction_list:
        if this_instruction.opcode == OP_POPI and this_instruction.payload == DUMMY_VAR_NAME:
            this_instruction.opcode = OP_DROP
            this_instruction.payload = None

def replace_dummy_with_drop_from_context_dict(ctx_dict):
    replace_dummy_with_drop(ctx_dict["root_assembly_list"])
    for key in ctx_dict['func_assembly_dict']:
        replace_dummy_with_drop(ctx_dict['func_assembly_dict'][key])