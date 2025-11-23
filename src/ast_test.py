import ast

source = """
def add(a, b):
	return a+b

foo = 3
bar = 5
add(foo, bar)
"""

tree = ast.parse(source, mode="exec")
print(ast.dump(tree, indent=2))