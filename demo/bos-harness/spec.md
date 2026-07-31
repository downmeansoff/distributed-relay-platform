# Behavioral specification — structured health states

## Goal

Replace the binary demo health response with a structured contract that distinguishes normal operation, partial degradation, and a critical outage.

## Observable requirements

1. `GET /health` returns JSON with top-level `status`, `env`, and `checks`.
2. `healthy` means every configured probe succeeded.
3. `degraded` means at least one non-critical probe failed or timed out while every critical probe succeeded.
4. `unhealthy` means at least one critical probe failed or timed out.
5. `unhealthy` returns HTTP 503; `healthy` and `degraded` return HTTP 200.
6. Every probe has a hard timeout and cannot block the response indefinitely.
7. Probe exceptions are converted into sanitized details; exception messages, credentials, and internal addresses are not exposed.
8. The behavior is covered by deterministic tests for all three states, timeout handling, and exception sanitization.

## Non-goals

- No production hosts, credentials, network identifiers, or proprietary health logic.
- No autonomous deployment.
- No attempt to replicate the private production monitoring stack.

## Completion rule

The executor cannot mark the task complete by narrative. Completion requires tests and a verifier mapping every requirement to concrete evidence.
