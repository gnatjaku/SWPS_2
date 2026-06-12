from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HoldingField:
    """
    Central object of the holding-first architecture.

    It does not primarily answer:
        "What does this mean?"

    It first answers:
        "What must be held stable here?"
    """

    original_message: str
    anchors: List[str]
    uncertainties: List[str]
    risks: List[str]
    next_safe_steps: List[str]


class AnchorExtractor:
    """
    Extracts stable anchors from the user's message.

    Anchors are not full meanings.
    They are stable points that should not be lost.
    """

    def extract(self, message: str) -> List[str]:
        lower = message.lower()
        anchors: List[str] = []

        if "projekt" in lower:
            anchors.append("Użytkownik odnosi się do projektu.")

        if "kod" in lower:
            anchors.append("Użytkownik posiada jakąś część kodu lub pracy technicznej.")

        if "termin" in lower or "jutro" in lower or "dziś" in lower or "dzisiaj" in lower:
            anchors.append("Występuje problem z terminem lub harmonogramem.")

        if "grupa" in lower or "zespół" in lower:
            anchors.append("Problem dotyczy również pracy grupowej lub koordynacji zespołu.")

        if "prowadzący" in lower or "wykładowca" in lower:
            anchors.append("Wiadomość odwołuje się do autorytetu prowadzącego.")

        if not anchors:
            anchors.append("Brak stabilnych punktów faktograficznych poza samą prośbą użytkownika.")

        return anchors


class UncertaintyDetector:
    """
    Detects places where the system should not pretend certainty.
    """

    uncertainty_patterns = [
        "chyba",
        "nie wiem",
        "ktoś mówił",
        "może",
        "prawdopodobnie",
        "nie jestem pewien",
        "nie jestem pewna",
        "podobno",
        "wydaje mi się",
    ]

    def detect(self, message: str) -> List[str]:
        lower = message.lower()
        uncertainties: List[str] = []

        for pattern in self.uncertainty_patterns:
            if pattern in lower:
                uncertainties.append(f"Wiadomość zawiera sygnał niepewności: '{pattern}'.")

        if ("dziś" in lower or "dzisiaj" in lower) and "jutro" in lower:
            uncertainties.append("Występuje sprzeczność lub niejasność: termin może być dziś albo jutro.")

        if "ale" in lower and ("nie wiem" in lower or "chyba" in lower):
            uncertainties.append("Wiadomość zawiera napięcie między działaniem a niepewnością.")

        if not uncertainties:
            uncertainties.append("Brak jawnych sygnałów niepewności.")

        return uncertainties


class RiskDetector:
    """
    Detects what may collapse if the system answers too quickly.
    """

    def detect(self, message: str) -> List[str]:
        lower = message.lower()
        risks: List[str] = []

        if "termin" in lower or "dziś" in lower or "dzisiaj" in lower or "jutro" in lower:
            risks.append("Ryzyko podania błędnego lub niepotwierdzonego terminu.")

        if ("grupa" in lower or "zespół" in lower) and (
            "nie odzywa" in lower or "nie odpowiada" in lower or "cisza" in lower
        ):
            risks.append("Ryzyko braku koordynacji w grupie.")

        if "kod" in lower and ("nie wiem" in lower or "wystarczy" in lower or "nie działa" in lower):
            risks.append("Ryzyko oddania niepełnego lub niedziałającego rozwiązania.")

        if "prowadzący" in lower and ("nie odpisał" in lower or "nie odpowiedział" in lower):
            risks.append("Ryzyko braku potwierdzenia ze strony prowadzącego.")

        if not risks:
            risks.append("Brak oczywistego ryzyka, ale należy unikać nadinterpretacji.")

        return risks


class NextStepPlanner:
    """
    Proposes safe next steps.

    The goal is not to solve everything.
    The goal is to prevent collapse of the situation.
    """

    def plan(self, field_data: Dict[str, List[str]]) -> List[str]:
        risks = field_data.get("risks", [])
        steps: List[str] = []

        if any("termin" in risk.lower() for risk in risks):
            steps.append(
                "Sprawdź oficjalne źródło terminu: sylabus, LMS, mail od prowadzącego albo treść zadania."
            )

        if any("grup" in risk.lower() or "zesp" in risk.lower() for risk in risks):
            steps.append(
                "Wyślij krótką wiadomość do grupy z prośbą o potwierdzenie podziału pracy i aktualnego stanu."
            )

        if any("kod" in risk.lower() or "rozwiązania" in risk.lower() for risk in risks):
            steps.append(
                "Zrób minimalną listę: co działa, czego brakuje, co można pokazać jako wersję roboczą."
            )

        if any("prowadzącego" in risk.lower() for risk in risks):
            steps.append(
                "Przygotuj krótkie pytanie do prowadzącego z jednym konkretnym problemem i prośbą o potwierdzenie."
            )

        if not steps:
            steps.append("Sformułuj jedno konkretne pytanie albo pokaż aktualny stan pracy.")

        return steps


class HoldingFieldBuilder:
    """
    Builds the holding field.

    This is the central layer of topology 2.
    """

    def __init__(self) -> None:
        self.anchor_extractor = AnchorExtractor()
        self.uncertainty_detector = UncertaintyDetector()
        self.risk_detector = RiskDetector()
        self.next_step_planner = NextStepPlanner()

    def build(self, message: str) -> HoldingField:
        anchors = self.anchor_extractor.extract(message)
        uncertainties = self.uncertainty_detector.detect(message)
        risks = self.risk_detector.detect(message)

        field_data = {
            "anchors": anchors,
            "uncertainties": uncertainties,
            "risks": risks,
        }

        next_steps = self.next_step_planner.plan(field_data)

        return HoldingField(
            original_message=message,
            anchors=anchors,
            uncertainties=uncertainties,
            risks=risks,
            next_safe_steps=next_steps,
        )


class CandidateResponseGenerator:
    """
    Generates candidate responses.

    One can be meaning-first.
    One can be too confident.
    One can be holding-first.
    """

    def generate(self, field: HoldingField) -> List[str]:
        response_1 = """
Wygląda na to, że pytasz o termin projektu i wymagania zaliczeniowe.
Najlepiej sprawdź regulamin zadania i skontaktuj się z prowadzącym.
""".strip()

        response_2 = """
Termin prawdopodobnie jest jutro, więc powinieneś szybko dokończyć kod
i wysłać projekt nawet bez kontaktu z grupą.
""".strip()

        response_3 = f"""
Widzę tu kilka rzeczy, które trzeba najpierw uporządkować.

FAKTY, KTÓRE MAMY:
{self._format_list(field.anchors)}

MIEJSCA NIEPEWNOŚCI:
{self._format_list(field.uncertainties)}

RYZYKA:
{self._format_list(field.risks)}

NAJBLIŻSZY BEZPIECZNY KROK:
{self._format_list(field.next_safe_steps)}

Nie zakładałbym teraz terminu na podstawie plotki. Najpierw trzeba potwierdzić oficjalne źródło,
a równolegle przygotować minimalną wersję projektu: co działa, czego brakuje i co można oddać jako stan obecny.
""".strip()

        return [response_1, response_2, response_3]

    @staticmethod
    def _format_list(items: List[str]) -> str:
        return "\n".join([f"- {item}" for item in items])


class HoldingEvaluator:
    """
    Scores responses according to holding criteria.

    It does not choose the prettiest response.
    It chooses the response that best stabilizes the situation.
    """

    def evaluate(self, response: str) -> Dict[str, object]:
        lower = response.lower()

        score = 0
        reasons: List[str] = []

        if "fakty" in lower or "które mamy" in lower:
            score += 2
            reasons.append("Odpowiedź stabilizuje fakty.")

        if "niepew" in lower or "nie zakładałbym" in lower or "potwierdzić" in lower:
            score += 2
            reasons.append("Odpowiedź jawnie obsługuje niepewność.")

        if "następny" in lower or "krok" in lower or "sprawdź" in lower:
            score += 2
            reasons.append("Odpowiedź daje konkretny następny krok.")

        if "prawdopodobnie jest jutro" in lower:
            score -= 3
            reasons.append("Odpowiedź zakłada niepotwierdzony termin.")

        if "ryzyk" in lower:
            score += 2
            reasons.append("Odpowiedź identyfikuje ryzyka.")

        context_words = ["grupa", "kod", "termin", "projekt"]
        context_hits = sum(1 for word in context_words if word in lower)

        score += context_hits
        if context_hits > 0:
            reasons.append(f"Odpowiedź zachowuje kontekst: {context_hits} elementów.")

        return {
            "score": score,
            "reasons": reasons,
        }

    def choose_best(self, responses: List[str]) -> Dict[str, object]:
        evaluated = []

        for response in responses:
            result = self.evaluate(response)
            evaluated.append(
                {
                    "response": response,
                    "score": result["score"],
                    "reasons": result["reasons"],
                }
            )

        evaluated = sorted(evaluated, key=lambda item: item["score"], reverse=True)

        return {
            "best": evaluated[0],
            "all": evaluated,
        }


class HoldingFirstAgent:
    """
    Agent based on holding-first topology.

    The agent:
    1. builds a holding field,
    2. generates candidate responses,
    3. evaluates responses by holding score,
    4. returns the best stabilizing response.
    """

    def __init__(self) -> None:
        self.field_builder = HoldingFieldBuilder()
        self.response_generator = CandidateResponseGenerator()
        self.evaluator = HoldingEvaluator()

    def answer(self, message: str) -> Dict[str, object]:
        field = self.field_builder.build(message)
        candidates = self.response_generator.generate(field)
        decision = self.evaluator.choose_best(candidates)

        return {
            "holding_field": field,
            "best_response": decision["best"],
            "all_candidates": decision["all"],
        }