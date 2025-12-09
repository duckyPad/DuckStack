import sys
import ast
import symtable
from dsvm_common import *

import symtable

def find_function_table(root: symtable.SymbolTable, func_name: str):
    for child in root.get_children():
        if child.get_type() == 'function' and child.get_name() == func_name:
            return child
        found = find_function_table(child, func_name)
        if found is not None:
            return found
    return None

def get_func_parameters(func_name: str, root: symtable.SymbolTable):
    func_table = find_function_table(root, func_name)
    if func_table is None:
        return None
    # returns a tuple of parameter names
    return func_table.get_parameters()

def how_many_args(name: str, table: symtable.SymbolTable):
    params = get_func_parameters(name, table)
    if params is None:
        return None
    return len(params)

def get_orig_ds_lnumsf1_from_py_lnumsf1(rdict, this_pylnum_sf1):
    if this_pylnum_sf1 is None:
        return None
    og_index_sf1 = None
    for line_obj in rdict['ds2py_listing']:
        if line_obj.py_lnum_sf1 == this_pylnum_sf1:
            og_index_sf1 = line_obj.orig_lnum_sf1
    return og_index_sf1

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

@dataclass(frozen=True, slots=True)
class add_alloc:
    func_name : str = ""

@dataclass(frozen=True, slots=True)
class add_nop:
    label: str = ""

@dataclass(frozen=True, slots=True)
class add_jmp:
    label: str = ""

@dataclass(frozen=True, slots=True)
class add_push0:
    label: str = ""

@dataclass(frozen=True, slots=True)
class add_default_return:
    arg_count: int = 0

def is_leaf(node):
    if isinstance(node, AST_LEAF_NODES):
        return True
    return not any(ast.iter_child_nodes(node))

def postorder_walk(node, action, goodies):
    # print_node_info(node)
    this_pylnum_sf1 = getattr(node, "lineno", None)
    this_orig_ds_lnum_sf1 = get_orig_ds_lnumsf1_from_py_lnumsf1(goodies, this_pylnum_sf1)
    if this_orig_ds_lnum_sf1 is not None:
        goodies['latest_orig_ds_lnum_sf1'] = this_orig_ds_lnum_sf1
    if isinstance(node, ast.Expr):
        postorder_walk(node.value, action, goodies)
    elif isinstance(node, ast.BinOp):
        postorder_walk(node.left, action, goodies)
        postorder_walk(node.right, action, goodies)
        postorder_walk(node.op, action, goodies)
    elif isinstance(node, ast.BoolOp):
        # Consecutive operations with the same operator, such as a or b or c, are collapsed into one node with several values.
        if len(node.values) > 2:
            raise ValueError("Ambiguous expr, add parentheses.")
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
        func_name = node.name
        this_func_label = f"func_{func_name}"
        this_arg_count = how_many_args(func_name, goodies['symtable_root'])
        if this_arg_count is None:
            raise ValueError("Invalid args:", func_name)
        goodies['func_def_name'] = func_name
        action(add_nop(this_func_label), goodies)
        action(add_alloc(func_name), goodies)
        for item in node.body:
            postorder_walk(item, action, goodies)
        action(add_push0(), goodies)
        action(add_default_return(this_arg_count), goodies)
    elif isinstance(node, ast.Return):
        if node.value is None:
            action(add_push0(), goodies)
        else:
            postorder_walk(node.value, action, goodies)
        action(node, goodies)
    elif isinstance(node, ast.AugAssign):
        raise ValueError(f"{node.__class__.__name__}: To Be Implemented")
    elif isinstance(node, ast.If):
        if_skip_label = f"{node.__class__.__name__}_skip@{this_orig_ds_lnum_sf1}"
        if_end_label = f"{node.__class__.__name__}_end@{this_orig_ds_lnum_sf1}"
        if len(node.orelse) == 0:
            if_skip_label = if_end_label
        goodies['if_destination_label'] = if_skip_label
        postorder_walk(node.test, action, goodies)
        action(node, goodies)
        for item in node.body:
            postorder_walk(item, action, goodies)
        if len(node.orelse):
            action(add_jmp(if_end_label), goodies)
            action(add_nop(if_skip_label), goodies)
            for item in node.orelse:
                postorder_walk(item, action, goodies)
        action(add_nop(if_end_label), goodies)
    elif isinstance(node, ast.While):
        while_start_label = f"{node.__class__.__name__}_start@{this_orig_ds_lnum_sf1}"
        while_end_label = f"{node.__class__.__name__}_end@{this_orig_ds_lnum_sf1}"
        action(add_nop(while_start_label), goodies)
        postorder_walk(node.test, action, goodies)
        goodies['while_start_label'] = while_start_label
        goodies['while_end_label'] = while_end_label
        action(node, goodies)
        for item in node.body:
            postorder_walk(item, action, goodies)
        action(add_jmp(while_start_label), goodies)
        action(add_nop(while_end_label), goodies)
    elif isinstance(node, ast.Call):
        func_name = node.func.id
        caller_arg_count = len(node.args)
        if len(node.keywords) != 0:
            raise ValueError("Invalid arguments")
        if func_name in ds_reserved_funcs:
            callee_arg_count = ds_reserved_funcs[func_name].arg_len
        else:
            callee_arg_count = how_many_args(func_name, goodies['symtable_root'])
        if callee_arg_count is None:
            raise ValueError(f"Function {func_name}() not found")
        if caller_arg_count != callee_arg_count:
            raise ValueError("Wrong number of arguments")
        goodies["caller_func_name"] = func_name
        # Push args right-to-left
        for item in reversed(node.args):
            postorder_walk(item, action, goodies)
        action(node, goodies)
    elif is_leaf(node):
        action(node, goodies)
    else:
        raise ValueError(f"Unknown AST Node: {node}")
