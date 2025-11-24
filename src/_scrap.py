elif isinstance(node, ast.Call):
        fun_name = node.func.id
        if fun_name not in func_lookup:
            raise ValueError("unknown function name")
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_CALL
        this_instruction['oparg'] = label_dict[func_lookup[fun_name]['fun_start']]
        instruction_list.append(this_instruction)