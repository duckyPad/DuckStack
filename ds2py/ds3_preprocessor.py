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

def single_pass(program_listing):
    loop_numbers = set()
    define_dict = {"TRUE":"1", "FALSE":"0"}
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
        print(line_obj)
        first_word = this_line.split()[0]
        if needs_rstrip(first_word):
            this_line = this_line.rstrip(" \t")

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

        if first_word == cmd_DEFINE:
            presult, pcomment = new_define(this_line, define_dict)
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
            presult, pcomment = PARSE_OK, ''
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
        
        if presult == PARSE_ERROR:
            # error_message = f"PARSE ERROR at Line {line_number_starting_from_1}: {this_line}\n{pcomment}"
            # print(error_message)
            return_dict['is_success'] = False
            return_dict['comments'] = pcomment
            return_dict['error_line_number_starting_from_1'] = line_number_starting_from_1
            return_dict['error_line_str'] = this_line
            return return_dict

    return_dict['is_success'] = True
    return_dict['comments'] = ""
    return_dict['error_line_number_starting_from_1'] = None
    return_dict['error_line_str'] = ""
    return_dict['define_dict'] = define_dict
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
    
    rdict = single_pass(program_listing)
    if rdict['is_success'] is False:
        return rdict
    
    


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

    run_all(program_listing)