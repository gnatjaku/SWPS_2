
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from itertools import product

@dataclass
class Scenario:
    name: str
    description: str
    tags: List[str]
    values: Dict[str, float]

@dataclass
class Agent:
    name: str
    weights: Dict[str, float]
    bias: float = 0.0

    def evaluate(self, scenario: Scenario) -> float:
        score = self.bias
        for k, w in self.weights.items():
            score += scenario.values.get(k, 0.0) * w
        return float(np.clip(score, 0.0, 10.0))

@dataclass
class Player:
    name: str
    preferences: Dict[str, float]

    def payoff(self, scenario: Scenario) -> float:
        value = 0.0
        for k, w in self.preferences.items():
            value += scenario.values.get(k, 0.0) * w
        return float(value)

class FieldMemory:
    def __init__(self):
        self.residue = {}

    def gravity(self, scenario: Scenario) -> float:
        return sum(self.residue.get(tag, 0.0) for tag in scenario.tags)

    def update(self, scenario: Scenario, strength=0.25):
        for tag in scenario.tags:
            self.residue[tag] = self.residue.get(tag, 0.0) + strength

class GameTheoreticShadowFieldEngine:
    """
    Game-Theoretic Shadow Field Engine

    Combines:
    - multi-agent evaluation
    - FIELD TENSION DYNAMICS
    - semantic gravity
    - scenario interference
    - payoff matrix
    - stakeholder conflict
    - Nash-like stability
    - social welfare
    - regret
    - probabilistic collapse
    """

    def __init__(self, scenarios, agents, players, interference, memory=None):
        self.scenarios = scenarios
        self.agents = agents
        self.players = players
        self.interference = interference
        self.memory = memory or FieldMemory()

    @staticmethod
    def softmax(x, temperature=1.0):
        x = np.array(x, dtype=float) / temperature
        e = np.exp(x - np.max(x))
        return e / e.sum()

    def agent_matrix(self):
        rows = []
        for s in self.scenarios:
            row = {"scenario": s.name}
            for a in self.agents:
                row[a.name] = a.evaluate(s)
            rows.append(row)
        return pd.DataFrame(rows)

    def payoff_matrix(self):
        rows = []
        for s in self.scenarios:
            row = {"scenario": s.name}
            payoffs = [p.payoff(s) for p in self.players]
            for p, payoff in zip(self.players, payoffs):
                row[p.name] = payoff
            row["social_welfare"] = float(np.mean(payoffs))
            row["conflict"] = float(np.std(payoffs))
            row["min_payoff"] = float(np.min(payoffs))
            row["max_payoff"] = float(np.max(payoffs))
            rows.append(row)
        return pd.DataFrame(rows)

    def regret_matrix(self):
        payoff_df = self.payoff_matrix()
        rows = []

        for p in self.players:
            best = payoff_df[p.name].max()
            for _, row in payoff_df.iterrows():
                rows.append({
                    "player": p.name,
                    "scenario": row["scenario"],
                    "payoff": row[p.name],
                    "best_possible": best,
                    "regret": best - row[p.name]
                })

        return pd.DataFrame(rows)

    def game_stability(self):
        """
        A simplified Nash-like stability score:
        A scenario is stable when no player has a strong regret.
        Lower max regret = more stable.
        """
        payoff_df = self.payoff_matrix()
        regret_df = self.regret_matrix()

        rows = []
        for s in payoff_df["scenario"]:
            subset = regret_df[regret_df["scenario"] == s]
            max_regret = subset["regret"].max()
            avg_regret = subset["regret"].mean()
            stability = 1.0 / (1.0 + max_regret)
            rows.append({
                "scenario": s,
                "max_regret": max_regret,
                "avg_regret": avg_regret,
                "game_stability": stability
            })

        return pd.DataFrame(rows)

    def find_pure_nash_like_scenarios(self, regret_threshold=0.75):
        """
        Not a strict Nash equilibrium in a strategic-form game with simultaneous moves,
        but a useful classroom simplification:
        a scenario is Nash-like if no stakeholder has regret above threshold.
        """
        stability = self.game_stability()
        return stability[stability["max_regret"] <= regret_threshold].copy()

    def field(self, temperature=1.0):
        payoff_df = self.payoff_matrix()
        stability_df = self.game_stability()

        rows = []
        for s in self.scenarios:
            scores = {a.name: a.evaluate(s) for a in self.agents}

            roi = scores["ROI_AGENT"]
            risk = scores["RISK_AGENT"]
            strategy = scores["STRATEGY_AGENT"]
            ethics = scores["ETHICS_AGENT"]
            data = scores["DATA_AGENT"]
            org = scores["ORG_AGENT"]

            tension_value_risk = abs(roi - risk)
            tension_ethics_strategy = abs(ethics - strategy)
            tension_data_org = abs(data - org)

            field_tension = (
                0.45 * tension_value_risk +
                0.30 * tension_ethics_strategy +
                0.25 * tension_data_org
            )

            semantic_gravity = self.memory.gravity(s)

            interference_score = 0.0
            for other in self.scenarios:
                if other.name == s.name:
                    continue
                interference_score += self.interference.get((s.name, other.name), 0.0)
                interference_score += 0.5 * self.interference.get((other.name, s.name), 0.0)

            p_row = payoff_df[payoff_df["scenario"] == s.name].iloc[0]
            g_row = stability_df[stability_df["scenario"] == s.name].iloc[0]

            social_welfare = p_row["social_welfare"]
            stakeholder_conflict = p_row["conflict"]
            game_stability = g_row["game_stability"]
            max_regret = g_row["max_regret"]

            # Core field energy with game theory terms.
            energy = (
                0.26 * roi
                - 0.20 * risk
                + 0.20 * strategy
                + 0.10 * ethics
                + 0.08 * data
                + 0.06 * org
                - 0.16 * field_tension
                + 0.30 * semantic_gravity
                + 0.13 * interference_score
                + 0.28 * social_welfare
                + 1.25 * game_stability
                - 0.22 * stakeholder_conflict
                - 0.12 * max_regret
            )

            instability = (
                field_tension +
                max(0, risk - ethics) +
                max(0, risk - org) +
                stakeholder_conflict +
                max_regret
            )

            rows.append({
                "scenario": s.name,
                "description": s.description,
                "tags": ", ".join(s.tags),
                "roi": roi,
                "risk": risk,
                "strategy": strategy,
                "ethics": ethics,
                "data": data,
                "organization": org,
                "field_tension": field_tension,
                "semantic_gravity": semantic_gravity,
                "interference": interference_score,
                "social_welfare": social_welfare,
                "stakeholder_conflict": stakeholder_conflict,
                "game_stability": game_stability,
                "max_regret": max_regret,
                "energy": energy,
                "instability": instability
            })

        df = pd.DataFrame(rows)
        df["probability"] = self.softmax(df["energy"].values, temperature=temperature)
        df["rank"] = df["probability"].rank(ascending=False, method="dense").astype(int)
        return df.sort_values("probability", ascending=False).reset_index(drop=True)

    def collapse(self, temperature=1.0):
        df = self.field(temperature=temperature)
        selected_row = df.iloc[0]
        selected = next(s for s in self.scenarios if s.name == selected_row["scenario"])
        self.memory.update(selected)
        shadows = df.iloc[1:4]
        return selected_row.to_dict(), shadows, df

    def timeline(self, rounds=5, temperature=1.0):
        rows = []
        for i in range(rounds):
            selected, shadows, df = self.collapse(temperature=temperature)
            rows.append({
                "round": i + 1,
                "selected": selected["scenario"],
                "probability": selected["probability"],
                "energy": selected["energy"],
                "field_tension": selected["field_tension"],
                "game_stability": selected["game_stability"],
                "stakeholder_conflict": selected["stakeholder_conflict"],
                "semantic_gravity": selected["semantic_gravity"]
            })
        return pd.DataFrame(rows)

def create_engine():
    scenarios = [
        Scenario("AI Knowledge Graph", "Warstwa wiedzy łącząca dokumenty, procedury i ekspertów.", ["knowledge", "stability", "data", "organization"], {"roi":7.0,"risk":3.5,"strategy":9.0,"ethics":8.0,"data":7.5,"organization":8.0}),
        Scenario("Predictive Maintenance", "Predykcja awarii, przestojów i planowanie utrzymania ruchu.", ["production", "prediction", "efficiency", "data"], {"roi":8.5,"risk":4.0,"strategy":8.0,"ethics":7.0,"data":8.0,"organization":6.5}),
        Scenario("AI Quality Control", "Wizja komputerowa i detekcja anomalii jakościowych.", ["production", "quality", "automation", "risk"], {"roi":8.0,"risk":5.5,"strategy":8.5,"ethics":6.5,"data":6.5,"organization":6.0}),
        Scenario("Customer Service Agent", "Agent obsługi klienta, reklamacji i historii kontaktu.", ["customer", "language", "automation", "reputation"], {"roi":6.5,"risk":5.0,"strategy":6.5,"ethics":6.0,"data":7.0,"organization":7.0}),
        Scenario("Financial Forecasting Agent", "Prognozy finansowe, cashflow i warianty scenariuszowe.", ["finance", "prediction", "strategy", "risk"], {"roi":7.5,"risk":6.5,"strategy":7.5,"ethics":6.0,"data":6.0,"organization":5.5}),
        Scenario("Autonomous Decision Cockpit", "Kokpit zarządczy z agentami, KPI i symulacją strategii.", ["strategy", "governance", "knowledge", "risk"], {"roi":9.0,"risk":8.0,"strategy":10.0,"ethics":6.5,"data":5.5,"organization":5.0}),
        Scenario("HR Competence Mapper", "Mapa kompetencji, luk i potrzeb szkoleniowych.", ["organization", "people", "ethics", "knowledge"], {"roi":5.5,"risk":4.5,"strategy":6.5,"ethics":7.0,"data":5.5,"organization":8.5}),
        Scenario("Logistics Optimization AI", "Optymalizacja tras, zapasów, magazynów i przepływu operacyjnego.", ["logistics", "efficiency", "prediction", "data"], {"roi":8.0,"risk":4.5,"strategy":7.5,"ethics":7.0,"data":7.0,"organization":6.5})
    ]

    agents = [
        Agent("ROI_AGENT", {"roi":1.0,"strategy":0.1,"risk":-0.1}),
        Agent("RISK_AGENT", {"risk":1.0,"ethics":-0.15,"organization":-0.1}, bias=0.5),
        Agent("STRATEGY_AGENT", {"strategy":1.0,"roi":0.1,"organization":0.1}),
        Agent("ETHICS_AGENT", {"ethics":1.0,"risk":-0.2,"organization":0.1}, bias=1.0),
        Agent("DATA_AGENT", {"data":1.0,"strategy":0.1,"risk":-0.05}),
        Agent("ORG_AGENT", {"organization":1.0,"ethics":0.15,"risk":-0.1})
    ]

    players = [
        Player("BOARD", {"roi":0.35, "strategy":0.35, "risk":-0.15, "organization":0.10}),
        Player("IT", {"data":0.35, "risk":-0.25, "organization":0.25, "strategy":0.15}),
        Player("EMPLOYEES", {"ethics":0.35, "organization":0.35, "risk":-0.25, "automation":-0.10}),
        Player("CUSTOMERS", {"ethics":0.30, "risk":-0.20, "strategy":0.15, "roi":0.05, "data":0.10}),
        Player("CFO", {"roi":0.45, "risk":-0.25, "strategy":0.20, "data":0.10})
    ]

    interference = {
        ("AI Knowledge Graph", "Customer Service Agent"): 1.4,
        ("AI Knowledge Graph", "HR Competence Mapper"): 1.0,
        ("AI Knowledge Graph", "Autonomous Decision Cockpit"): 1.8,
        ("Predictive Maintenance", "Logistics Optimization AI"): 1.5,
        ("Predictive Maintenance", "AI Quality Control"): 1.2,
        ("Financial Forecasting Agent", "Autonomous Decision Cockpit"): 1.1,
        ("Customer Service Agent", "AI Quality Control"): -0.4,
        ("Autonomous Decision Cockpit", "HR Competence Mapper"): -0.6
    }

    return GameTheoreticShadowFieldEngine(scenarios, agents, players, interference)

def report(selected, shadows):
    lines = []
    lines.append("GAME-THEORETIC SHADOW FIELD ENGINE — DECISION REPORT")
    lines.append("=" * 70)
    lines.append(f"COLLAPSED DECISION: {selected['scenario']}")
    lines.append(f"Probability: {selected['probability']:.3f}")
    lines.append(f"Energy: {selected['energy']:.3f}")
    lines.append(f"Field tension: {selected['field_tension']:.3f}")
    lines.append(f"Game stability: {selected['game_stability']:.3f}")
    lines.append(f"Stakeholder conflict: {selected['stakeholder_conflict']:.3f}")
    lines.append(f"Max regret: {selected['max_regret']:.3f}")
    lines.append(f"Instability: {selected['instability']:.3f}")
    lines.append("")
    lines.append("Interpretation:")
    lines.append("The selected decision is not only strong in the AI field. It is also relatively stable in the stakeholder game.")
    lines.append("The system rewards high social welfare and game stability, while penalizing conflict and regret.")
    lines.append("")
    lines.append("SHADOW ALTERNATIVES:")
    for _, row in shadows.iterrows():
        lines.append(f"- {row['scenario']} | p={row['probability']:.3f}, energy={row['energy']:.3f}, game_stability={row['game_stability']:.3f}, conflict={row['stakeholder_conflict']:.3f}")
    lines.append("")
    lines.append("Core thesis:")
    lines.append("A decision is not merely optimal. It must survive the strategic field of players, incentives, conflicts and regret.")
    return "\\n".join(lines)
