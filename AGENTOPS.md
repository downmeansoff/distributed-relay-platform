# AgentOps — AI-Assisted Engineering Workflow

The production platform was developed and maintained with an AI-assisted engineering workflow designed to increase delivery speed without giving agents unrestricted access to production.

## Principle

Coding agents are engineering force multipliers, not autonomous production owners.

Agents can analyze, implement, test, review, and document. Humans retain ownership of architecture, acceptance criteria, security boundaries, production permissions, and release decisions.

## Workflow

```text
Business or product requirement
              ↓
Architecture, scope and acceptance criteria
              ↓
Specialized coding agents in isolated branches
              ↓
Implementation, tests and documentation
              ↓
QA, regression and security review
              ↓
CI/CD and staging validation
              ↓
Smoke evidence and operational checks
              ↓
Human-controlled production decision
```

## Agent roles

The workflow can use specialized roles such as:

- architecture and repository-analysis agent;
- backend implementation agent;
- Android implementation agent;
- iOS implementation agent;
- QA and regression agent;
- security-review agent;
- DevOps and incident-analysis agent;
- documentation agent.

These are task roles, not independent administrators. Every role operates within a defined scope.

## Human-owned controls

Humans define and approve:

- system architecture;
- task boundaries;
- data contracts;
- acceptance criteria;
- security constraints;
- production credentials and permissions;
- rollout plans;
- rollback conditions;
- final production changes.

## Engineering gates

Agent output is validated through:

- code review;
- linting and static checks;
- unit and integration tests;
- regression scenarios;
- security review;
- CI status;
- staging deployment;
- health checks;
- smoke evidence;
- structured logs and telemetry;
- human approval before high-impact production changes.

## Safe production model

Agents do not receive unrestricted production access. High-impact actions are separated by role and environment, while secrets remain in controlled CI/CD and infrastructure boundaries.

A production change follows the same operational path regardless of whether the implementation was written manually or accelerated by agents:

```text
Commit / pull request
        ↓
Lint and tests
        ↓
Staging deployment
        ↓
Health and smoke validation
        ↓
Manual production approval
        ↓
Rolling rollout with health gates
        ↓
Rollback or recovery if validation fails
```

## Why this matters

This workflow provides:

- faster implementation and repository analysis;
- more consistent test and documentation coverage;
- parallel work across backend, mobile, QA, and infrastructure tasks;
- explicit risk boundaries;
- reproducible delivery;
- human accountability for production behavior.

## Portfolio boundary

Private prompts, internal agent configurations, proprietary business logic, production credentials, customer data, and live infrastructure identifiers are not included in the public repository.
