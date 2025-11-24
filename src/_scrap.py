elif isinstance(node, ast.Call):
        fun_name = node.func.id
        if fun_name not in func_lookup:
            raise ValueError("unknown function name")
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_CALL
        this_instruction['oparg'] = label_dict[func_lookup[fun_name]['fun_start']]
        instruction_list.append(this_instruction)


        elif first_word == cmd_RETURN:
            inst_list = parse_return_value(this_line, cmd_RETURN)
            for item in inst_list:
                print(item)
            exit()

            # inst_list = parse_multi_expression(1, this_line)
            # print(inst_list)
            # exit()
            # this_instruction['opcode'] = OP_RET
            # assembly_listing.append(this_instruction)


elif first_word == cmd_END_FUNCTION:
            # RET, then NOP
            inst_list = parse_multi_expression(1, this_line)
            print(inst_list)
            exit()
            this_instruction['opcode'] = OP_RET
            this_instruction['comment'] = None
            assembly_listing.append(this_instruction)
            this_instruction = get_empty_instruction()
            this_instruction['comment'] = this_line
            this_instruction['label'] = label_dict[lnum]
            assembly_listing.append(this_instruction)