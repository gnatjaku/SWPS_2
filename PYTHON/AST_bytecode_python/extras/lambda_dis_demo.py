
"""
extras/lambda_dis_demo.py
Krótki pokaz: jak wygląda bytecode dla różnych lambd.
"""

import dis

def main():
    lambdas = [
        ("x*2", lambda x: x*2),
        ("x+1", lambda x: x+1),
        ("x**2 + 3", lambda x: x**2 + 3),
    ]
    for desc, fn in lambdas:
        print(f"=== Lambda: {desc} ===")
        dis.dis(fn)
        print()

if __name__ == "__main__":
    main()
