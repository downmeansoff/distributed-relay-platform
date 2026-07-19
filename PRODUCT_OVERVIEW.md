# Fortune Network Platform — Product Overview

This document describes the product and engineering scope of the private production platform without exposing customer data, credentials, private domains, infrastructure identifiers, billing secrets, or proprietary business logic.

## Product summary

The platform is a multi-client network product used by **1,000+ users** across **7 production infrastructure nodes** and **5 client channels**:

- web;
- Android;
- iOS;
- Telegram;
- external clients.

The product is not only a relay fleet. It combines mobile applications, shared backend contracts, account and device management, subscription and entitlement logic, server-side usage policy, telemetry, support operations, distributed infrastructure, and controlled production delivery.

## End-to-end product flow

```text
User registration / authentication
                ↓
Account and device registration
                ↓
Entitlement and capability evaluation
                ↓
Region and transport policy selection
                ↓
Session allocation and credential delivery
                ↓
Connection through distributed infrastructure
                ↓
Usage accounting, telemetry and support signals
                ↓
Renewal, recovery, revocation or fallback
```

## Product architecture

```text
Web / Android / iOS / Telegram / External clients
                         ↓
                 Shared API contracts
                         ↓
                  Go control plane
      Auth · Devices · Entitlements · Billing
      Sessions · Usage · Telemetry · Support
                         ↓
                    PostgreSQL
                         ↓
             Distributed network layer
                  7 production nodes
```

## Shared control plane

The production Go control plane is the source of truth for:

- authentication and account lifecycle;
- device registration, limits, and revocation;
- account-level entitlements and client capabilities;
- billing and rewarded-access flows;
- region and transport policy publication;
- transport session allocation, rotation, and revocation;
- server-side traffic accounting and quota enforcement;
- telemetry, metrics, support metadata, and audit events;
- guarded orchestration of distributed infrastructure.

Clients consume versioned contracts instead of reimplementing product policy independently.

## Product responsibilities I led

- requirements and product architecture;
- decomposition into backend, mobile, infrastructure, and operational workstreams;
- Android and iOS delivery coordination;
- shared API contracts and data-model design;
- acceptance criteria, release preparation, and production validation;
- monitoring, rollout, rollback, and incident readiness;
- controlled use of coding agents for implementation, QA, documentation, and security review.

## Why this architecture matters

### One backend for several product surfaces

Authentication, devices, entitlements, usage limits, and transport behavior are centrally managed. This prevents five client channels from drifting into different product rules.

### Server-owned policy

The server evaluates account access, device limits, quotas, and capabilities. Clients display and apply the resulting policy rather than becoming independent sources of truth.

### Replaceable infrastructure

Infrastructure nodes can be added, removed, or excluded without redesigning every client because clients interact with stable backend contracts rather than node-specific implementation details.

### Observable operations

Health checks, telemetry, structured logs, audit events, and support metadata make runtime behavior diagnosable and reduce the time between a user report and an actionable technical explanation.

## Business value

- supported growth to 1,000+ users through one centrally controlled product architecture;
- reduced duplication across web, Android, iOS, Telegram, and external clients;
- improved release safety through staging, smoke checks, rolling rollout, and rollback;
- shortened incident diagnosis through stable contracts, health data, telemetry, and evidence collection;
- accelerated delivery with controlled AgentOps while preserving human ownership of architecture and production risk.

## Public/private boundary

The runnable public repository demonstrates architecture, Docker topology, a minimal API, PostgreSQL, monitoring, health checks, and CI/CD.

The production Go backend, mobile source code, customer data, billing integrations, live infrastructure, credentials, and proprietary business logic remain private.
