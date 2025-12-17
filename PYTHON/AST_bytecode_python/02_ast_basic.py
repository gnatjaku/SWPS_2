
"""
02_ast_basic.py
Podstawy AST – jak Python widzi kod jako drzewo składniowe.
"""

import ast

CODE = """
x = 2 + 3
y = x * 5
"""

def main():
    print("=== Kod źródłowy ===")
    print(CODE)

    print("\n=== Drzewo AST (ast.dump) ===")
    tree = ast.parse(CODE)
    print(ast.dump(tree, indent=4))

    # Dodatkowy akcent: typ głównego węzła
    print("\n=== Typ drzewa głównego ===")
    print(type(tree).__name__)  # Module

if __name__ == "__main__":
    main()
