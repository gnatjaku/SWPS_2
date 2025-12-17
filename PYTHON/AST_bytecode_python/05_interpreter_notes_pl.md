
# Interpreter Pythona, bytecode i AST – krótkie notatki do wykładu

## 1. Co się dzieje, gdy uruchamiasz `python skrypt.py`?

1. Python wczytuje plik jako tekst.
2. Tekst przechodzi przez **parser** – powstaje AST (Abstract Syntax Tree).
3. AST jest kompilowane do **bytecode** – sekwencji prostych instrukcji dla „maszyny wirtualnej Pythona”.
4. Maszyna wirtualna wykonuje bytecode krok po kroku, zarządzając:
   - stosami (operandów, wywołań funkcji),
   - ramkami stosu,
   - pamięcią obiektów (GC, referencje).

## 2. AST (Abstract Syntax Tree)

- To nie jest tekst, tylko drzewo obiektów:
  - `Module`, `Assign`, `BinOp`, `Name`, `Constant`, itd.
- Każdy węzeł reprezentuje konstrukcję języka.
- Dzięki AST można:
  - budować lintery (np. flake8),
  - tworzyć automatyczne refaktoryzatory,
  - pisać narzędzia analizujące i transformujące kod,
  - robić systemy AI, które rozumieją strukturę programów, a nie tylko tekst.

## 3. Bytecode i `dis`

- Bytecode to „asemblery” Pythona – instrukcje typu:
  - `LOAD_FAST`, `LOAD_CONST`, `BINARY_ADD`, `RETURN_VALUE`.
- Moduł `dis` pozwala podejrzeć ten poziom:
  - `dis.dis(funkcja)`.



## 4. Meta-programowanie

- `ast.parse` – zamiana tekstu w drzewo.
- `ast.NodeTransformer` – klasa bazowa do przepisywania drzewa.
- `compile(tree, filename, mode)` – kompilacja AST do bytecode.
- `exec` – wykonanie skompilowanego kodu.


> „Python nie tylko wykonuje programy.  
>  Python może też być użyty do pisania programów, które przepisują inne programy.”
