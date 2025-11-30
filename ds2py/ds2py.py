import sys
from dsvm_common import *
import ds3_preprocessor
import copy

def make_dspy_func_name(cmd_name):
    DS_FUN_PREFIX = "DSFN_"
    return f"{DS_FUN_PREFIX}{cmd_name}"

def make_func_string(first_word, this_line):
    str_content = this_line[len(first_word)+1:]
    fun_name = make_dspy_func_name(first_word)
    return f"{fun_name}({repr(str_content)})"

def make_func_with_args(first_word, this_line):
    args = this_line[len(first_word)+1:].strip().split(" ")
    final_str = make_dspy_func_name(first_word) + "("
    for item in args:
        final_str += f"{item}, "
    final_str = final_str.rstrip(", ") + ")"
    return final_str

def replace_operators(this_line):
    return this_line.replace("$", "").replace("||", " or ").replace("&&", " and ")

def run_all(program_listing):
    new_listing = []
    for line_obj in program_listing:
        line_obj.content = line_obj.content.lstrip(' \t')
        first_word = line_obj.content.split()[0]

        if first_word == cmd_VAR_DECLARE:
            line_obj.content = line_obj.content[len(cmd_VAR_DECLARE):].strip()
        if first_word not in ds_string_funcs:
            line_obj.content = replace_operators(line_obj.content)

        this_line = line_obj.content

        if first_word in ds_string_funcs:
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = make_func_string(first_word, this_line)
            new_listing.append(new_obj)
        elif first_word in ds_func_arg_lookup:
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = make_func_with_args(first_word, this_line)
            new_listing.append(new_obj)
        elif first_word == cmd_IF:
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = f"if {this_line[len(cmd_IF):len(this_line)-len(cmd_THEN)].strip()}:"
            new_listing.append(new_obj)
        elif this_line.startswith(f"{cmd_ELSE_IF} "):
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = f"elif {this_line[len(cmd_ELSE_IF):len(this_line)-len(cmd_THEN)].strip()}:"
            new_listing.append(new_obj)
        elif first_word == cmd_ELSE:
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = "else:"
            new_listing.append(new_obj)
        elif first_word in ds2py_ignored_cmds:
            continue
        elif first_word == cmd_WHILE:
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = f"while {this_line[len(cmd_WHILE):].strip()}:"
            new_listing.append(new_obj)
        elif first_word == cmd_FUNCTION:
            new_obj = copy.deepcopy(line_obj)
            new_obj.content = f"def {this_line[len(cmd_FUNCTION):].strip()}:"
            new_listing.append(new_obj)
        else:
            new_listing.append(line_obj)
    for index, line_obj in enumerate(new_listing):
        line_obj.py_lnum_sf1 = index+1
    return new_listing

if __name__ == "__main__":
    # Require at least input and output arguments
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

    post_pp_listing = rdict["dspp_listing_with_indent_level"]
    # print_ds_line_list(post_pp_listing)
    pyout = run_all(post_pp_listing)

    print_ds_line_list(pyout)