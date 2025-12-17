
"""
extras/compile_exec_demo.py
Pokazuje użycie compile() + exec() na prostym stringu z kodem.
"""

CODE = "result = sum([1,2,3]); print('Wynik =', result)"

def main():
    print("=== Oryginalny tekst kodu ===")
    print(CODE)

    compiled = compile(CODE, "<string>", "exec")

    print("\n=== Wykonanie kodu przez exec ===")
    exec_globals = {}
    exec(compiled, exec_globals)

    print("\n=== Zmienna result w exec_globals ===")
    print(exec_globals.get("result"))

if __name__ == "__main__":
    main()
