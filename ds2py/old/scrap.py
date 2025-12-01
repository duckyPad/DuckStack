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


post_pp_listing = rdict["program_listing_with_indent_level"]
save_lines_to_file(post_pp_listing, "ppds.txt")
pyout = ds2py.run_all(post_pp_listing)
save_lines_to_file(pyout, "pyds.py")
# print_ds_line_list(pyout)
source = dsline_to_source(pyout)
tree = ast.parse(source, mode="exec")
# print(ast.dump(tree, indent=2))
#-------------

	if isinstance(node, ast.FunctionDef):
		print_node_info(node)
		arg_list = node.args.args
		# put function name in parent_info_dict, check for nested func def
		func_statements = node.body # lines inside function
		for item in arg_list:
			print_node_info(item)
		# exit()
              
    if isinstance(node, ast.Assign):
		"""
		node.targets is the variable to assign to
		resolve and add to instruction list, POPI32
		node.value is the right hand side
		print("ASSIGN!")
		print(node._fields)
		print(node.targets, node.value)
		"""
		# POPI32 instruction here
		postorder_walk(node.value, action, instruction_list, parent_history)
		

def visit_node(node, instruction_list, parent_info):
    # myast.print_node_info(node)
    print("hello", parent_info)


if isinstance(node, ast.Assign):
		# POPI32 instruction here
		# postorder_walk(node.value, action, instruction_list, parent_history)
		pass

# dont distingusih between left and right, treat case by case
def postorder_walk(node, action, instruction_list):
	print_node_info(node)
	if node is None:
		raise ValueError(f"Unknown AST Node")
	if isinstance(node, ast.BoolOp):
		for item in node.values:
			postorder_walk(item, action, instruction_list)
	if isinstance(node, ast.Call):
		for item in node.args:
			postorder_walk(item, action, instruction_list)
	if isinstance(node, ast.Assign):
		# walk the rest
		action(node, instruction_list)
		return
	if isinstance(node, ast.FunctionDef):
		print("FunctionDef Node: Not Implemented")
		exit()

	if is_leaf(node):
		action(node, instruction_list)
		return
	postorder_walk(get_left(node), action, instruction_list)
	postorder_walk(get_right(node), action, instruction_list)
	action(node, instruction_list)

def try_print_node(node):
	lineno = getattr(node, "lineno", None)
	print(f"---Line {lineno}: {type(node)}---")
	for item in node._fields:
		if getattr(node, item, None) is not None:
			print(f"{item}: {getattr(node, item, None)}")
	print()

def print_node_info(node):
	try:
		try_print_node(node)
	except:
		print(node)

# print(ast.dump(tree, indent=2))
# print_ds_line_list(pyout)

rdict["assembly_list"] = []
# rdict["func_assembly_dict"] = {}
# rdict["parent_history_list"] = []
		goodies['if_take_label'] = f"{node.__class__.__name__}_take@{this_orig_ds_lnum_sf1}"
	elif isinstance(node, ast.AugAssign):
		postorder_walk(node.target, action, goodies)
		postorder_walk(node.value, action, goodies)
		postorder_walk(node.op, action, goodies)