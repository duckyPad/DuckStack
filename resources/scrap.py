
hid_send_bluetooth

RAWHID(addr)
send 8/9 bytes of HID starting from ADDR

* PUTS() function and instruction
    * 1 item, channel, n, addr
* STRING Answer is $foo%ld 

-----------------------------
// --- Setup ---
VAR count = 0
VAR target = 1000
VAR startTime = 0
VAR endTime = 0
VAR temp = 0

// --- Start Timer ---
startTime = _TIME_MS

// --- Loop 1000 Times ---
WHILE count < target
    temp = _RANDOM_INT
    count = count + 1
END_WHILE

endTime = _TIME_MS

VAR totalTime = endTime - startTime

STRINGLN Took $totalTime ms
-------------------

POKE8(0xFA00, 0x4c)
POKE8(0xFA01, 0x4f)
POKE8(0xFA02, 0x4c)
PUTS(0x800FFA00)

// (\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\})

VAR i = 0
_UNSIGNED_MATH = 1
_STR_PRINT_FORMAT = 0
WHILE i < 25
    VAR temp = _RANDOM_INT
    STRINGLN $temp
    i += 1
END_WHILE

void wrap_print(const char* format, uint32_t value, uint8_t* buf, uint32_t buf_size)

wrap_print("%x", 255, buf, 32)

buf should have "ff"

_RAND_CHR(channel, chr_type)
    channel: bit mask
        bit 0: kb
        bit 1: oled
    chr_type: bit mask
        bit 0: letter upper
        bit 1: letter lower
        bit 2: number
        bit 3: symbol
_RAND_INT(lower, upper)
_PUTS(channel, n, addr)

"""
DEFINE MAX_ADDR 64
VAR curr_addr = 0
_UNSIGNED_MATH = 1
_STR_PRINT_FORMAT = 3
_STR_PRINT_PADDING = 2
WHILE curr_addr != MAX_ADDR
    VAR value = PEEK8(curr_addr)
    STRINGLN Addr $curr_addr: $value
    curr_addr = curr_addr + 1
END_WHILE
"""

"""
_UNSIGNED_MATH = 1
_STR_PRINT_FORMAT = 3
_STR_PRINT_PADDING = 4

POKE8(0xfa02, 0x9)
POKE8(0xfa04, 0xff)

VAR start_addr = 0xfa00
VAR end_addr = start_addr + 5
VAR curr_addr = start_addr
WHILE curr_addr <= end_addr
    VAR value = PEEK8(curr_addr)
    STRINGLN Addr $curr_addr: $value
    curr_addr = curr_addr + 1
END_WHILE
"""

this_indent_level = len(if_search_stack) + len(func_search_stack) + len(while_search_stack)

        presult = PARSE_ERROR
        pcomment = f"single_pass: Unknown error"

        if first_word != cmd_DEFINE:
            is_success, replaced_str = replace_DEFINE(this_line, define_dict)
            if is_success is False:
                return_dict['is_success'] = False
                return_dict['comments'] = "Recursive DEFINE"
                return_dict['error_line_number_starting_from_1'] = line_number_starting_from_1
                return_dict['error_line_str'] = this_line
                return return_dict
            this_line = replaced_str


if needs_rstrip(first_word):
            line_obj.content = this_line.rstrip(" \t")
        if first_word != cmd_DEFINE:
            is_success, replaced_str = replace_DEFINE(this_line, all_def_dict)
            if is_success is False:
                rdict['is_success'] = False
                rdict['comments'] = "Recursive DEFINE"
                return rdict
            else:
                line_obj.content = replaced_str
        else:
            continue


def print_assembly_list(asmlist):
    if print_asm is False:
        return
    for item in asmlist:
        print(item)

    # no need to pop unused stack item for reserved func
    for key in ds_reserved_funcs:
        if f"{key}(" in line_obj.content:
            return False


def test_func(spam, eggs):
	foo = 10
	return spam * eggs + foo

def another(spam, eggs):
	foo = 10
	return spam - eggs - foo

result = test_func(11, 22)

another(result, 44)


# print(line_obj.orig_lnum_sf1, len(if_search_stack), len(func_search_stack), len(while_search_stack))
        indent_level_dict[line_obj.orig_lnum_sf1] = len(if_search_stack) + len(func_search_stack) + len(while_search_stack)

    # rdict = single_pass(program_listing)
    # if rdict['is_success'] is False:
    #     return rdict

    print("---------First Pass OK!---------")

    # for item in program_listing:
    #     final_str = "    "*rdict['indent_level_dict'][item.orig_lnum_sf1] + item.content
    #     print(final_str)
	
    final_dict = single_pass(second_pass_program_listing)
    second_pass_program_listing = final_dict['program_listing_with_indent_level']

    for item in second_pass_program_listing:
        final_str = "    "*item.indent_level + item.content
        print(final_str)

def walk_tree(this_tree):
    for statement in this_tree.body:
        print(statement)
        for item in ast.iter_child_nodes(statement):
            print(item)

        print("---------")

if isinstance(node, ast.Assign):
		print("ASSIGN!")
		print(node._fields)
		print(node.targets, node.value, node.type_comment)
		exit()
WALKABLE_NODES = (
    ast.BinOp,
    ast.BoolOp,
    ast.Compare,
    ast.UnaryOp,
    ast.Call,
	ast.Assign,
)

def is_walkable(node):
	return isinstance(node, WALKABLE_NODES)

FUNCTION test()
    VAR $foo = 3
END_FUNCTION

VAR $foo = 2
VAR $bar = 3 + $foo
STRING Value is: $bar
CTRL ALT DELETE


post_pp_listing = rdict["program_listing_with_indent_level"]
save_lines_to_file(post_pp_listing, "ppds.txt")
pyout = ds2py.run_all(post_pp_listing)
save_lines_to_file(pyout, "pyds.py")
# print_ds_line_list(pyout)
source = dsline_to_source(pyout)
tree = ast.parse(source, mode="exec")
# print(ast.dump(tree, indent=2))
#-------------

	if isinstance(node, ast.FunctionDef):
		print_node_info(node)
		arg_list = node.args.args
		# put function name in parent_info_dict, check for nested func def
		func_statements = node.body # lines inside function
		for item in arg_list:
			print_node_info(item)
		# exit()
              
    if isinstance(node, ast.Assign):
		"""
		node.targets is the variable to assign to
		resolve and add to instruction list, POPI32
		node.value is the right hand side
		print("ASSIGN!")
		print(node._fields)
		print(node.targets, node.value)
		"""
		# POPI32 instruction here
		postorder_walk(node.value, action, instruction_list, parent_history)
		

def visit_node(node, instruction_list, parent_info):
    # myast.print_node_info(node)
    print("hello", parent_info)


if isinstance(node, ast.Assign):
		# POPI32 instruction here
		# postorder_walk(node.value, action, instruction_list, parent_history)
		pass

# dont distingusih between left and right, treat case by case
def postorder_walk(node, action, instruction_list):
	print_node_info(node)
	if node is None:
		raise ValueError(f"Unknown AST Node")
	if isinstance(node, ast.BoolOp):
		for item in node.values:
			postorder_walk(item, action, instruction_list)
	if isinstance(node, ast.Call):
		for item in node.args:
			postorder_walk(item, action, instruction_list)
	if isinstance(node, ast.Assign):
		# walk the rest
		action(node, instruction_list)
		return
	if isinstance(node, ast.FunctionDef):
		print("FunctionDef Node: Not Implemented")
		exit()

	if is_leaf(node):
		action(node, instruction_list)
		return
	postorder_walk(get_left(node), action, instruction_list)
	postorder_walk(get_right(node), action, instruction_list)
	action(node, instruction_list)

def try_print_node(node):
	lineno = getattr(node, "lineno", None)
	print(f"---Line {lineno}: {type(node)}---")
	for item in node._fields:
		if getattr(node, item, None) is not None:
			print(f"{item}: {getattr(node, item, None)}")
	print()

def print_node_info(node):
	try:
		try_print_node(node)
	except:
		print(node)

# print(ast.dump(tree, indent=2))
# print_ds_line_list(pyout)

rdict["assembly_list"] = []
# rdict["func_assembly_dict"] = {}
# rdict["parent_history_list"] = []
		goodies['if_take_label'] = f"{node.__class__.__name__}_take@{this_orig_ds_lnum_sf1}"
	elif isinstance(node, ast.AugAssign):
		postorder_walk(node.target, action, goodies)
		postorder_walk(node.value, action, goodies)
		postorder_walk(node.op, action, goodies)


def make_instruction_pushc32(value, comment=""):
    node_value_high = (int(value) & 0xffff0000) >> 16
    node_value_low = int(value) & 0xffff
    inst_list = []
    this_instruction = get_empty_instruction(comment=comment)
    this_instruction['opcode'] = OP_PUSHC16
    this_instruction['oparg'] = node_value_low
    inst_list.append(this_instruction)
    if node_value_high:
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['oparg'] = node_value_high
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['oparg'] = 16
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_LSHIFT
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_BITOR
        inst_list.append(this_instruction)
    return inst_list

if goodies['this_func_name'] is not None:
        print(f"In function: {goodies['this_func_name']}()!!!")

"""
elif isinstance(node, ast.FunctionDef):
		arg_list = node.args.args
		print("FunctionDef Node: Not Implemented")
		print_node_info(node)
		for item in arg_list:
			print(item.__dict__)
		exit()

"""

    # for func_name in ds_func_arg_lookup:
    #     arg_count = ds_func_arg_lookup[func_name]
    #     # func_proto = f"def {key}():\n    pass"
    #     func_proto = f"def {make_dspy_func_name(func_name)}("
    #     for x in range(arg_count):
    #         func_proto += f"arg{x},"
    #     func_proto = func_proto.rstrip(",")
    #     func_proto += "):"
    #     new_obj = ds_line(content=func_proto)
    #     new_listing.append(new_obj)
    #     new_obj = ds_line(content="pass", indent_lvl=1)
    #     new_listing.append(new_obj)


def print_instruction(instruction):
    if instruction['label'] is not None and len(instruction['label']):
        print(f"~~~~{instruction['label']}:")

    if instruction['addr'] is not None:
        print(str(instruction['addr']).ljust(5), end='')
    print(instruction['opcode'][0].ljust(10), end='')
    tempstr = ""
    this_payload = instruction['payload']
    if this_payload is not None:
        if isinstance(this_payload, str) and len(this_payload) > 14:
            this_payload = f"{this_payload[:14]}..."
        tempstr = f"{this_payload}".ljust(6)
        if isinstance(this_payload, int):
            tempstr += f"{hex(this_payload)}".ljust(6)
    print(tempstr.ljust(20), end='')
    tempstr = ""
    this_comment = str(instruction['comment'])
    if len(this_comment) > 32:
        tempstr = ";" + str(instruction['comment'].strip())[:32] + "..."
    elif len(this_comment) > 0:
        tempstr = ";" + str(instruction['comment'].strip())
    print(tempstr)
	

try:
        sym = table.lookup(name)
        print(sym)
        # exit()
        if sym.is_local() is False:
            raise ValueError(f"Symbol \"{name}\" not found")
    except KeyError:
        # name is not known in this scope at all
        raise ValueError(f"Symbol \"{name}\" not found: {e}")


    print(
    "symbol_info:\n"
    f"  name:        {name!r}\n"
    f"  function:    {current_function!r}\n"
    f"  global:      {sym_global_scope!r}\n"
    f"  func_scope:  {sym_func_scope!r}"
)

def search_in_symtable(name:str,table:symtable.SymbolTable):
    try:
        return table.lookup(name)
    except KeyError as e:
        print(f"search_in_symtable: {e}")
    return None

def search_in_symtable(name:str,table:symtable.SymbolTable):
    try:
        return table.lookup(name)
    except KeyError as e:
        print(f"search_in_symtable: {e}")
    return None

def classify_name(name: str,
                  current_function: str | None,
                  root_table: symtable.SymbolTable) -> int:
    if name in internal_variable_dict:
        return SYM_TYPE_GLOBAL_VAR
    
    function_names = {child.get_name() for child in root_table.get_children()
                      if child.get_type() == 'function'}

    if name in function_names and name != current_function:
        raise ValueError(f"Variable \"{name}\" conflicts with function \"{name}()\"")
    
    if current_function is None:
        table = root_table
    else:
        table = myast.find_function_table(root_table, current_function)
        if table is None:
            raise ValueError(f"No symtable for function {current_function!r}")
    sym_func_scope = search_in_symtable(name, table)
    sym_global_scope = search_in_symtable(name, root_table)
    if sym_global_scope is None:
        raise ValueError(f"Symbol \"{name}\" not found")
    if current_function is not None and sym_func_scope.is_parameter():
        return SYM_TYPE_FUNC_ARG
    # Anything else that *does* exist (local / global / free / imported)
    return SYM_TYPE_GLOBAL_VAR

    function_names = {child.get_name() for child in root_table.get_children() if child.get_type() == 'function'}

    # print(name, current_function, function_names)
    # if name in function_names and name != current_function: # throw error only on second conflict?
    #     raise ValueError(f"Variable \"{name}\" conflicts with function \"{name}()\"")


def group_vars(var_infos):
    result = defaultdict(lambda: {"args": [], "locals": []})
    
    for v in var_infos:
        if v.type == SymType.FUNC_ARG and v.func is not None:
            result[v.func]["args"].append(v.name)
        elif v.type == SymType.FUNC_LOCAL_VAR and v.func is not None:
            result[v.func]["locals"].append(v.name)

    return {
        func: {
            "args": sorted(data["args"]),
            "locals": sorted(data["locals"]),
        }
        for func, data in result.items()
    }

    print(group_vars(rdict['var_info_set']))

    
    # for item in rdict['var_info_set']:
    #     print(item)
    # exit()

final_assembly_list = []

    curr_inst_addr = 0
    for this_inst in rdict['root_assembly_list']:
        this_inst.addr = curr_inst_addr
        curr_inst_addr += this_inst.opcode.length
        print(this_inst)
        if isinstance(this_inst.payload, int):
            final_assembly_list.append(this_inst)
            continue
        # print(this_inst)
        if this_inst.opcode in [OP_PUSHI, OP_POPI]:
            this_inst.payload = resolve_global_and_reserved_var_address(this_inst.payload, user_declared_global_var_addr_lookup)
            final_assembly_list.append(this_inst)
        elif this_inst.opcode in [OP_PUSHR, OP_POPR]:
            # local / func args
            pass

        # lay out all instructions
        # duckyscript commands absolutely not resolved, double check
        # make label to address lookup dict

    # print("\n----- FINAL ASS -----")
    # print_assembly_list(final_assembly_list)


    def __init__(self,\
                opcode=OP_NOP,\
                payload=None,\
                label=None,\
                comment='',\
                addr=None,\
                parent_func=None,\
                var_type=None,\
                # obj_name="",
                ):
        self.opcode = opcode
        self.payload = payload
        self.label = label
        self.comment = comment
        self.addr = addr
        self.parent_func = parent_func
        self.var_type = var_type
        # self.obj_name = obj_name
        # if isinstance(self.payload, str):
        #     self.obj_name = self.payload



            comment_items = []
        # if self.parent_func:
        #     comment_items.append(f"{self.parent_func}")
        # if len(self.obj_name):
        #     comment_items.append(f"[{self.obj_name}]")
        # if self.var_type:
        #     comment_items.append(f"{self.var_type.name}")

# -------------


def group_vars(var_infos):
    this_fun = fun_info()
    result = defaultdict(lambda: {"args": set(), "locals": set()})
    
    for v in var_infos:
        if v.type == SymType.FUNC_ARG and v.func is not None:
            result[v.func]["args"].add(v.name)
        elif v.type == SymType.FUNC_LOCAL_VAR and v.func is not None:
            result[v.func]["locals"].add(v.name)

    # return {
    #     func: {
    #         "args": sorted(data["args"]),
    #         "locals": sorted(data["locals"]),
    #     }
    #     for func, data in result.items()
    # }

    print(result)
    exit()

    return {
        func: (sorted(data["args"]),sorted(data["locals"])) for func, data in result.items()
    }


    # ------------------------------



def make_fun_info(info_list):
    fun_dict = {}
    for this_var in info_list:
        fun_name = this_var.func
        if fun_name is None:
            continue
        if fun_name not in fun_dict:
            fun_dict[fun_name]
        if this_var.type == SymType.FUNC_ARG:
            pass
        print(this_var)
    exit()

---------------------

print()
    print_assembly_list(rdict['root_assembly_list'])
    print()

    for key in rdict['func_assembly_dict']:
        print(f'----FUNC: {key}----')
        print_assembly_list(rdict['func_assembly_dict'][key])
        print(f'----END {key}----')
    exit()

-------------------

"""
dump everything into one list
first main code, then func code

go through each instruction:
    collect all global variables, assign address to them
    collect all strings, deduplicate, process, generate address
    look at variables, figure out arg position and local var ordering
"""

        # print(f"{item}: {hex(user_declared_global_var_addr_lookup[item])}")


elif this_inst.opcode == OP_ALLOC:
            #find out how many locals
            local_vars_count = 0
            try:
                local_vars_count = len(func_arg_and_local_var_lookup[this_inst.payload]['args'])
            except Exception as e:
                pass
            # print(this_inst.payload, local_vars_count)
            this_inst.payload = local_vars_count
            # print(this_inst)


------


FUNCTION print_result(value)
    value = value + 100
    STRINGLN Value is: $value
END_FUNCTION

FUNCTION is_even(n, b, c)
    VAR mylocal = n%2 + n +b + c
    VAR test = mylocal /2 
    IF mylocal == 0 THEN
        RETURN 1
    END_IF
    RETURN test
END_FUNCTION

FUNCTION nothing()
    RETURN
END_FUNCTION

VAR i = 1
VAR sum = 0
VAR eq = 9

WHILE i <= 6
    IF is_even(i, i, i) THEN
        sum = sum + i
    END_IF
    i = i + 1
END_WHILE

print_result(sum)


----            


            print(this_inst)
            print(this_inst.payload, this_inst.parent_func)


-------



def replace_var_in_str(instruction, arg_and_local_var_lookup, udgv_lookup):
    bytearr = bytearray()
    curr = -1
    msg = instruction.payload
    while curr < len(msg)-1:
        curr += 1
        this_letter = msg[curr]
        if this_letter == "$":
            var_name, var_addr, var_type = get_partial_varname_addr(msg[curr+1:], instruction, arg_and_local_var_lookup, udgv_lookup)
            if var_addr is None:
                bytearr += this_letter.encode()
                continue
            if var_type in [SymType.FUNC_ARG, SymType.FUNC_LOCAL_VAR]:
                this_boundary = var_boundary_fp_rel
                payload_bytes = var_addr.to_bytes(2, endianness, signed=True)
            else:
                this_boundary = var_boundary_udgv
                payload_bytes = var_addr.to_bytes(2, endianness, signed=False)
            curr += len(var_name)
            bytearr += this_boundary.to_bytes(1, endianness)
            bytearr += payload_bytes
            bytearr += this_boundary.to_bytes(1, endianness)
        else:
            bytearr += this_letter.encode()
    return bytearr


-----------



@dataclass(slots=True)
class bin_str:
    content: str
    start_addr: int

---

 elif this_inst.opcode == OP_PUSHSTR:
            bytestr = replace_var_in_str(this_inst, func_arg_and_local_var_lookup, user_declared_global_var_addr_lookup)
            if bytestr not in user_strings_lookup:
                if len(user_strings_lookup) == 0:
                    user
                user_strings_lookup[bytestr]


    for key in user_strings_dict:
        print(f"{user_strings_dict[key]}  DATA: {key}")
    exit()

---

for statement in my_tree.body:
    rdict["func_def_name"] = None
    rdict["caller_func_name"] = None
    # myast.postorder_walk(statement, visit_node, rdict)
    myast.print_node_info(statement)

---

def line_has_unconsumed_stack_value(line_obj):
    try:
        ast_root = ast.parse(line_obj.content, mode="exec").body
    except Exception as e:
        return False
    # goodies = {}
    # myast.postorder_walk(ast_root, my_visit, goodies)
    print(line_obj, ast_root)
    # myast.print_node_info(ast_root)
    return True
----

    if len(fss) == 0:
        print(f"Variable {this_var_name} is on root level")
    else:
        parent_func_name = fss[-1]
        print(f"Variable {this_var_name} is in function {parent_func_name}")
----
func_arg_and_local_var_lookup = group_vars(rdict['var_info_set'])
    user_declared_global_var_addr_lookup = {}
    for index, item in enumerate(sorted([x.name for x in rdict['var_info_set'] if x.type is SymType.GLOBAL_VAR])):
        user_declared_global_var_addr_lookup[item] = index * USER_VAR_BYTE_WIDTH + USER_VAR_START_ADDRESS
---


def group_vars(var_infos):
    result = defaultdict(lambda: {"args": [], "locals": []})
    
    for v in var_infos:
        if v.type == SymType.FUNC_ARG and v.func is not None:
            result[v.func]["args"].append(v.name)
        elif v.type == SymType.FUNC_LOCAL_VAR and v.func is not None:
            result[v.func]["locals"].append(v.name)

    return {
        func: {
            "args": sorted(data["args"]),
            "locals": sorted(data["locals"]),
        }
        for func, data in result.items()
    }

from collections import defaultdict


def get_partial_varname_addr(msg, str_inst, arg_and_local_var_lookup, udgv_lookup):
    if len(msg) == 0:
        return None, None, None
    last_name = None
    last_addr = None
    last_type = None
    for x in range(len(msg)+1):
        partial_name = msg[:x]
        this_result = var_name_to_address_lookup_only_for_strprint(partial_name, str_inst, arg_and_local_var_lookup, udgv_lookup)
        if this_result[0] is not None:
            last_name = partial_name
            last_addr, last_type = this_result
    if last_addr is not None:
        return last_name, last_addr, last_type
    return None, None, None


-------

output_bin_array = bytearray()
    for this_inst in final_assembly_list:
        output_bin_array += this_inst.opcode.code.to_bytes(1, byteorder=endianness)
        this_payload = this_inst.payload
        if this_payload is None:
            continue
        output_bin_array += pack_to_two_bytes(this_payload)
        # output_bin_array += this_payload.to_bytes(1, byteorder=endianness)
        # print(this_inst, inst_bytes.hex(), this_inst.payload)
    print(output_bin_array.hex())

# print(output_bin_array.hex())
    # print(len(output_bin_array))

    final_result = {}
    for func_name, data in grouped_data.items():
        final_result[func_name] = {
            "args": data['args'],
            "locals": sorted(data["locals"])
        }

    for key in grouped_data:
        this_func_info = grouped_data[key]
        this_func_info['locals'].sort()
    print("grouped_data", dict(grouped_data))
    print("final_result", final_result)
    return final_result

func_args_dict

this_arg_count = how_many_args(func_name, goodies['symtable_root'])


goodies['if_destination_label'] = if_skip_label
        postorder_walk(node.test, action, goodies)


def get_func_parameters(func_name: str, root: symtable.SymbolTable):
    func_table = find_function_table(root, func_name)
    if func_table is None:
        return None
    # returns a tuple of parameter names
    return func_table.get_parameters()


def how_many_args(name: str, context_dict):
    params = get_func_parameters(name, table)
    if params is None:
        return None
    return len(params)

# -----------------------

    print("----- Binary output ------")
    for bbb in output_bin_array:
        print(f"{bbb:02x}", end=" ")
    print()
    print()
    file_path = "out.dsb"
    with open(file_path, 'wb') as file_out:
        bytes_written = file_out.write(output_bin_array)
        print(f"Successfully wrote {bytes_written} bytes to '{file_path}'")
    print(f"MAX_BIN_SIZE: {MAX_BIN_SIZE} Bytes")


-----

def make_dsb_no_exception(program_listing):
    try:
        return make_dsb_with_exception(program_listing)
    except Exception as e:
        print("MDNE:", traceback.format_exc())
        # print(e)
        # print(global_context_dict)
        # comp_result = compile_result(
        #     is_success=False,
        #     error_comment = str(e.comment),
        #     error_line_number_starting_from_1 = e.line_number,
        # )
    return None
    # return comp_result

    wtf = make_dsb_with_exception(program_listing)
    print(wtf)
    exit()

# |WAITK|`86`/`0x57`| **Wait for Keypress**<br>Pop **ONE** item as `KeyID`<br>Block until the key is pressed<br> 0 = Any key|
