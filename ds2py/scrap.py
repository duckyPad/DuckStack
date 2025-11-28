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