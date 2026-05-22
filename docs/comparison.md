# Memory Approach Comparison

Memory Agent SDK is a small set of reusable primitives for building memory-aware agents.

It is not a full agent framework, vector database, hosted memory platform, or production-ready persistence layer. It focuses on the memory lifecycle itself: deciding what to remember, retrieving useful context, correcting stale information, forgetting intentionally, and making memory behavior observable through audit events.

## Why Compare Memory Approaches?

Many agents appear to have memory, but often rely on simple shortcuts:

- keeping the full chat history
- stuffing summaries into prompts
- dumping everything into a vector database
- using framework-level memory modules without clear correction or forgetting behavior
- writing custom memory code for each project

These approaches can work for prototypes, but they often make memory hard to inspect, repair, and govern.

Memory Agent SDK exists to make memory behavior explicit.

## Comparison Table

| Approach | Strengths | Weaknesses | Best Use Case |
|---|---|---|---|
| Raw chat history | Simple, transparent, no extra system needed | Grows quickly, expensive, noisy, no correction or forgetting model | Short conversations and early prototypes |
| Prompt stuffing | Easy to implement, works with any LLM | Brittle, limited by context window, mixes relevant and irrelevant information | Small demos where memory is manually curated |
| Vector database memory | Good for semantic recall and large memory sets | Often stores too much, correction is unclear, forgetting can be neglected, retrieval may be opaque | Knowledge-heavy systems that need semantic search |
| Framework memory modules | Convenient, fast to integrate | Can hide memory behavior behind abstractions, may be tied to a specific framework | Apps already built inside a larger agent framework |
| Full agent platforms | Broad functionality, orchestration, hosting, integrations | Heavyweight when only memory primitives are needed | Teams needing full-stack agent infrastructure |
| Custom ad hoc memory code | Flexible and specific to the project | Hard to reuse, hard to test, easy to accumulate hidden behavior | One-off experiments or highly specialized systems |
| Memory Agent SDK | Small, inspectable, focused on memory lifecycle, supports correction, forgetting, policies, and audit events | Experimental, limited retrieval sophistication, no production scaling guarantees yet | Developers who want reusable memory primitives without adopting a full framework |

## When to Use Memory Agent SDK

Use this SDK when you want:

- explicit memory primitives
- local memory persistence
- correction and forgetting flows
- inspectable memory events
- a lightweight memory layer for agent prototypes
- a foundation for experimenting with memory architecture
- a reusable package across multiple agent projects

It is especially useful when you are building agents where memory should behave like a controllable system component, not an invisible side effect.

## When Not to Use It

Do not use this SDK as-is when you need:

- production-grade security
- encrypted storage
- access control
- distributed storage
- high-concurrency guarantees
- large-scale semantic search
- hosted memory infrastructure
- compliance-grade retention controls

For those cases, this SDK should be treated as an architectural reference or starting point, not a finished production system.

## What Makes It Different

The main difference is that Memory Agent SDK treats memory as a lifecycle.

A memory does not just get written once and live forever. It may need to be:

1. Created
2. Retrieved
3. Used
4. Corrected
5. Superseded
6. Forgotten
7. Audited

This makes the SDK closer to a memory control layer than a storage wrapper.

## Why Correction Matters

Agents often remember wrong things.

A user may change preferences. A fact may become outdated. A previous assumption may be incorrect. If a memory system only supports adding new memories, it gradually accumulates contradictions.

Correction allows the system to repair memory without pretending the old version never existed.

This matters for trust, debugging, and long-running agent behavior.

## Why Forgetting Matters

Forgetting is not a failure mode. It is a feature.

Without forgetting, memory systems become bloated, noisy, stale, and harder to govern. Useful memory requires boundaries.

Forgetting helps with:

- removing temporary state
- deleting outdated preferences
- reducing retrieval noise
- respecting retention policies
- keeping agent behavior focused

## Why Audit Events Matter

Memory behavior should be visible.

If an agent retrieves, corrects, or forgets something, developers should be able to inspect that behavior. Audit events make the memory layer easier to debug and reason about.

This is useful for:

- understanding why an agent behaved a certain way
- checking whether retrieval worked correctly
- verifying correction and forgetting flows
- building future memory evaluation tools

## Current Limitations

Memory Agent SDK is currently experimental.

Known limitations:

- retrieval is simple and local
- no embedding-based retrieval yet
- no vector store adapters yet
- no async API
- no concurrency guarantees
- no encryption layer
- no access control
- no schema migration system
- no production benchmarking
- no hosted service

These limitations are intentional for v0.1. The goal is to keep the foundation small, inspectable, and easy to extend.

## Design Position

Memory Agent SDK is for developers who want memory primitives without immediately adopting a full agent framework.

It should be seen as:

- smaller than a full agent platform
- more structured than raw chat history
- more lifecycle-aware than simple vector memory
- more reusable than custom project-specific memory code

The long-term direction is to become a practical memory infrastructure layer for agent developers.
