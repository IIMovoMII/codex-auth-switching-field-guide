---
name: codex-auth-switching-field-guide
description: Use when designing, auditing, or repairing a machine-specific Windows workflow that switches Codex between official OAuth accounts and API-compatible endpoints while preserving live configuration, credentials, plugins, MCP, skills, hooks, and local conversation compatibility.
---

# Codex Auth Switching Field Guide

Build a bespoke solution for the current machine. Do not install or copy a universal switcher.

## Applicable scenarios

Use this guide when the machine needs any combination of official OAuth accounts, API-compatible endpoints, provider-specific models, preserved live Codex configuration, cross-mode local history, or transport/proxy diagnosis.

Do not treat it as a cloud-chat migration method, an account-policy bypass, or a portable credential-sharing mechanism.

## One-prompt kickoff

When the user arrives through the README's one-prompt deployment sentence, treat it as authorization for read-only discovery and construction of a local solution. It is not blanket authorization to expose credentials, install third-party software, switch the live account, or mutate conversation history. Pause immediately before those sensitive actions when they become necessary.

## Workflow

1. Start with read-only discovery. Identify the Codex version, active processes, configuration source, credential store, active route, model, history stores, proxy behavior and requested profile set.
2. Report state without reading secret values into the conversation. Show credential type and consistency, not token contents.
3. Define the switcher's owned fields. Preserve every unrelated live setting, including plugins, MCP servers, skills, hooks, permissions and project configuration.
4. Model route, credential and history compatibility as separate state domains.
5. Design first use from the detected starting state. Never manufacture an OAuth session or assume a missing API credential.
6. Require a stopped-writer barrier before changing credentials or history.
7. Journal the previous state before every multi-file transition. Use OS-protected storage for inactive credentials.
8. Keep full history preparation separate from ordinary switching. Gate official-mode activation with a cheap fingerprint of the prepared history.
9. Validate effective behavior: route, authentication type, model availability, proxy path, transport, conversation resume, rollback and preservation of unrelated configuration.
10. After any Codex upgrade, rerun discovery and the transport/history probes.

## Non-negotiable safety rules

- Never expose, log, commit or ask a model to inspect credential values.
- Never replace an entire live configuration merely to change auth mode.
- Never rewrite active JSONL history or raw-copy a live WAL database.
- Never rename generic response identifiers blindly. Classify records by semantic type.
- Never fabricate a reasoning identifier when the protected reasoning payload required by the target endpoint is unavailable.
- Preserve tool-call and tool-result pairing.
- Abort before the first write when preflight or compatibility gates fail.
- Roll back only journaled fields or records; do not overwrite newer user activity.

## Read references as needed

- Start with [discovery](references/discovery.md).
- Read [architecture](references/architecture.md) before implementation.
- Read [history compatibility](references/history-compatibility.md) whenever existing conversations must survive a route or auth change.
- Read [network diagnostics](references/network-diagnostics.md) for reconnects, timeouts, proxy behavior or endpoint differences.
- Read [safety and rollback](references/safety-and-rollback.md) before any mutation.
- Finish with [validation](references/validation.md).

## Deliverable

Produce a machine-specific design or implementation with:

- a state inventory;
- explicit field ownership;
- a first-use flow;
- secure credential handling;
- transaction and rollback behavior;
- a separate history-preparation command;
- a versioned validation report;
- known limits and recovery instructions.
