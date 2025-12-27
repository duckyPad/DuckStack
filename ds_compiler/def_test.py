import re

cmd_STRING = "STRING"
cmd_STRINGLN = "STRINGLM"

def replace_DEFINE_once(pgm_line, def_dict):
    if pgm_line.startswith(cmd_STRING+" ") or pgm_line.startswith(cmd_STRINGLN+" "):
        def_dict.pop("TRUE", None)
        def_dict.pop("FALSE", None)
    else:
        def_dict['TRUE'] = 1
        def_dict['FALSE'] = 0
    def_dict_list_longest_first = sorted(list(def_dict.keys()), key=len, reverse=True)
    for key in def_dict_list_longest_first:
        value = str(def_dict[key])
        pattern = r'\b' + re.escape(key) + r'\b'
        pgm_line = re.sub(pattern, value, pgm_line)
    return pgm_line

def replace_DEFINE(source, def_dict):
    last_source = ""
    iterations = 0
    max_iterations = len(def_dict) + 1
    while last_source != source:
        if iterations > max_iterations:
            return False, ""
        last_source = source
        source = replace_DEFINE_once(source, def_dict)
        iterations += 1
    return True, source

dd = {'ORANGE': 'APPLE', 'APPLE': 'ORANGE'}
line = "I LIKE APPLE"
result = replace_DEFINE(line, dd)
print(result)