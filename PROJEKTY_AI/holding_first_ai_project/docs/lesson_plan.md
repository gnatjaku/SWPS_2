# Lesson Plan: Holding-First AI

## Duration

60–90 minutes.

## Learning goals

Students should understand:

1. the difference between meaning-first and holding-first architecture,
2. why uncertainty should be preserved rather than prematurely collapsed,
3. how to build a simple AI decision pipeline,
4. how to evaluate answers according to stability, not only semantic elegance,
5. how this architecture relates to RAG, tool use, prompting and fine-tuning.

---

## Part 1. Conceptual introduction

Show two architectures:

```text
Meaning-first:
input → meaning → response
```

```text
Holding-first:
input → anchors → uncertainty → risks → safe steps → response
```

Key sentence:

> Meaning-first AI answers when it thinks it understands.  
> Holding-first AI answers when it can hold the situation without falsifying it.

---

## Part 2. Run demo

Use:

```bash
python examples/run_demo.py
```

Discuss:

- anchors,
- uncertainties,
- risks,
- next safe steps,
- selected answer,
- holding score.

---

## Part 3. Student exercise

Ask students to modify the input message:

```text
Prowadzący nie odpisał, a termin w systemie jest inny niż w mailu.
```

They should add detection for:

- source conflict,
- official source priority,
- escalation step.

---

## Part 4. Extension

Implement:

```python
class SourcePriorityResolver:
    pass
```

Suggested hierarchy:

1. official course regulation,
2. LMS,
3. email from teacher,
4. group leader,
5. group chat rumor.

---

## Part 5. Discussion

Questions:

1. Is this AI if it does not use an LLM?
2. Where would an LLM fit into this architecture?
3. Would RAG help here?
4. What could be fine-tuned?
5. What should remain rule-based?

---

## Closing formula

Prompt gives instruction.  
RAG gives memory.  
Tools give action.  
Fine-tuning gives habit.  
Holding-first architecture gives stability.