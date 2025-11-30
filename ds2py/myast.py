import sys
import ast

def print_node_info(node):
	lineno = getattr(node, "lineno", None)
	print(f"---Line {lineno}: {type(node)}---")
	for item in node._fields:
		if getattr(node, item, None) is not None:
			print(f"{item}: {getattr(node, item, None)}")
	print()

AST_LEAF_NODES = (
	ast.Name,
)

def is_leaf(node):
	if isinstance(node, AST_LEAF_NODES):
		return True
	return not any(ast.iter_child_nodes(node))

def postorder_walk(node, action, goodies):
	if isinstance(node, ast.Expr):
		postorder_walk(node.value, action, goodies)
	elif isinstance(node, ast.BinOp):
		postorder_walk(node.left, action, goodies)
		postorder_walk(node.right, action, goodies)
		postorder_walk(node.op, action, goodies)
	elif isinstance(node, ast.BoolOp):
		for item in node.values:
			postorder_walk(item, action, goodies)
		postorder_walk(node.op, action, goodies)
	elif isinstance(node, ast.UnaryOp):
		postorder_walk(node.operand, action, goodies)
		postorder_walk(node.op, action, goodies)
	elif isinstance(node, ast.Compare):
		if len(node.comparators) > 1 or len(node.ops) > 1:
			raise ValueError("Multiple Comparators")
		postorder_walk(node.left, action, goodies)
		postorder_walk(node.comparators[0], action, goodies)
		postorder_walk(node.ops[0], action, goodies)
	elif isinstance(node, ast.Assign):
		postorder_walk(node.value, action, goodies)
		if len(node.targets) != 1:
			raise ValueError("Multiple Assignments")
		postorder_walk(node.targets[0], action, goodies)
	elif isinstance(node, ast.FunctionDef):
		raise ValueError("FunctionDef Node: Not Implemented")
	elif isinstance(node, ast.If):
		print_node_info(node)
		goodies['this_label'] = f"{node.__class__.__name__}@{getattr(node, "lineno", None)}"
		postorder_walk(node.test, action, goodies)
		action(node, goodies)
		for item in node.body:
			postorder_walk(item, action, goodies)
		for item in node.orelse:
			postorder_walk(item, action, goodies)
		action("NOP", goodies)
		# add labelled NOP here
	elif is_leaf(node):
		action(node, goodies)
	else:
		print_node_info(node)
		raise ValueError(f"Unknown AST Node")

"""
elif isinstance(node, ast.FunctionDef):
		arg_list = node.args.args
		print("FunctionDef Node: Not Implemented")
		print_node_info(node)
		for item in arg_list:
			print(item.__dict__)
		exit()

"""