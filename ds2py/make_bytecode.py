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

def my_action(node, instruction_list):
    print(node, instruction_list)

for statement in tree.body:
    myast.postorder_walk(statement, my_action, None)