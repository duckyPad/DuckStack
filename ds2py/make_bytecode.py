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

def make_instruction_pushc32(value, comment: str = ""):
    node_value_high = (int(value) & 0xFFFF0000) >> 16
    node_value_low  = int(value) & 0xFFFF

    inst_list: list[dsvm_instruction] = []

    # low 16
    inst_list.append(dsvm_instruction(opcode=OP_PUSHC16, payload=node_value_low, comment=comment))

    # if high 16 is non-zero, build (high << 16) | low
    if node_value_high:
        inst_list.append(dsvm_instruction(opcode=OP_PUSHC16, payload=node_value_high, comment=comment))
        inst_list.append(dsvm_instruction(opcode=OP_PUSHC16, payload=16, comment=comment))
        inst_list.append(dsvm_instruction(opcode=OP_LSHIFT, comment=comment))
        inst_list.append(dsvm_instruction(opcode=OP_BITOR, comment=comment))

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
    og_index_sf0 = None
    for line_obj in rdict['ds2py_listing']:
        if line_obj.py_lnum_sf1 == this_pylnum_sf1:
            og_index_sf0 = line_obj.orig_lnum_sf1 - 1
    if og_index_sf0 is None:
        return ""
    return rdict['orig_listing'][og_index_sf0].content

def search_in_symtable(name: str, table: symtable.SymbolTable):
    try:
        return table.lookup(name)
    except KeyError:
        return None

def is_known_global(name: str, goodies) -> bool:
    root_table = goodies["symtable_root"]
    if name in goodies["user_declared_var_table"]:
        return True
    if name in root_table.get_identifiers():
        return True
    return False

def classify_name(name: str, current_function: str | None, goodies) -> int:
    if keyword.iskeyword(name):
        raise ValueError(f'"{name}" invalid variable name')
    
    if name in internal_variable_dict:
        return SymType.RESERVED_VAR
    
    root_table = goodies["symtable_root"]

    if current_function is not None:
        this_table = myast.find_function_table(root_table, current_function)
        if this_table is None:
            raise ValueError(f"No symtable for {current_function!r}()")

        sym = search_in_symtable(name, this_table)
        if sym is not None:
            if sym.is_parameter():
                return SymType.FUNC_ARG

            if sym.is_local() and sym.is_assigned():
                return SymType.FUNC_LOCAL_VAR

            # referenced from this function but resolved outside it
            if sym.is_global() or sym.is_declared_global() or sym.is_free() or sym.is_nonlocal():
                if is_known_global(name, goodies):
                    return SymType.GLOBAL_VAR
                raise ValueError(f'Undefined symbol "{name}" (referenced in "{current_function}()")')

    if is_known_global(name, goodies):
        return SymType.GLOBAL_VAR
        
    raise ValueError(f'Unknown symbol "{name}" in function "{current_function}()"')

def visit_name_node(node, goodies, inst_list):
    og_ds_line = goodies["og_ds_line"]
    current_function = goodies["this_func_name"]

    node_name = node.id
    sym_type = classify_name(node.id, current_function, goodies)
    # print("symtype:", node.id, current_function, sym_type.name)

    vi_func = current_function
    if sym_type in [SymType.GLOBAL_VAR, SymType.RESERVED_VAR]:
        vi_func = None
    this_var_info = var_info(node_name, sym_type, vi_func)
    goodies['var_info_set'].add(this_var_info)

    if isinstance(node.ctx, ast.Store):
        opcode = OP_POPR if sym_type == SymType.FUNC_ARG else OP_POPI
        inst_list.append(dsvm_instruction(opcode=opcode, payload=node_name, comment=og_ds_line, parent_func=current_function, var_type=sym_type))
        return

    if isinstance(node.ctx, ast.Load):
        opcode = OP_PUSHR if sym_type == SymType.FUNC_ARG else OP_PUSHI
        inst_list.append(dsvm_instruction(opcode=opcode, payload=node_name, comment=og_ds_line, parent_func=current_function, var_type=sym_type))

def visit_node(node, goodies):
    current_function = goodies.get("this_func_name")

    # Pick the right instruction list (root vs function)
    if current_function is None:
        instruction_list = goodies["root_assembly_list"]
    else:
        instruction_list = goodies["func_assembly_dict"].setdefault(current_function, [])

    og_ds_line = get_orig_ds_line_from_py_lnum(goodies, getattr(node, "lineno", None))
    goodies["og_ds_line"] = og_ds_line

    def emit(opcode, payload=None, label=None):
        instruction_list.append(
            dsvm_instruction(opcode=opcode, payload=payload, label=label, comment=og_ds_line)
        )

    if isinstance(node, ast.Name):
        visit_name_node(node, goodies, instruction_list)

    elif isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            emit(OP_PUSHSTR, payload=node.value)
        elif isinstance(node.value, int):
            # assumes make_instruction_pushc32 now returns list[dsvm_instruction]
            instruction_list.extend(make_instruction_pushc32(node.value, og_ds_line))
        else:
            raise ValueError("Unknown type:", type(node.value))

    elif isinstance(node, AST_ARITH_NODES):
        op_name = node.__class__.__name__
        if op_name not in arith_lookup:
            raise ValueError("unknown operation")
        emit(arith_lookup[op_name])

    elif isinstance(node, ast.If):
        emit(OP_BRZ, payload=goodies["if_destination_label"])

    elif isinstance(node, ast.While):
        emit(OP_BRZ, payload=goodies["while_end_label"])

    elif isinstance(node, ast.Continue):
        emit(OP_JMP, payload=goodies["while_start_label"])

    elif isinstance(node, ast.Break):
        emit(OP_JMP, payload=goodies["while_end_label"])

    elif isinstance(node, ast.Call):
        func_name = node.func.id
        if func_name in ds_reserved_funcs:
            emit(ds_reserved_funcs[func_name][0])
        else:
            emit(OP_CALL, payload=f"func_{func_name}")

    elif isinstance(node, ast.Return):
        arg_count = myast.how_many_args(current_function, goodies["symtable_root"])
        if arg_count is None:
            raise ValueError("Invalid arg count")
        emit(OP_RET, payload=arg_count)

    elif isinstance(node, myast.add_nop):
        emit(OP_NOP, label=node.label)

    elif isinstance(node, myast.add_jmp):
        emit(OP_JMP, payload=node.label)

    elif isinstance(node, myast.add_push0):
        emit(OP_PUSHC16, payload=0, label=node.label)

    elif isinstance(node, myast.add_default_return):
        emit(OP_RET, payload=node.arg_count)

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

def compile_to_bin(rdict):
    final_assembly_list = []

    print()
    print_assembly_list(rdict['root_assembly_list'])
    print()

    for key in rdict['func_assembly_dict']:
        print(f'----FUNC: {key}----')
        print_assembly_list(rdict['func_assembly_dict'][key])
        print(f'----END {key}----')

    """
    dump everything into one list
    first main code, then func code

    go through each instruction:
        collect all global variables, assign address to them
        collect all strings, deduplicate, process, generate address
        look at variables, figure out arg position and local var ordering

    """
    for item in rdict['var_info_set']:
        print(item)



# --------------------------

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

# print(rdict['user_declared_var_table'])
# exit()

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
rdict['var_info_set'] = set()

for statement in my_tree.body:
        rdict["this_func_name"] = None
        myast.postorder_walk(statement, visit_node, rdict)

# try:
#     for statement in my_tree.body:
#         rdict["this_func_name"] = None
#         myast.postorder_walk(statement, visit_node, rdict)
# except Exception as e:
#     print(f"Line {rdict["latest_orig_ds_lnum_sf1"]}: {e}")
#     exit()


compile_to_bin(rdict)