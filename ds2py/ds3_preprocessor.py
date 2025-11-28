import sys
from dsvm_common import *

def needs_rstrip(first_word):
    return not (first_word.startswith(cmd_STRING) or first_word == cmd_OLED_PRINT)


valid_char_for_define_replacements = set([' ', '=', '+', '-', '*', '/', '%', '^', '>', '<', '!', '|', '(', ')', '&'])

def replace_DEFINE(pgm_line, dd):
    if pgm_line.startswith(cmd_STRING+" ") or pgm_line.startswith(cmd_STRINGLN+" "):
        dd.pop("TRUE", None)
        dd.pop("FALSE", None)
    else:
        dd['TRUE'] = 1
        dd['FALSE'] = 0
    dd_list_longest_first = sorted(list(dd.keys()), key=len, reverse=True)
    temp_line = f" {pgm_line} "
    for key in dd_list_longest_first:
        start_index = 0
        loop_count = 0
        while 1:
            loop_count += 1
            # hacky way to detect recursive DEFINE
            if loop_count > 127:
                return False, ""
            # print("start_index", start_index)
            key_location = str(temp_line).find(key, start_index)
            if key_location == -1:
                break
            # print(key, "still in:", temp_line, 'at location', key_location)
            letter_before = temp_line[key_location - 1]
            letter_after = temp_line[key_location + len(key)]
            # print("letter_before:", letter_before)
            # print("letter_after:", letter_after)
            if letter_before in valid_char_for_define_replacements and letter_after in valid_char_for_define_replacements:
                # print("STRING BEFORE", temp_line[:key_location])
                # print("STRING AFTER", temp_line[key_location + len(key):])
                temp_line = temp_line[:key_location] + str(dd[key]) + temp_line[key_location + len(key):]
            else:
                start_index = key_location + len(key)
    # print("AFTER REPLACEMENT:", temp_line)
    return True, temp_line[1:len(temp_line)-1]

def replace_delay_statements(pgm_line):
    first_word = pgm_line.split()[0]
    if first_word == cmd_DEFAULTDELAY:
        pgm_line = pgm_line.replace(cmd_DEFAULTDELAY, f"$_{cmd_DEFAULTDELAY} =")
        first_word = pgm_line.split()[0]
    elif first_word == cmd_DEFAULTCHARDELAY:
        pgm_line = pgm_line.replace(cmd_DEFAULTCHARDELAY, f"$_{cmd_DEFAULTCHARDELAY} =")
        first_word = pgm_line.split()[0]
    elif first_word == cmd_CHARJITTER:
        pgm_line = pgm_line.replace(cmd_CHARJITTER, f"$_{cmd_CHARJITTER} =")
        first_word = pgm_line.split()[0]
    return first_word, pgm_line

def skip_whitespace(pgm_line):
    whitespace_chars = [' ', '\t']
    search_index = len(cmd_DEFINE)
    try:
        while 1:
            this_char = pgm_line[search_index]
            if this_char in whitespace_chars:
                search_index += 1
            else:
                return search_index
    except Exception:
        return -1
    return -1

def is_valid_var_name(varname):
    if len(varname) == 0:
        return False, 'empty name'
    if varname[0].isnumeric():
        return False, "name can't begin with a number"
    for letter in varname:
        if letter not in valid_var_chars:
            return False, 'name contains invalid characters'
    return True, ''

def new_define(pgm_line, dd):
    define_source_start = skip_whitespace(pgm_line)
    if define_source_start == -1:
        return PARSE_ERROR, "DEFINE content not found"
    segments = pgm_line[define_source_start:].split(' ', 1)
    if len(segments) != 2:
        return PARSE_ERROR, "empty DEFINE"
    define_source = segments[0]
    define_destination = segments[1]
    is_valid, comment = is_valid_var_name(define_source)
    if is_valid is False:
        return PARSE_ERROR, comment
    if define_source in dd:
        return PARSE_ERROR, f"{define_source} is already defined"
    dd[define_source] = define_destination
    return PARSE_OK, ''

def check_loop(pgm_line):
    try:
        line_split = [x for x in pgm_line.split(cmd_LOOP) if len(x) > 0]
        if ':' not in line_split[0]:
            return PARSE_ERROR, 'missing ":"', None
        number_split = [x for x in line_split[0].split(":") if len(x) > 0]
        if len(number_split) != 1:
            return PARSE_ERROR, "wrong number of arguments", None
        return PARSE_OK, "", int(number_split[0])
    except Exception as e:
        return PARSE_ERROR, str(e), None

def new_rem_block_check(pgm_line, lnum, rbss, rbdict):
    if len(rbss) != 0:
        return PARSE_ERROR, "unmatched END_REM"
    rbss.append(lnum)
    rbdict[lnum] = None
    return PARSE_OK, ''

def new_stringln_block_check(pgm_line, lnum, slbss, slbdict):
    if len(slbss) != 0:
        return PARSE_ERROR, "unmatched END_STRINGLN"
    slbss.append(lnum)
    slbdict[lnum] = None
    # print("new_stringln_block_check:", slbss, slbdict)
    return PARSE_OK, ''

def new_string_block_check(pgm_line, lnum, sbss, sbdict):
    if len(sbss) != 0:
        return PARSE_ERROR, "unmatched END_STRING"
    sbss.append(lnum)
    sbdict[lnum] = None
    return PARSE_OK, ''

def new_func_check(pgm_line, lnum, fss, fdict):
    if len(fss) != 0:
        return PARSE_ERROR, "unmatched END_FUNCTION"
    if pgm_line.endswith(")") is False:
        return PARSE_ERROR, "missing )"
    try:
        fun_name = pgm_line.split()[1].split('(')[0]
    except Exception:
        return PARSE_ERROR, "invalid func name"
    if_valid_vn, vn_comment = is_valid_var_name(fun_name)
    if if_valid_vn is False:
        return PARSE_ERROR, vn_comment
    if fun_name in fdict:
        return PARSE_ERROR, "function already exists"
    try:
        all_args = pgm_line.split("(", 1)[-1].rsplit(")", 1)[0]
        # arg_list = [f"{FUNC_NAME_MANGLE_PREFIX}{fun_name}_{x.strip()}" for x in all_args.split(",")]
        arg_list = [x.strip() for x in all_args.split(",") if len(x.strip())]
    except Exception:
        return PARSE_ERROR, "Arg parse error"
    for arg in arg_list:
        is_valid, vn_comment = is_valid_var_name(arg)
        if is_valid is False:
            return PARSE_ERROR, vn_comment
    if len(arg_list) != len(set(arg_list)):
        return PARSE_ERROR, "Duplicate arg name"
    fss.append(fun_name)
    fdict[fun_name] = {"fun_start":lnum, 'fun_end':None, 'args':arg_list}
    return PARSE_OK, ''

def rem_block_end_check(pgm_line, lnum, rbss, rbdict):
    if len(rbss) == 0:
        return PARSE_ERROR, "orphan END_REM"
    if len(rbss) != 1:
        return PARSE_ERROR, "unmatched REM_BLOCK"
    rbdict[rbss.pop()] = lnum
    # print(pgm_line, lnum, rbss, rbdict)
    return PARSE_OK, ''

def stringln_block_end_check(pgm_line, lnum, slbss, slbdict):
    if len(slbss) == 0:
        return PARSE_ERROR, "orphan END_STRINGLN"
    if len(slbss) != 1:
        return PARSE_ERROR, "unmatched STRINGLN_BLOCK"
    slbdict[slbss.pop()] = lnum
    # print("stringln_block_end_check", lnum, slbss, slbdict)
    return PARSE_OK, ''

def string_block_end_check(pgm_line, lnum, sbss, sbdict):
    if len(sbss) == 0:
        return PARSE_ERROR, "orphan END_STRING"
    if len(sbss) != 1:
        return PARSE_ERROR, "unmatched STRING_BLOCK"
    sbdict[sbss.pop()] = lnum
    # print("stringln_block_end_check", lnum, sbss, sbdict)
    return PARSE_OK, ''

def func_end_check(pgm_line, lnum, fss, fdict):
    if len(fss) == 0:
        return PARSE_ERROR, "orphan END_FUNCTION"
    fun_name = fss.pop()
    fdict[fun_name]['fun_end'] = lnum
    return PARSE_OK, ''

def if_check(pgm_line, lnum, iss):
    if pgm_line.endswith(cmd_THEN) is False:
        return PARSE_ERROR, "missing THEN at end"
    if_expr = pgm_line.replace(cmd_IF, '', 1)
    if_expr = if_expr[:len(if_expr) - len(cmd_THEN)]
    iss.append({lnum:{"else_if":[], "else":None, "end_if":None}})
    return PARSE_OK, ''

def end_if_check(pgm_line, lnum, iss, if_skip_table, if_take_table, ifraw_list):
    if pgm_line != cmd_END_IF:
        return PARSE_ERROR, "missing END_IF at end"
    if len(iss) == 0:
        return PARSE_ERROR, "orphan END_IF"
    ifdict = iss.pop()
    if_root = list(ifdict.keys())[0]
    ifdict[if_root]['end_if'] = lnum
    ifdict[if_root]['else_if'] = sorted(ifdict[if_root]['else_if'])
    # print(ifdict)

    if_take_table[if_root] = ifdict[if_root]['end_if']
    # has no else_if and no else
    if len(ifdict[if_root]['else_if']) == 0 and ifdict[if_root]['else'] is None:
        # print("no else_if and no else")
        if_skip_table[if_root] = ifdict[if_root]['end_if']
    # only has else
    elif len(ifdict[if_root]['else_if']) == 0 and ifdict[if_root]['else'] is not None:
        # print("only has else")
        if_skip_table[if_root] = ifdict[if_root]['else']
    # only has else_if
    elif len(ifdict[if_root]['else_if']) > 0 and ifdict[if_root]['else'] is None:
        # print("only has else_if")
        cond_chain = [if_root] + ifdict[if_root]['else_if'] + [ifdict[if_root]['end_if']]
        # print(cond_chain)
        for index, item in enumerate(cond_chain[:-1]):
            if_skip_table[item] = cond_chain[index+1]
            if_take_table[item] = ifdict[if_root]['end_if']

    elif len(ifdict[if_root]['else_if']) > 0 and ifdict[if_root]['else'] is not None:
        # print("has both else and else_if")
        cond_chain = [if_root] + ifdict[if_root]['else_if'] + [ifdict[if_root]['else']] + [ifdict[if_root]['end_if']]
        # print(cond_chain)
        for index, item in enumerate(cond_chain[:-1]):
            if_skip_table[item] = cond_chain[index+1]
            if_take_table[item] = ifdict[if_root]['end_if']
    # print("if_skip_table", if_skip_table)
    # print("if_take_table", if_take_table)
    ifraw_list.append(ifdict)
    return PARSE_OK, ''

def elseif_check(pgm_line, lnum, iss):
    if pgm_line.endswith(cmd_THEN) is False:
        return PARSE_ERROR, "missing THEN"
    if len(iss) == 0:
        return PARSE_ERROR, "orphan ELSE IF"
    ifdict = iss[-1]
    for key in ifdict:
        if ifdict[key]['else'] is not None:
            return PARSE_ERROR, "ELSE IF must be before ELSE"
        ifdict[key]['else_if'].append(lnum)
    # print(ifdict)
    elseif_expr = pgm_line.replace(cmd_ELSE_IF, '', 1)
    elseif_expr = elseif_expr[:len(elseif_expr) - len(cmd_THEN)]
    return PARSE_OK, ''

def else_check(pgm_line, lnum, iss):
    if pgm_line != cmd_ELSE:
        return PARSE_ERROR, "extra stuff at end"
    if len(iss) == 0:
        return PARSE_ERROR, "orphan ELSE"
    ifdict = iss[-1]
    for key in ifdict:
        if ifdict[key]['else'] != None:
            return PARSE_ERROR, "unmatched ELSE"
        ifdict[key]['else'] = lnum
    # print(ifdict)
    return PARSE_OK, ''

def new_while_check(pgm_line, lnum, wss, wdict):
    wss.append(lnum)
    wdict[lnum] = None
    return PARSE_OK, ''

def end_while_check(pgm_line, lnum, wss, wdict):
    if pgm_line != cmd_END_WHILE:
        return PARSE_ERROR, "extra stuff at end"
    if len(wss) == 0:
        return PARSE_ERROR, "orphan END_WHILE"
    while_start_line = wss.pop()
    wdict[while_start_line] = lnum
    return PARSE_OK, '' 

def break_check(pgm_line, lnum, wss, bdict):
    split = [x for x in pgm_line.split(' ') if len(x) > 0]
    if len(split) != 1:
        return PARSE_ERROR, "extra stuff at end"
    if len(wss) == 0:
        return PARSE_ERROR, "BREAK outside WHILE"
    bdict[lnum] = wss[-1]
    return PARSE_OK, '' 

def continue_check(pgm_line, lnum, wss, cdict):
    split = [x for x in pgm_line.split(' ') if len(x) > 0]
    if len(split) != 1:
        return PARSE_ERROR, "extra stuff at end"
    if len(wss) == 0:
        return PARSE_ERROR, "CONTINUE outside WHILE"
    cdict[lnum] = wss[-1]
    return PARSE_OK, '' 

def is_within_rem_block(lnum, rbdict):
    for key in rbdict:
        if rbdict[key] is None:
            return lnum >= key
        if key <= lnum <= rbdict[key]:
            return True
    return False

def is_within_strlen_block(lnum, slbdict):
    for key in slbdict:
        if slbdict[key] is None:
            return True
        if key < lnum < slbdict[key]:
            return True
    return False

def is_within_str_block(lnum, sbdict):
    for key in sbdict:
        if sbdict[key] is None:
            return True
        if key < lnum < sbdict[key]:
            return True
    return False

def ensure_zero_arg(pgm_line):
    split = [x for x in pgm_line.split(' ') if len(x) > 0]
    if len(split) != 1:
        return PARSE_ERROR, "No args needed"
    return PARSE_OK, ''

def split_string(input_string, max_length=STRING_MAX_SIZE):
    if len(input_string) <= max_length:
        return [input_string]
    return [input_string[i:i+max_length] for i in range(0, len(input_string), max_length)]

def split_str_cmd(cmd_type, line_obj):
    str_content = line_obj.content.split(cmd_type + " ", 1)[-1]
    if len(str_content) <= STRING_MAX_SIZE:
        return [line_obj]
    cmd_list = []
    for item in split_string(str_content):
        new_obj = ds_line(content=f"{cmd_STRING} {item}", orig_lnum_sf1=line_obj.orig_lnum_sf1)
        cmd_list.append(new_obj)
    if cmd_type == cmd_STRINGLN:
        new_obj = ds_line(content=f"{cmd_ENTER}", orig_lnum_sf1=line_obj.orig_lnum_sf1)
        cmd_list.append(new_obj)
    return cmd_list

# this makes sure the code is suitable for converting into python
def single_pass(program_listing):
    loop_numbers = set()
    define_dict = {"TRUE":"1", "FALSE":"0"}
    func_table = {}
    if_take_table = {}
    if_skip_table = {}
    # line_number_starting_from_1 : end_while line number
    while_table = {}
    func_search_stack = []
    if_search_stack = []
    while_search_stack = []
    if_raw_info = []
    define_dict = {}
    break_dict = {}
    continue_dict = {}
    rem_block_search_stack = []
    rem_block_table = {}
    strlen_block_search_stack = []
    strlen_block_table = {}
    str_block_search_stack = []
    str_block_table = {}

    return_dict = {
    'is_success':False,
    'comments':"",
    'error_line_number_starting_from_1':None,
    'error_line_str':"",
    'define_dict':None,
    'loop_state_save_needed':False,
    'color_state_save_needed':False,
    'oled_restore_needed':False,
    'loop_size':None,
    }

    for line_obj in program_listing:
        line_number_starting_from_1 = line_obj.orig_lnum_sf1
        this_line = line_obj.content.lstrip(' \t')
        if len(this_line) == 0:
            continue
        first_word = this_line.split()[0]
        if needs_rstrip(first_word):
            this_line = this_line.rstrip(" \t")
        
        this_indent_level = len(if_search_stack) + len(func_search_stack) + len(while_search_stack)

        presult = PARSE_ERROR
        pcomment = f"empty comment"

        if first_word != cmd_DEFINE:
            is_success, replaced_str = replace_DEFINE(this_line, define_dict)
            if is_success is False:
                return_dict['is_success'] = False
                return_dict['comments'] = "Recursive DEFINE"
                return_dict['error_line_number_starting_from_1'] = line_number_starting_from_1
                return_dict['error_line_str'] = this_line
                return return_dict
            this_line = replaced_str

        first_word, this_line = replace_delay_statements(this_line)

        if first_word == cmd_END_REM:
            presult, pcomment = rem_block_end_check(this_line, line_number_starting_from_1, rem_block_search_stack, rem_block_table)
        elif is_within_rem_block(line_number_starting_from_1, rem_block_table):
            presult = PARSE_OK
            pcomment = ''
        elif first_word == cmd_END_STRINGLN:
            presult, pcomment = stringln_block_end_check(this_line, line_number_starting_from_1, strlen_block_search_stack, strlen_block_table)
        elif is_within_strlen_block(line_number_starting_from_1, strlen_block_table):
            presult = PARSE_OK
            pcomment = ''
        elif first_word == cmd_END_STRING:
            presult, pcomment = string_block_end_check(this_line, line_number_starting_from_1, str_block_search_stack, str_block_table)
        elif is_within_str_block(line_number_starting_from_1, str_block_table):
            presult = PARSE_OK
            pcomment = ''
        elif first_word == cmd_DEFINE:
            presult, pcomment = new_define(this_line, define_dict)
        elif first_word == cmd_FUNCTION:
            presult, pcomment = new_func_check(this_line, line_number_starting_from_1, func_search_stack, func_table)
        elif first_word == cmd_END_FUNCTION:
            this_indent_level -= 1
            presult, pcomment = func_end_check(this_line, line_number_starting_from_1, func_search_stack, func_table)
        elif first_word == cmd_IF:
            presult, pcomment = if_check(this_line, line_number_starting_from_1, if_search_stack)
        elif this_line.startswith(cmd_ELSE_IF):
            this_indent_level -= 1
            presult, pcomment = elseif_check(this_line, line_number_starting_from_1, if_search_stack)
        elif first_word == cmd_ELSE:
            this_indent_level -= 1
            presult, pcomment = else_check(this_line, line_number_starting_from_1, if_search_stack)
        elif first_word == cmd_END_IF:
            this_indent_level -= 1
            presult, pcomment = end_if_check(this_line, line_number_starting_from_1, if_search_stack, if_skip_table, if_take_table, if_raw_info)
        elif first_word == cmd_WHILE:
            presult, pcomment = new_while_check(this_line, line_number_starting_from_1, while_search_stack, while_table)
        elif first_word == cmd_END_WHILE:
            this_indent_level -= 1
            presult, pcomment = end_while_check(this_line, line_number_starting_from_1, while_search_stack, while_table)
        elif first_word == cmd_LOOP_BREAK:
            presult, pcomment = break_check(this_line, line_number_starting_from_1, while_search_stack, break_dict)
        elif first_word == cmd_CONTINUE:
            presult, pcomment = continue_check(this_line, line_number_starting_from_1, while_search_stack, continue_dict)
        elif first_word == cmd_REM_BLOCK:
            presult, pcomment = new_rem_block_check(this_line, line_number_starting_from_1, rem_block_search_stack, rem_block_table)
        elif first_word == cmd_STRINGLN_BLOCK:
            presult, pcomment = new_stringln_block_check(this_line, line_number_starting_from_1, strlen_block_search_stack, strlen_block_table)
        elif first_word == cmd_STRING_BLOCK:
            presult, pcomment = new_string_block_check(this_line, line_number_starting_from_1, str_block_search_stack, str_block_table)
        elif first_word == cmd_SWCC:
            return_dict['color_state_save_needed'] = True
            presult, pcomment = PARSE_OK, ''
        elif first_word == cmd_SWCF:
            return_dict['color_state_save_needed'] = True
            presult, pcomment = PARSE_OK, ''
        elif first_word == cmd_SWCR:
            return_dict['color_state_save_needed'] = True
            presult, pcomment = PARSE_OK, ''
        elif first_word == cmd_OLED_UPDATE:
            return_dict['oled_restore_needed'] = True
            presult, pcomment = ensure_zero_arg(this_line)
        elif first_word == cmd_OLED_BLANK:
            presult, pcomment = ensure_zero_arg(this_line)
        elif first_word == cmd_OLED_RESTORE:
            presult, pcomment = ensure_zero_arg(this_line)
        elif first_word == cmd_BCLR:
            presult, pcomment = ensure_zero_arg(this_line)
        elif first_word == cmd_NEXT_PROFILE:
            presult, pcomment = ensure_zero_arg(this_line)
        elif first_word == cmd_PREV_PROFILE:
            presult, pcomment = ensure_zero_arg(this_line)
        elif first_word == cmd_DP_SLEEP:
            presult, pcomment = ensure_zero_arg(this_line)
        elif this_line.startswith(cmd_SWCOLOR):
            return_dict['color_state_save_needed'] = True
            presult, pcomment = PARSE_OK, ''
        elif this_line.startswith(cmd_LOOP):
            presult, pcomment, value = check_loop(this_line)
            if value is not None:
                return_dict['loop_state_save_needed'] = True
                loop_numbers.add(value)
        else:
             presult, pcomment = PARSE_OK, ''

        if this_indent_level < 0:
            presult, pcomment = PARSE_ERROR, "Invalid indent level"
        
        line_obj.indent_level = this_indent_level
        
        if presult == PARSE_ERROR:
            # error_message = f"PARSE ERROR at Line {line_number_starting_from_1}: {this_line}\n{pcomment}"
            # print(error_message)
            return_dict['is_success'] = False
            return_dict['comments'] = pcomment
            return_dict['error_line_number_starting_from_1'] = line_number_starting_from_1
            return_dict['error_line_str'] = this_line
            return return_dict
        
    # ----------
    
    if len(if_search_stack) != 0:
        return_dict['is_success'] = False
        # return_dict['comments'] = f"END_IF missing for IF at line {list(if_search_stack[0].keys())[0]}"
        return_dict['comments'] = "Missing END_IF"
        return_dict['error_line_number_starting_from_1'] = list(if_search_stack[0].keys())[0]
        return return_dict

    if len(func_search_stack) != 0:
        return_dict['is_success'] = False
        # return_dict['comments'] = f"END_FUNCTION missing for FUNCTION {func_search_stack[0]}() at line {func_table[func_search_stack[0]]['fun_start']}"
        return_dict['comments'] = "Missing END_FUNCTION"
        return_dict['error_line_number_starting_from_1'] = func_table[func_search_stack[0]]['fun_start']
        return return_dict

    if len(while_search_stack) != 0:
        return_dict['is_success'] = False
        # return_dict['comments'] = f"END_WHILE missing for WHILE at line {while_search_stack[-1]}"
        return_dict['comments'] = "Missing END_WHILE"
        return_dict['error_line_number_starting_from_1'] = while_search_stack[-1]
        return return_dict

    for key in rem_block_table:
        if rem_block_table[key] is None:
            return_dict['is_success'] = False
            return_dict['comments'] = "Missing END_REM"
            return_dict['error_line_number_starting_from_1'] = key
            return_dict['error_line_str'] = ""
            return return_dict

    for key in strlen_block_table:
        if strlen_block_table[key] is None:
            return_dict['is_success'] = False
            return_dict['comments'] = "Missing END_STRINGLN"
            return_dict['error_line_number_starting_from_1'] = key
            return_dict['error_line_str'] = ""
            return return_dict

    for key in str_block_table:
        if str_block_table[key] is None:
            return_dict['is_success'] = False
            return_dict['comments'] = "Missing END_STRING"
            return_dict['error_line_number_starting_from_1'] = key
            return_dict['error_line_str'] = ""
            return return_dict
    # ----------

    return_dict['is_success'] = True
    return_dict['comments'] = ""
    return_dict['error_line_number_starting_from_1'] = None
    return_dict['error_line_str'] = ""
    return_dict['define_dict'] = define_dict
    return_dict['func_table'] = func_table
    return_dict['if_take_table'] = if_take_table
    return_dict['if_skip_table'] = if_skip_table
    return_dict['break_dict'] = break_dict
    return_dict['continue_dict'] = continue_dict
    return_dict['rem_block_table'] = rem_block_table
    return_dict['strlen_block_table'] = strlen_block_table
    return_dict['str_block_table'] = str_block_table
    return_dict['program_listing_with_indent_level'] = program_listing

    if len(loop_numbers) > 0:
        return_dict['loop_size'] = max(loop_numbers)
    
    return return_dict

def search_profile_index_from_name(query, profile_list):
    if profile_list is None:
        return None
    for index, item in enumerate(profile_list):
        if query.lower().strip() == item.name.lower().strip():
            return index
    return None

def run_all(program_listing, profile_list=None):
    new_program_listing = []
    for line_obj in program_listing:
        first_word = line_obj.content.lstrip(" \t").split(" ")[0]

        # parse GOTO_PROFILE commands
        if first_word == cmd_GOTO_PROFILE_NAME:
            line_obj.content = line_obj.content.replace(cmd_GOTO_PROFILE_NAME, cmd_GOTO_PROFILE, 1)
            first_word = cmd_GOTO_PROFILE

        if first_word == cmd_GOTO_PROFILE:
            target_profile_name = line_obj.content.split(cmd_GOTO_PROFILE, 1)[-1].strip()
            target_profile_index_0_indexed = search_profile_index_from_name(target_profile_name, profile_list)
            if target_profile_index_0_indexed is not None:
                line_obj.content = f"{cmd_GOTO_PROFILE} {target_profile_index_0_indexed + 1}"

        new_program_listing.append(line_obj)

    program_listing = new_program_listing

    # ----------- expand STRING_BLOCK and STRINGLN_BLOCK, split STRING and STRINGLN ----------

    rdict = single_pass(program_listing)
    if rdict['is_success'] is False:
        return rdict
    
    new_program_listing = []
    for line_obj in program_listing:
        line_number_starting_from_1 = line_obj.orig_lnum_sf1

        if is_within_strlen_block(line_number_starting_from_1, rdict['strlen_block_table']):
            line_obj.content = "STRINGLN " + line_obj.content
        elif is_within_str_block(line_number_starting_from_1, rdict['str_block_table']):
            line_obj.content = "STRING " + line_obj.content
        else:
            line_obj.content = line_obj.content.lstrip(' \t')

        if len(line_obj.content) == 0:
            continue

        first_word = line_obj.content.split(" ")[0]
        first_word, line_obj.content = replace_delay_statements(line_obj.content)

        if first_word in [cmd_STRINGLN_BLOCK, cmd_END_STRINGLN, cmd_STRING_BLOCK, cmd_END_STRING]:
            continue

        if first_word in [cmd_STRINGLN, cmd_STRING]:
            for item in split_str_cmd(first_word, line_obj):
                new_program_listing.append(item)
        else:
            new_program_listing.append(line_obj)

    program_listing = new_program_listing

    # ---------------------
    new_program_listing = []
    for line_obj in program_listing:
        # remove leading space and tabs
        line_obj.content = line_obj.content.lstrip(" \t")
        first_word = line_obj.content.split(" ")[0]

        # remove single-line comments 
        if first_word == cmd_REM or first_word.startswith(cmd_C_COMMENT):
            continue

        # remove INJECT_MOD
        if first_word == cmd_INJECT_MOD:
            line_obj.content = line_obj.content.replace(cmd_INJECT_MOD, "", 1)

        line_obj.content = line_obj.content.lstrip(" \t")
        new_program_listing.append(line_obj)

    program_listing = new_program_listing

    rdict = single_pass(program_listing)
    if rdict['is_success'] is False:
        return rdict

    print("---------First Pass OK!---------")

    # ----- Second Pass -------------

    second_pass_program_listing = []
    needs_end_if = False

    epilogue = 0
    if rdict['loop_state_save_needed']:
        epilogue |= 0x1
    if rdict['color_state_save_needed']:
        epilogue |= 0x2
    if rdict['oled_restore_needed']:
        epilogue |= 0x4
    # 0x8 is disable_autorepeat, generated on duckypad itself
    # 0x10 is pgv_save_needed, generated on duckypad itself

    if epilogue != 0:
        second_pass_program_listing.append(ds_line(content=f"$_NEEDS_EPILOGUE = {epilogue}"))
    if rdict['loop_size'] is not None:
        second_pass_program_listing.append(ds_line(content=f"$_LOOP_SIZE = {rdict['loop_size']+1}"))
    
    for line_obj in program_listing:
        line_number_starting_from_1 = line_obj.orig_lnum_sf1
        this_line = line_obj.content.lstrip(' \t')
        rdict['error_line_number_starting_from_1'] = line_number_starting_from_1
        rdict['error_line_str'] = this_line
        if len(this_line) == 0:
            continue
        first_word = this_line.split(" ")[0]
        if is_within_rem_block(line_number_starting_from_1, rdict['rem_block_table']):
            continue
        if needs_rstrip(first_word):
            line_obj.content = this_line.rstrip(" \t")
        if first_word == cmd_REM or this_line.startswith(cmd_C_COMMENT):
            continue
        if first_word != cmd_DEFINE:
            is_success, replaced_str = replace_DEFINE(this_line, rdict['define_dict'])
            if is_success is False:
                rdict['is_success'] = False
                rdict['comments'] = "Recursive DEFINE"
                return rdict
            else:
                line_obj.content = replaced_str
        else:
            continue

        if first_word == cmd_REPEAT:
            if len(second_pass_program_listing) == 0:
                rdict['is_success'] = False
                rdict['comments'] = "Nothing before REPEAT"
                return rdict
            try:
                repeat_count = int(this_line[len(cmd_REPEAT):].strip())
                if repeat_count > REPEAT_MAX_SIZE:
                    raise ValueError
            except Exception as e:
                rdict['is_success'] = False
                rdict['comments'] = "Invalid REPEAT count"
                return rdict
            last_line = second_pass_program_listing[-1]
            for x in range(repeat_count):
                second_pass_program_listing.append(last_line)
        elif this_line.startswith(cmd_LOOP):
            presult, pcomment, value = check_loop(this_line)
            if needs_end_if:
                second_pass_program_listing.append(ds_line(cmd_END_IF, line_number_starting_from_1))
            loop_str = f'{cmd_IF} $_KEYPRESS_COUNT % $_LOOP_SIZE == {value} {cmd_THEN}'
            second_pass_program_listing.append(ds_line(loop_str, line_number_starting_from_1))
            needs_end_if = True
        else:
            second_pass_program_listing.append(line_obj)
        
    if needs_end_if:
        second_pass_program_listing.append(ds_line(cmd_END_IF, line_number_starting_from_1))

    final_dict = single_pass(second_pass_program_listing)
    print(final_dict)
    second_pass_program_listing = final_dict['program_listing_with_indent_level']

    for item in second_pass_program_listing:
        final_str = "    "*item.indent_level + item.content
        print(final_str)

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

    result = run_all(program_listing)
    print(result)