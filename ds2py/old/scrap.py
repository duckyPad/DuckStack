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