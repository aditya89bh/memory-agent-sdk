# Security Policy

Memory Agent SDK is currently an experimental developer SDK for learning, prototyping, and portfolio-grade demonstrations of agent memory architecture.

It is not production-ready security infrastructure.

## Supported Versions

| Version | Supported |
|---|---|
| v0.1.x | Experimental support |

## Security Scope

This project currently focuses on local memory primitives:

- in-memory storage
- JSON file storage
- SQLite storage
- retrieval
- correction
- forgetting
- audit events
- memory policies

The SDK does not currently provide:

- encryption at rest
- access control
- authentication
- authorization
- multi-tenant isolation
- secret management
- production retention controls
- compliance guarantees
- secure distributed storage

Do not use this SDK as-is for sensitive production memory workloads.

## Reporting a Vulnerability

If you find a security issue, open a GitHub issue with:

- a clear description of the problem
- reproduction steps
- affected files or APIs
- expected vs actual behavior
- suggested mitigation, if known

Avoid posting real secrets, personal data, private keys, customer data, or sensitive production memory records in public issues.

## Sensitive Data Guidance

Agent memory can contain sensitive information.

Until this SDK has stronger privacy and security controls, avoid storing:

- passwords
- API keys
- private tokens
- financial data
- health data
- government IDs
- confidential customer data
- private personal information

Use synthetic or local test data for demos and examples.

## Current Security Posture

The current repo includes:

- tests
- CI
- documented production-readiness gaps
- explicit warnings around sensitive production use
- local-only storage backends

The current repo does not include formal security review, threat modeling, encrypted storage, or hardened deployment guidance.

## Production Hardening Roadmap

Before production use, the SDK would need:

- encryption support
- access control model
- retention and deletion guarantees
- schema migrations
- audit log hardening
- concurrency guarantees
- secure configuration handling
- privacy review
- threat model
- integration tests for persistence failure modes

See `docs/production_readiness.md` for the broader production-readiness roadmap.
