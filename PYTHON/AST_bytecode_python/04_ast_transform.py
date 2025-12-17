
"""
04_ast_transform.py
Transformacja AST – modyfikujemy liczby w kodzie, kompilujemy, wykonujemy.

Cel:
- pokazać meta-programowanie na prostym przykładzie;
- uświadomić, że Python pozwala pisać kod, który przepisuje kod.
"""

import ast

class MultiplyIntConstantsByTen(ast.NodeTransformer):
    def visit_Constant(self, node):
        # W Pythonie 3.8+ liczby całkowite to ast.Constant
        if isinstance(node.value, int):
            new_value = node.value * 10
            return ast.copy_location(ast.Constant(new_value), node)
        return node

def main():
    code = "x = 2 + 3 + 1.45\nprint('x =', x)"
    print("=== Oryginalny kod ===")
    print(code)

    tree = ast.parse(code)
    transformer = MultiplyIntConstantsByTen()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    print("\n=== Zmienione drzewo AST ===")
    print(ast.dump(new_tree, indent=4))

    print("\n=== Uruchomienie zmodyfikowanego kodu ===")
    compiled = compile(new_tree, "<ast>", "exec")
    exec_globals = {}
    exec(compiled, exec_globals)

if __name__ == "__main__":
    main()
