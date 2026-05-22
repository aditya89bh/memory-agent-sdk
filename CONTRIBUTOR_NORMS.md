# Contributor Norms

Memory Agent SDK is an experimental developer tooling project for agent memory architecture.

The goal is to keep collaboration focused, practical, and useful for people working on AI agents, memory systems, retrieval, correction, forgetting, policies, and auditability.

## Working Style

Contributors should aim to:

- keep changes small and focused
- use one task per commit
- explain technical tradeoffs clearly
- keep examples runnable
- keep documentation accurate
- avoid unsupported production-readiness claims
- respect the current v0.1 scope

## Good Technical Feedback

Useful feedback should:

- identify the issue
- explain why it matters
- suggest a fix or alternative
- reference the relevant file, function, or doc section
- stay grounded in the current implementation

## Project Boundaries

For v0.1, the project intentionally avoids:

- LLM API dependencies
- hosted services
- vector database integrations
- framework lock-in
- production-readiness claims

This keeps the core SDK small, readable, and inspectable.

## Sensitive Data Reminder

Agent memory can contain sensitive information.

Use synthetic examples in issues, pull requests, demos, and documentation. Do not include real secrets, private data, customer records, or confidential memory content.

## Contribution Principle

Memory should behave like infrastructure: explicit, inspectable, correctable, forgettable, and auditable.

Contributions should strengthen that principle.
