# BOS.PRO Harness Engineer demo

This branch is a small, public, verifiable demonstration of an agentic engineering harness. It intentionally uses a narrow change instead of exposing private commercial systems.

## What the demo proves

```text
Goal → behavioral spec → plan → execute → verify → classify failure → replan → verify → human boundary
```

The feature changes the public `/health` endpoint from a binary response into three explicit states:

- `healthy` — all probes succeeded;
- `degraded` — an optional probe failed or timed out;
- `unhealthy` — a critical probe failed or timed out.

## Files to show during the interview

1. [`spec.md`](spec.md) — observable requirements and completion rule.
2. [`design.md`](design.md) — harness layers, tool boundary, and replan logic.
3. [`tasks.md`](tasks.md) — original plan and tasks added after new evidence.
4. [`state.json`](state.json) — externalized run state and budgets.
5. [`01-initial-failure.txt`](evidence/01-initial-failure.txt) — evidence that invalidated the first plan.
6. [`02-final-verification.md`](evidence/02-final-verification.md) — acceptance criteria mapped to tests.
7. [`backend/app.py`](../../backend/app.py) and [`tests/test_health.py`](../../tests/test_health.py) — implementation and deterministic gates.

## Reproduce

```bash
python -m pytest -q
```

Run the API:

```bash
python backend/app.py
curl http://localhost:8000/health
```

Simulate degradation:

```bash
DEMO_RELAY_HEALTH=timeout python backend/app.py
curl http://localhost:8000/health
```

Simulate a critical outage:

```bash
DEMO_DB_HEALTH=error python backend/app.py
curl -i http://localhost:8000/health
```

## Eight-minute interview script

### 0:00–0:45 — framing

> I will show a controlled harness, not a one-shot prompt. The commercial workflow is private, so I reproduced the same engineering pattern on a sanitized public repository.

### 0:45–2:00 — goal and specification

Open `spec.md` and explain that observable behavior and acceptance criteria are the source of truth, not the chat transcript.

### 2:00–3:00 — plan and state

Open `tasks.md` and `state.json`:

> The state is externalized. Another agent or a new session can recover the goal, completed work, budgets, and current blocker without replaying the whole conversation.

### 3:00–4:30 — execution loop

```text
observe → plan → act → verify → classify → continue / replan / escalate
```

Explain that the executor is not allowed to declare success. Tests and the verifier decide whether evidence is sufficient.

### 4:30–6:00 — dynamic replan

Show `01-initial-failure.txt` and the added T3.1/T4.1 tasks:

> The original design called probes directly. A test showed that a slow optional dependency could exceed the response budget and still be reported as healthy. The harness changed the plan, added timeout isolation, and preserved the failure as a regression test.

### 6:00–7:00 — final evidence

Show `02-final-verification.md`, then run:

```bash
git diff main...bos-harness-demo --stat
python -m pytest -q
```

### 7:00–8:00 — production boundary

> Agents can analyze, implement, test, and document. They do not receive production credentials. CI, staging, smoke checks, and human approval remain mandatory for high-impact changes.

## Key answers

### What is a harness?

A harness is the control layer around the model: specification, context, tools, state, memory, execution loop, verification, permissions, observability, budgets, and escalation.

### How do you stop infinite loops?

Iteration and time budgets, no-progress detection, a ban on repeating the same action without new evidence, failure classification, fallback strategies, and human escalation.

### How do you parallelize agents?

A dependency graph, isolated branches/worktrees, file ownership, scoped tools, and integration only after independent verification. Two agents do not write the same file concurrently.

### How do you measure the harness?

Task success rate, acceptance-criteria coverage, iterations, intervention rate, regressions, latency, tool-call failures, and cost on a fixed evaluation set.

## Honest positioning

This repository demonstrates the engineering method publicly. Private prompts, commercial logic, infrastructure identifiers, credentials, and production access are intentionally excluded.
