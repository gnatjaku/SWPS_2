
"""
01_dis_bytecode.py
Pokaz bytecode w Pythonie – moduł `dis`.

Cel dydaktyczny:
- pokazać studentom, że Python nie „interpretuje tekstu” linijka po linijce,
  tylko najpierw kompiluje kod do bytecode, który wykonuje w maszynie wirtualnej.
"""

import dis

def multiply_and_add(x, y):
    return x * 2 + y

def main():
    print("=== Funkcja multiply_and_add ===")
    print(dis.dis(multiply_and_add))

    # Dodatkowy pokaz: prosty lambda w locie
    print("\n=== Lambda x*2 ===")
    print(dis.dis(lambda x: x * 2))

if __name__ == "__main__":
    main()
