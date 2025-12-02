import sys
from dsvm_common import *
import ds3_preprocessor
import ds2py
import ast
import symtable
import ast
import sys
import symtable
import myast
import copy

"""
duckyscript VM changelog
version 0:
OG duckyPad with duckyscript 3

version 1:
duckyPad Pro with duckyScript 3
Done:
Added VMVER to aid version checking
mouse move and mouse scroll arguments on stack
more changes at the end of bytecode_vm.md

Version 2:
2025-11-23
New flat memory map
complete overhaul
new opcode values
single stack
32 bit stack width and arithmetics

"""
DS_VM_VERSION = 2

arith_lookup = {
    "Eq" : OP_EQ,
    "NotEq" : OP_NOTEQ,
    "Lt" : OP_LT,
    "LtE" : OP_LTE,
    "Gt" : OP_GT,
    "GtE" : OP_GTE,

    "Add" : OP_ADD,
    "Sub" : OP_SUB,
    "Mult" : OP_MULT,
    "Div" : OP_DIV,
    "Mod" : OP_MOD,
    "Pow" : OP_POW,

    "LShift" : OP_LSHIFT,
    "RShift" : OP_RSHIFT,
    "BitOr" : OP_BITOR,
    "BitAnd" : OP_BITAND,
    "BitXor" : OP_BITXOR,

    "And" : OP_LOGIAND,
    "Or" : OP_LOGIOR,

    "Invert" : OP_BITINV,
    "Not" : OP_LOGINOT,
    "USub" : OP_USUB,
}

def get_empty_instruction(comment="", orig_lnum_sf1=None, py_lnum_sf1=None):
    return {
    'opcode':OP_NOP,
    'payload':None,
    'label':None,
    'comment':comment,
    'addr':None,
    'orig_lnum_sf1':orig_lnum_sf1,
    'py_lnum_sf1':py_lnum_sf1,
    }

def make_instruction_pushc32(value, comment=""):
    node_value_high = (int(value) & 0xffff0000) >> 16
    node_value_low = int(value) & 0xffff
    inst_list = []
    this_instruction = get_empty_instruction(comment=comment)
    this_instruction['opcode'] = OP_PUSHC16
    this_instruction['payload'] = node_value_low
    inst_list.append(this_instruction)
    if node_value_high:
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['payload'] = node_value_high
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['payload'] = 16
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_LSHIFT
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction(comment=comment)
        this_instruction['opcode'] = OP_BITOR
        inst_list.append(this_instruction)
    return inst_list

def print_assembly_list(asmlist):
    # print()
    for item in asmlist:
        print(item)
    # print()

AST_ARITH_NODES = (
    ast.operator,
    ast.cmpop,
    ast.boolop,
    ast.unaryop,
)

def get_orig_ds_line_from_py_lnum(rdict, this_pylnum_sf1):
    if this_pylnum_sf1 is None:
        return ""
    # print("this_pylnum_sf1:", this_pylnum_sf1)
    og_index_sf0 = None
    for line_obj in rdict['ds2py_listing']:
        if line_obj.py_lnum_sf1 == this_pylnum_sf1:
            og_index_sf0 = line_obj.orig_lnum_sf1 - 1
    if og_index_sf0 is None:
        return ""
    # print(rdict['orig_listing'])
    return rdict['orig_listing'][og_index_sf0].content

SYM_TYPE_GLOBAL_VAR = 0
SYM_TYPE_FUNC_ARG = 1

def classify_name(name: str,
                  current_function: str | None,
                  root_table: symtable.SymbolTable) -> int:
    
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
    try:
        sym = table.lookup(name)
        if sym.is_local() is False:
            raise ValueError(f"Symbol \"{name}\" not found")
    except KeyError:
        # name is not known in this scope at all
        raise ValueError(f"Symbol {name} not found")
    if current_function is not None and sym.is_parameter():
        return SYM_TYPE_FUNC_ARG
    # Anything else that *does* exist (local / global / free / imported)
    return SYM_TYPE_GLOBAL_VAR

def visit_name_node(node, goodies, inst_list):
    og_ds_line = goodies['og_ds_line']
    current_function = goodies['this_func_name']
    symtable_root = goodies['symtable_root']

    sym_type = classify_name(node.id, current_function, symtable_root)
    if isinstance(node.ctx, ast.Store):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        if sym_type == SYM_TYPE_FUNC_ARG:
            this_instruction['opcode'] = OP_POPR
        else:
            this_instruction['opcode'] = OP_POPI
        this_instruction['payload'] = str(node.id)
        inst_list.append(this_instruction)
    elif isinstance(node.ctx, ast.Load):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        if sym_type == SYM_TYPE_FUNC_ARG:
            this_instruction['opcode'] = OP_PUSHR
        else:
            this_instruction['opcode'] = OP_PUSHI
        this_instruction['payload'] = str(node.id)
        inst_list.append(this_instruction)

def visit_node(node, goodies):
    current_function = goodies['this_func_name']
    if current_function is None:
        instruction_list = goodies['root_assembly_list']
    elif current_function not in goodies['func_assembly_dict']:
        goodies['func_assembly_dict'][current_function] = []
        instruction_list = goodies['func_assembly_dict'][current_function]
    else:
        instruction_list = goodies['func_assembly_dict'][current_function]
    og_ds_line = get_orig_ds_line_from_py_lnum(goodies, getattr(node, "lineno", None))
    # print(current_function, og_ds_line)
    goodies['og_ds_line'] = og_ds_line
    if isinstance(node, ast.Name):
        visit_name_node(node, goodies, instruction_list)
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            this_instruction = get_empty_instruction(comment=og_ds_line)
            this_instruction['opcode'] = OP_PUSHSTR
            this_instruction['payload'] = node.value
            instruction_list.append(this_instruction)
        elif isinstance(node.value, int):
            instruction_list += make_instruction_pushc32(node.value, og_ds_line)
        else:
            raise ValueError("Unknown type:", type(node.value))
    elif isinstance(node, AST_ARITH_NODES):
        op_name = node.__class__.__name__
        if op_name not in arith_lookup:
            raise ValueError("unknown operation")
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = arith_lookup[op_name]
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.If):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_BRZ
        this_instruction['payload'] = goodies['if_destination_label']
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.While):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_BRZ
        this_instruction['payload'] = goodies['while_end_label']
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.Continue):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_JMP
        this_instruction['payload'] = goodies['while_start_label']
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.Break):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_JMP
        this_instruction['payload'] = goodies['while_end_label']
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.Call):
        func_name = node.func.id
        this_instruction = get_empty_instruction(comment=og_ds_line)
        if func_name in ds_reserved_funcs:
            this_instruction['opcode'] = ds_reserved_funcs[func_name][0]
        else:
            this_instruction['opcode'] = OP_CALL
            this_instruction['payload'] = f"func_{func_name}"
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.Return):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_RET
        arg_count = myast.how_many_args(current_function, goodies['symtable_root'])
        if arg_count == None:
            raise ValueError("Invalid arg count")
        this_instruction['payload'] = arg_count
        instruction_list.append(this_instruction)
    elif isinstance(node, myast.add_nop):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_NOP
        this_instruction['label'] = node.label
        instruction_list.append(this_instruction)
    elif isinstance(node, myast.add_jmp):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_JMP
        this_instruction['payload'] = node.label
        instruction_list.append(this_instruction)
    elif isinstance(node, myast.add_push0):
        this_instruction = get_empty_instruction(comment=og_ds_line)
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['payload'] = 0
        this_instruction['label'] = node.label
        instruction_list.append(this_instruction)
    else:
        raise ValueError("Unknown leaf node:", node)
    
def print_symtable(tbl, indent=0):
    pad = " " * indent
    print(f"{pad}Table ({tbl.get_type()}): {tbl.get_name()}")
    for symbol in tbl.get_symbols():
        print(f"{pad}  - {symbol.get_name()} "
              f"(param={symbol.is_parameter()}, "
              f"local={symbol.is_local()}, "
              f"global={symbol.is_global()}, "
              f"free={symbol.is_free()}, "
              )

    for child in tbl.get_children():
        print_symtable(child, indent + 2)

# ---------------------------

if __name__ != "__main__":
    exit()

if len(sys.argv) < 2:
    print(f"Usage: {__file__} <ds3_script> [output]")
    exit()

text_file = open(sys.argv[1])
text_listing = text_file.readlines()
text_file.close()

program_listing = []
for index, line in enumerate(text_listing):
    line = line.rstrip("\r\n")
    program_listing.append(ds_line(line, index + 1))

orig_listing = copy.deepcopy(program_listing)
rdict = ds3_preprocessor.run_all(program_listing)

if rdict['is_success'] is False:
    print("Preprocessing failed!")
    print(f"\t{rdict['comments']}")
    print(f"\tLine {rdict['error_line_number_starting_from_1']}: {rdict['error_line_str']}")
    exit()

rdict["orig_listing"] = orig_listing
post_pp_listing = rdict["dspp_listing_with_indent_level"]
save_lines_to_file(post_pp_listing, "ppds.txt")
pyout = ds2py.run_all(post_pp_listing)
rdict["ds2py_listing"] = pyout
save_lines_to_file(pyout, "pyds.py")
source = dsline_to_source(pyout)
my_tree = ast.parse(source, mode="exec", optimize=-1)
symtable_root = symtable.symtable(source, filename="ds2py", compile_type="exec")
# print_symtable(symtable_root)
rdict["root_assembly_list"] = []
rdict["symtable_root"] = symtable_root
rdict['func_assembly_dict'] = {}

for statement in my_tree.body:
    rdict["this_func_name"] = None
    myast.postorder_walk(statement, visit_node, rdict)

print()
print_assembly_list(rdict['root_assembly_list'])
print()

for key in rdict['func_assembly_dict']:
    print(f'----FUNC: {key}----')
    print_assembly_list(rdict['func_assembly_dict'][key])
    print(f'----END {key}----')

