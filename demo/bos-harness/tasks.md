# Task plan

## Original plan

- [x] T1 — inspect the existing `/health` endpoint and public repository constraints;
- [x] T2 — define the behavioral contract and acceptance criteria;
- [x] T3 — add typed health states and probe aggregation;
- [x] T4 — add tests for healthy, degraded, and unhealthy states;
- [x] T5 — document the architecture and verification path.

## Evidence-driven replan

The slow-probe test exposed an unplanned edge case: direct probe execution could exceed the response budget and still return `healthy`.

Added tasks:

- [x] T3.1 — enforce a timeout per probe;
- [x] T3.2 — isolate exceptions and remove sensitive exception text;
- [x] T4.1 — add a regression test for a timed-out optional probe;
- [x] T4.2 — verify that a critical failure returns HTTP 503;

## Stop conditions

The loop stops when one of these conditions is met:

1. all acceptance criteria have deterministic evidence;
2. the iteration budget is exhausted;
3. two consecutive iterations produce no new evidence;
4. a requirement is ambiguous or a privileged action is required, causing human escalation.
