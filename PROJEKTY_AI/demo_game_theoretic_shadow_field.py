
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from game_theoretic_shadow_field_engine import create_engine, report

engine = create_engine()

print("=== AGENT MATRIX ===")
print(engine.agent_matrix().round(2))

print("\n=== PAYOFF MATRIX ===")
payoff = engine.payoff_matrix()
print(payoff.round(3))

print("\n=== GAME STABILITY ===")
stability = engine.game_stability()
print(stability.round(3))

print("\n=== NASH-LIKE SCENARIOS ===")
print(engine.find_pure_nash_like_scenarios(regret_threshold=0.75).round(3))

selected, shadows, field = engine.collapse(temperature=1.4)

print("\n=== DECISION FIELD WITH GAME THEORY ===")
print(field[[
    "scenario","probability","energy","field_tension",
    "social_welfare","stakeholder_conflict","game_stability",
    "max_regret","instability"
]].round(3))

print("\n")
print(report(selected, shadows))

plt.figure(figsize=(10,6))
plt.scatter(
    field["stakeholder_conflict"],
    field["energy"],
    s=field["probability"] * 3000 + 120,
    alpha=0.75
)
for _, row in field.iterrows():
    plt.text(row["stakeholder_conflict"] + 0.02, row["energy"] + 0.02, row["scenario"], fontsize=8)
plt.title("Game-Theoretic Shadow Field: Energy vs Stakeholder Conflict")
plt.xlabel("Stakeholder conflict")
plt.ylabel("Field energy")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("game_theoretic_shadow_field_map.png", dpi=160)

plt.figure(figsize=(10,6))
plt.scatter(
    field["field_tension"],
    field["game_stability"],
    s=field["probability"] * 3000 + 120,
    alpha=0.75
)
for _, row in field.iterrows():
    plt.text(row["field_tension"] + 0.02, row["game_stability"] + 0.01, row["scenario"], fontsize=8)
plt.title("Field Tension vs Game Stability")
plt.xlabel("Field tension")
plt.ylabel("Game stability")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("field_tension_vs_game_stability.png", dpi=160)

timeline = engine.timeline(rounds=6, temperature=1.4)
print("\n=== TIMELINE WITH FIELD MEMORY AND GAME THEORY ===")
print(timeline.round(3))

plt.figure(figsize=(10,5))
plt.plot(timeline["round"], timeline["energy"], marker="o", label="energy")
plt.plot(timeline["round"], timeline["game_stability"], marker="o", label="game stability")
plt.title("Decision Timeline: Energy and Game Stability")
plt.xlabel("Round")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("game_theoretic_timeline.png", dpi=160)
