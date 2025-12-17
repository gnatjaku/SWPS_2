
"""
03_ast_walk.py
Przechodzenie po drzewie AST – pokaz `ast.walk`.

Cel:
- uświadomić studentom, że AST to nie jest „string”,
  tylko struktura złożona z obiektów reprezentujących elementy języka.
"""

import ast

CODE = "x = (a + b) * 3"

def main():
    print("=== Kod źródłowy ===")
    print(CODE)

    tree = ast.parse(CODE)

    print("\n=== Typy węzłów odwiedzonych przez ast.walk ===")
    for node in ast.walk(tree):
        print(type(node).__name__)

if __name__ == "__main__":
    main()
