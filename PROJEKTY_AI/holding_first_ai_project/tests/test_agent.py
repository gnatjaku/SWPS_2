import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from holding_first_ai import HoldingFirstAgent, HoldingFieldBuilder


def test_holding_field_detects_deadline_uncertainty():
    builder = HoldingFieldBuilder()
    field = builder.build("Chyba termin jest jutro, ale ktoś mówił, że dziś.")

    assert any("termin" in item.lower() for item in field.anchors)
    assert any("niepewności" in item.lower() or "chyba" in item.lower() for item in field.uncertainties)
    assert any("termin" in item.lower() for item in field.risks)


def test_agent_selects_holding_first_response():
    agent = HoldingFirstAgent()
    result = agent.answer(
        "Nie wiem co mam oddać. Chyba termin jest jutro, ale ktoś mówił, że dziś. "
        "Grupa się nie odzywa. Mam część kodu."
    )

    best = result["best_response"]["response"].lower()

    assert "fakty" in best
    assert "ryzyka" in best
    assert "nie zakładałbym" in best or "potwierdzić" in best