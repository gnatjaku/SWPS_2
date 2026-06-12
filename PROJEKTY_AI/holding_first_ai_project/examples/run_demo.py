import sys
from pathlib import Path

# Allows running this file directly without installing the package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from holding_first_ai import HoldingFirstAgent


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    message = """
Nie wiem, co mam oddać. Chyba termin jest jutro, ale ktoś mówił, że dziś.
Grupa się nie odzywa. Mam część kodu, ale nie wiem, czy to wystarczy.
""".strip()

    agent = HoldingFirstAgent()
    result = agent.answer(message)
    field = result["holding_field"]

    print_section("WEJŚCIE")
    print(message)

    print_section("POLE NOŚNOŚCI: ANCHORS")
    for item in field.anchors:
        print("-", item)

    print_section("POLE NOŚNOŚCI: UNCERTAINTIES")
    for item in field.uncertainties:
        print("-", item)

    print_section("POLE NOŚNOŚCI: RISKS")
    for item in field.risks:
        print("-", item)

    print_section("NAJBLIŻSZE BEZPIECZNE KROKI")
    for item in field.next_safe_steps:
        print("-", item)

    print_section("WSZYSTKIE ODPOWIEDZI KANDYDACKIE")
    for index, item in enumerate(result["all_candidates"], start=1):
        print(f"\n--- Kandydat {index} | score={item['score']} ---")
        print(item["response"])
        print("Powody:")
        for reason in item["reasons"]:
            print("  -", reason)

    print_section("WYBRANA ODPOWIEDŹ")
    print(result["best_response"]["response"])

    print_section("SCORE I UZASADNIENIE WYBORU")
    print("Score:", result["best_response"]["score"])
    for reason in result["best_response"]["reasons"]:
        print("-", reason)


if __name__ == "__main__":
    main()