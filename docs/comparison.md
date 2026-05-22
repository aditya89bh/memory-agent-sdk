# Memory Approach Comparison

`memory-agent-sdk` is a lightweight set of memory primitives for agent builders who want memory behavior to be explicit, inspectable, and framework-neutral. It is not a full agent platform, a hosted memory service, or production infrastructure.

This page compares the SDK with common ways developers add memory to agents. The goal is positioning, not claiming that one approach is universally better.

## Comparison table

| Approach | What it is good for | Typical tradeoffs | Where Memory Agent SDK fits |
|---|---|---|---|
| Raw chat history | Keeping recent conversation context with almost no extra machinery. | Grows with the conversation, mixes useful facts with noise, and usually has no explicit correction, forgetting, or audit trail. | Adds structured long-term records alongside session memory, with lifecycle operations instead of replaying every turn. |
| Prompt stuffing | Fast prototypes where the developer manually injects notes, summaries, or facts into the prompt. | Easy to start but hard to maintain as memory grows; provenance and cleanup are usually manual. | Provides explicit `remember`, `retrieve`, `correct`, and `forget` operations so prompt context can be built from selected records. |
| Vector database memory | Semantic retrieval across large collections of embedded text. | Requires embeddings, external services or extra dependencies, retrieval evaluation, and separate lifecycle logic for correction and deletion. | Does not replace vector search. It offers standard-library local stores and deterministic retrieval primitives that can later be adapted to vector stores. |
| Framework memory modules | Convenient memory features inside an agent framework. | Behavior may be coupled to that framework's abstractions, storage choices, or execution model. | Keeps memory primitives framework-neutral so they can be used from a plain Python loop, tests, examples, or future adapters. |
| Full agent platforms | End-to-end orchestration, hosted tools, deployment, observability, and integrated memory features. | More capability, but also more platform commitment and often less control over low-level memory mechanics. | Focuses only on memory architecture primitives. It can support experiments before choosing a larger platform, but it is not a platform replacement. |
| Custom ad hoc memory code | Maximum flexibility for one project and no dependency on a memory library. | Often starts simple but can become inconsistent: duplicated schemas, unclear retention rules, no correction history, and limited tests. | Provides reusable primitives and tests for common memory lifecycle concerns while still staying small and readable. |

## When to use Memory Agent SDK

Use `memory-agent-sdk` when you want to:

- prototype agent memory without adopting a full agent framework;
- keep memory behavior visible in plain Python code;
- separate session memory, long-term records, retrieval, policy, correction, forgetting, and audit events;
- run local examples or tests without API keys, hosted services, or non-standard-library runtime dependencies;
- demonstrate or teach memory lifecycle design;
- build a foundation that could later gain adapters for vector stores, frameworks, or production storage.

## When not to use it

Do not use the SDK as-is when you need:

- production-grade durability, backups, migrations, or recovery guarantees;
- concurrent writers, distributed storage, or high-volume retrieval;
- encryption, access control, tenancy, or regulated data governance;
- semantic vector search over large corpora;
- managed hosting, deployment, monitoring, or agent orchestration;
- a mature ecosystem of integrations and production support.

For those needs, a database, vector search system, agent framework, hosted platform, or custom production service may be the right choice. The SDK can still be useful as a reference for lifecycle concepts, but it should not be treated as hardened infrastructure.

## What makes it different

The SDK's main distinction is that it treats memory as a lifecycle, not just as stored text.

A memory can be created, retrieved, corrected, forgotten, expired, and audited. These operations are exposed as direct primitives instead of being hidden inside prompt construction or a framework callback. That makes the behavior easier to inspect during development and easier to test in small examples.

The current implementation is intentionally modest:

- standard-library-first Python;
- local in-memory, JSON, and SQLite stores;
- deterministic retrieval using keyword overlap, recency, importance, and tags;
- explicit correction and forgetting helpers;
- audit events for major memory operations.

This is useful for learning, portfolio work, architecture experiments, and early prototypes. It is not evidence that the SDK outperforms vector search, agent frameworks, or production platforms on scale, retrieval quality, or operational maturity.

## Why correction and forgetting matter

Agent memory can become harmful when outdated or incorrect information keeps resurfacing. Raw history and simple note stores often preserve old statements even after the user corrects them. That can make an agent confidently repeat stale preferences, wrong facts, or decisions that have been reversed.

Correction and forgetting make memory maintenance explicit:

- **Correction** lets a newer memory supersede an older one without pretending the old record never existed.
- **Forgetting** lets an agent stop using records that are irrelevant, expired, sensitive, or explicitly removed.
- **Expiry** supports time-bound memory instead of treating every remembered fact as permanent.

These operations matter because long-term memory is not only about recall. It is also about knowing when not to recall something.

## Why audit events matter

Audit events help answer questions that are difficult to debug from final prompts alone:

- What did the agent store?
- Why did a record appear in retrieval results?
- When was a memory corrected or forgotten?
- Which records are active, superseded, expired, or inactive?

In early prototypes, audit events make memory behavior easier to inspect and explain. In production systems, auditability would need to be much stronger than the current SDK provides, but the primitive is included because observability is part of responsible memory design.

## Honest limitations

`memory-agent-sdk` is experimental and intentionally small. Current limitations include:

- no concurrency guarantees;
- no distributed storage;
- no encryption or access-control layer;
- no schema migration system;
- no async API;
- no vector database adapter in the core package;
- limited retrieval sophistication compared with embedding-based semantic search;
- no large-scale retrieval benchmarks;
- no production privacy, retention, or compliance framework;
- no full agent orchestration, tool routing, deployment, or hosted UI.

The SDK is best understood as a clean memory architecture toolkit for local development and demonstration. It gives developers explicit building blocks for memory behavior, while leaving production hardening and advanced retrieval integrations as future work.
