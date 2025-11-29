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

# CPU instructions
OP_VMVER = ("VMVER", 255)
OP_NOP = ("NOP", 0)
OP_PUSHC16 = ("PUSHC16", 1)
OP_PUSHI32 = ("PUSHI32", 2)
OP_PUSHR32 = ("PUSHR32", 3)
OP_POPI32 = ("POPI32", 4)
OP_POPR32 = ("POPR32", 5)
OP_BRZ = ("BRZ", 6)
OP_JMP = ("JMP", 7)
OP_CALL = ("CALL", 8)
OP_RET = ("RET", 9)
OP_HALT = ("HALT", 10)
# to be resolved into PUSHI32 or PUSHR32 depending on variable type
OP_PUSH32_DUMMY = ("PUSHD32", 11)
OP_POP32_DUMMY = ("PUSHD32", 12)

# Binary Operators
OP_EQ = ("EQ", 32)
OP_NOTEQ = ("NOTEQ", 33)
OP_LT = ("LT", 34)
OP_LTE = ("LTE", 35)
OP_GT = ("GT", 36)
OP_GTE = ("GTE", 37)
OP_ADD = ("ADD", 38)
OP_SUB = ("SUB", 39)
OP_MULT = ("MULT", 40)
OP_DIV = ("DIV", 41)
OP_MOD = ("MOD", 42)
OP_POW = ("POW", 43)
OP_LSHIFT = ("LSHIFT", 44)
OP_RSHIFT = ("RSHIFT", 45)
OP_BITOR = ("BITOR", 46)
OP_BITXOR = ("BITXOR", 47)
OP_BITAND = ("BITAND", 48)
OP_LOGIAND = ("LOGIAND", 49)
OP_LOGIOR = ("LOGIOR", 50)

# Unary Operators
OP_BITINV = ("BITINV", 55)
OP_LOGINOT = ("LOGINOT", 56)
OP_USUB = ("USUB", 57)

# duckyScript Commands
OP_DELAY = ("DELAY",64)
OP_KUP = ("KUP",65)
OP_KDOWN = ("KDOWN",66)
OP_MSCL = ("MSCL",67)
OP_MMOV = ("MMOV",68)
OP_SWCF = ("SWCF",69)
OP_SWCC = ("SWCC",70)
OP_SWCR = ("SWCR",71)
OP_STR = ("STR",72)
OP_STRLN = ("STRLN",73)
OP_OLED_CUSR = ("OLED_CUSR",74)
OP_OLED_PRNT = ("OLED_PRNT",75)
OP_OLED_UPDE = ("OLED_UPDE",76)
OP_OLED_CLR = ("OLED_CLR",77)
OP_OLED_REST = ("OLED_REST",78)
OP_BCLR = ("BCLR",79)
OP_PREVP = ("PREVP",80)
OP_NEXTP = ("NEXTP",81)
OP_GOTOP = ("GOTOP",82)
OP_SLEEP = ("SLEEP",83)
OP_OLED_LINE = ("OLED_LINE",84)
OP_OLED_RECT = ("OLED_RECT",85)
OP_OLED_CIRC = ("OLED_CIRC",86)

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

def get_empty_instruction(orig_lnum_sf1=None, py_lnum_sf1=None):
    return {
    'opcode':OP_NOP,
    'oparg':None,
    'label':None,
    'comment':None,
    'addr':None,
    'orig_lnum_sf1':orig_lnum_sf1,
    'py_lnum_sf1':py_lnum_sf1,
    }

def print_instruction(instruction):
    if instruction['label'] is not None:
        print(f"~~~~{instruction['label']}:")

    if instruction['addr'] is not None:
        print(str(instruction['addr']).ljust(5), end='')
    print(instruction['opcode'][0].ljust(10), end='')
    tempstr = ""
    if instruction['oparg'] is not None:
        tempstr = f"{instruction['oparg']}".ljust(6)
        if isinstance(instruction['oparg'], int):
            tempstr += f"{hex(instruction['oparg'])}".ljust(6)
    print(tempstr.ljust(20), end='')
    tempstr = ""
    if instruction['comment'] is not None:
        tempstr = ";" + str(instruction['comment'])
    print(tempstr)

def print_asslist(lll):
    print()
    for item in lll:
        print_instruction(item)
    print()

def make_instruction_pushc32(value):
    node_value_high = (int(value) & 0xffff0000) >> 16
    node_value_low = int(value) & 0xffff
    inst_list = []
    this_instruction = get_empty_instruction()
    this_instruction['opcode'] = OP_PUSHC16
    this_instruction['oparg'] = node_value_low
    inst_list.append(this_instruction)
    if node_value_high:
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['oparg'] = node_value_high
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_PUSHC16
        this_instruction['oparg'] = 16
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_LSHIFT
        inst_list.append(this_instruction)
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_BITOR
        inst_list.append(this_instruction)
    return inst_list

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

rdict = ds3_preprocessor.run_all(program_listing)

if rdict['is_success'] is False:
    print("Preprocessing failed!")
    print(f"\t{rdict['comments']}")
    print(f"\tLine {rdict['error_line_number_starting_from_1']}: {rdict['error_line_str']}")
    exit()

post_pp_listing = rdict["program_listing_with_indent_level"]
save_lines_to_file(post_pp_listing, "ppds.txt")
pyout = ds2py.run_all(post_pp_listing)
save_lines_to_file(pyout, "pyds.py")
source = dsline_to_source(pyout)
tree = ast.parse(source, mode="exec")
# print(ast.dump(tree, indent=2))

AST_ARITH_NODES = (
    ast.operator,
    ast.cmpop,
    ast.boolop,
    ast.unaryop,
)

def visit_node(node, instruction_list):
    print("at leaf:", node)
    if isinstance(node, ast.Name):
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = OP_PUSH32_DUMMY
        this_instruction['oparg'] = str(node.id)
        instruction_list.append(this_instruction)
    elif isinstance(node, ast.Constant):
        instruction_list += make_instruction_pushc32(node.value)
    elif isinstance(node, AST_ARITH_NODES):
        op_name = node.__class__.__name__
        if op_name not in arith_lookup:
            raise ValueError("unknown operation")
        this_instruction = get_empty_instruction()
        this_instruction['opcode'] = arith_lookup[op_name]
        instruction_list.append(this_instruction)
    else:
        raise ValueError("Unknown leaf node:", node)

instruction_list = []
for statement in tree.body:
    myast.postorder_walk(statement, visit_node, instruction_list)

print_asslist(instruction_list)