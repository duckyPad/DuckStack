import ast
import sys
import symtable

def print_symtable(table, indent=0):
    pad = "  " * indent

    print(f"{pad}Table: {table.get_name()} (type={table.get_type()})")
    print(f"{pad}  Nested scope: {table.is_nested()}")
    print(f"{pad}  Has children: {len(table.get_children()) > 0}")
    print(f"{pad}  Identifiers:")

    for ident in table.get_identifiers():
        sym = table.lookup(ident)
        print(f"{pad}    {ident}: "
              f"local={sym.is_local()}, "
              f"global={sym.is_global()}, "
              f"free={sym.is_free()}, "
              f"imported={sym.is_imported()}, "
              f"parameter={sym.is_parameter()}, "
              f"assigned={sym.is_assigned()}, "
              f"namespace={sym.is_namespace()}")

        if sym.is_namespace():
            for child in sym.get_namespaces():      # go into function/class blocks
                print_symtable(child, indent + 2)


if len(sys.argv) < 2:
    print("Usage: python ast_dump.py <sourcefile.py>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    source = f.read()

tree = ast.parse(source, mode="exec")
print(ast.dump(tree, indent=2))


print("\n=== Symbol Table ===")
top = symtable.symtable(source, filename, "exec")
print_symtable(top)