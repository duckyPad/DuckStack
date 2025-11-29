import sys
import ast

def print_node_info(node):
	lineno = getattr(node, "lineno", None)
	print(f"---Line {lineno}: {type(node)}---")
	for item in node._fields:
		if getattr(node, item, None) is not None:
			print(f"{item}: {getattr(node, item, None)}")
	print()

def is_leaf(node):
    return not any(ast.iter_child_nodes(node))

def postorder_walk(node, action, instruction_list):
	print_node_info(node)
	if isinstance(node, ast.Expr):
		postorder_walk(node.value, action, instruction_list)
	elif isinstance(node, ast.BinOp):
		postorder_walk(node.left, action, instruction_list)
		postorder_walk(node.right, action, instruction_list)
		postorder_walk(node.op, action, instruction_list)
	elif is_leaf(node):
		action(node, instruction_list)
	else:
		raise ValueError(f"Unknown AST Node")
