import ast

source = """
def draw_ball():
FUNCTION add(a, b)
END_FUNCTION

FUNCTION sub(a, b)
END_FUNCTION

add(2, 3)
"""

tree = ast.parse(source, mode="exec")
print(ast.dump(tree, indent=2))