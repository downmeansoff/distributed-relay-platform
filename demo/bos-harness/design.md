# Technical design — BOS.PRO harness demo

## Harness layers

```text
Goal / business requirement
          ↓
Behavioral spec + acceptance criteria
          ↓
Planner + explicit task state
          ↓
Executor with scoped tools
          ↓
Deterministic verifier
          ↓
Evidence + human approval boundary
```

## Implementation

- `ProbeSpec` describes a named health check, criticality, and timeout budget.
- `run_probe` isolates one probe, enforces its timeout, and sanitizes failures.
- `aggregate_health` converts probe outcomes into the stable public contract.
- `default_probes` uses deterministic environment-backed checks only for this sanitized demo.
- `tests/test_health.py` is the external completion gate.

## Dynamic workflow rule

A plan may change only when new evidence appears: a failing test, a blocked dependency, an invalid assumption, or a safety constraint. The goal and behavioral requirements remain stable.

## Replanning event used in this demo

The initial plan treated a probe as a direct function call. A timeout test showed that the endpoint could wait for a slow optional component and incorrectly report `healthy`. The plan was amended to:

1. execute probes within an explicit timeout boundary;
2. classify an optional timeout as a degraded service;
3. preserve a regression test for the discovered edge case.

## Safety boundaries

- Agents may edit only the demo branch.
- No production secrets or hosts are available.
- No deployment tool is granted to the executor.
- Production promotion remains a human decision after CI, staging, and smoke evidence.
