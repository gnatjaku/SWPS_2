# Holding-First AI Project

## Idea

This project demonstrates a simple **Holding-First AI** architecture inspired by the idea that an AI system should not always start from meaning.

Classic architecture:

```text
input → meaning/intention → response
```

Holding-first architecture:

```text
input → anchors → uncertainties → risks → safe next steps → response
```

In other words:

> The system first checks what must be held stable before it tries to interpret or answer.

This project is intentionally simple and educational. It does not require external APIs, OpenAI keys, databases, GPUs, or cloud services.

---

## What is inside?

```text
holding_first_ai_project/
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   └── holding_first_ai/
│       ├── __init__.py
│       └── core.py
├── examples/
│   └── run_demo.py
├── tests/
│   └── test_agent.py
├── notebooks/
│   └── holding_first_ai_colab.ipynb
└── docs/
    └── lesson_plan.md
```

---

## Main components

### 1. AnchorExtractor

Finds stable facts and contextual anchors.

Example:

```text
"mam część kodu" → "User has some code already."
```

### 2. UncertaintyDetector

Finds uncertainty signals.

Example:

```text
"chyba", "nie wiem", "ktoś mówił"
```

### 3. RiskDetector

Detects possible failure points.

Example:

```text
wrong deadline, lack of group coordination, incomplete project
```

### 4. NextStepPlanner

Suggests safe next steps before giving a final answer.

### 5. HoldingFieldBuilder

Builds the central object of the system: the **holding field**.

### 6. CandidateResponseGenerator

Creates several possible responses.

### 7. HoldingEvaluator

Scores responses not by elegance, but by how well they hold the situation.

### 8. HoldingFirstAgent

Runs the whole pipeline.

---

## How to run locally

### Windows PowerShell

```powershell
cd holding_first_ai_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python examples/run_demo.py
```

### macOS / Linux

```bash
cd holding_first_ai_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python examples/run_demo.py
```

---

## How to use in Google Colab

1. Open Google Colab.
2. Upload:

```text
notebooks/holding_first_ai_colab.ipynb
```

3. Run all cells.

This notebook version does not need GPU.

---

## Teaching use

Use this project after introducing:

1. prompt engineering,
2. RAG,
3. tool use,
4. fine-tuning,
5. AI agent architectures.

It works best as a conceptual bridge between:

```text
LLM as text generator
```

and

```text
AI system as stability architecture
```

---

## Core teaching sentence

> Prompt gives instruction.  
> RAG gives memory.  
> Tools give action.  
> Fine-tuning gives habit.  
> Holding-first architecture gives stability.

---

## Example input

```text
Nie wiem, co mam oddać. Chyba termin jest jutro, ale ktoś mówił, że dziś.
Grupa się nie odzywa. Mam część kodu, ale nie wiem, czy to wystarczy.
```

The system identifies:

- stable anchors,
- uncertainty,
- risks,
- safe next steps,
- best response according to holding score.

---

## Extension ideas for students

1. Add `SourcePriorityResolver`.
2. Add memory from previous messages.
3. Add real LLM response generation.
4. Add RAG for official documents.
5. Replace rule-based evaluation with an ML classifier.
6. Add JSON output mode.
7. Add Streamlit interface.
8. Add tests for new risk types.

---

## Important distinction

This is not a chatbot.

It is a small architecture that shows how to build an AI system that first stabilizes the situation.

Meaning is not removed.

Meaning appears after the system has created enough stability to carry it.