import sys
import ast

def print_node_info(node):
	lineno = getattr(node, "lineno", None)
	print(f"---Line {lineno}: {type(node)}---")
	for item in node._fields:
		if getattr(node, item, None) is not None:
			print(f"{item}: {getattr(node, item, None)}")
	print()

def get_right(node):
	if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
		return node.operand
	try:
		return node.right
	except:
		pass
	try:
		if len(node.comparators) > 1:
			return None
		return node.comparators[0]
	except:
		pass
	return None

def get_left(node):
	if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
		return ast.Constant(-1)
	return node.left

def is_leaf(node):
	if isinstance(node, ast.UnaryOp):
		return False
	return 'left' not in node.__dict__ and 'right' not in node.__dict__

def postorder_walk(node, action, instruction_list):
	if node is None:
		raise ValueError(f"Unknown AST Node")
	if isinstance(node, ast.BoolOp):
		for item in node.values:
			postorder_walk(item, action, instruction_list)
	if isinstance(node, ast.Call):
		for item in node.args:
			postorder_walk(item, action, instruction_list)
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
		postorder_walk(node.value, action, instruction_list)
	if isinstance(node, ast.FunctionDef):
		print_node_info(node)
		arg_list = node.args.args
		func_statements = node.body # lines inside function
		for item in arg_list:
			print_node_info(item)
		exit()

	if is_leaf(node):
		action(node, instruction_list)
		return
	postorder_walk(get_left(node), action, instruction_list)
	postorder_walk(get_right(node), action, instruction_list)
	action(node, instruction_list)

