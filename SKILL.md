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

1. Start with read-only discovery. Identify the Codex version, active processes, configuration source, credential store, active route, model, history stores, proxy behavior, requested profile set, and external config managers such as CC Switch.
2. Report state without reading secret values into the conversation. Show credential type and consistency, not token contents.
3. Establish one configuration writer. If CC Switch or another manager projects profiles into the same live file, explain the ownership conflict and require the user to choose one tool before any mutation.
4. Before the first write, ask the user to save one complete `config.toml` that has passed a real request after a fresh Codex restart. Do not silently create an unbounded backup archive.
5. Define the switcher's owned fields. Preserve every unrelated live setting, including plugins, MCP servers, skills, hooks, permissions and project configuration.
6. Model route, credential and history compatibility as separate state domains.
7. Design first use from the detected starting state. Handle "no official login yet" and "no API/relay configuration yet" explicitly; never manufacture either state.
8. Collect endpoint and model choices separately from secrets. Provide a local masked or OS-supported secret-entry path and never ask the user to paste a key into chat.
9. When requested, model multiple relays as profiles containing endpoint, protected credential reference, model and proxy policy—not full copied configs—so the user can stop using CC Switch for Codex.
10. Prove one stable provider identity for new conversations. For the built-in OpenAI route plus top-level endpoint-override architecture, use `model_provider = "openai"` in both official and API-compatible profiles only after the installed build and endpoint pass the probe; never redefine the reserved built-in `openai` provider table.
11. Treat first use as a persistent, idempotent bootstrap state machine. Save a checkpoint before every required Codex shutdown or restart, then verify the effective state from a fresh process before advancing.
12. Before the first cross-mode activation, inventory provider values across active and archived local JSONL and every relevant SQLite store. Exclude cloud ChatGPT Work/Chat records.
13. Require a stopped-writer barrier before changing credentials or history. With explicit user approval, normalize every proven semantic local provider field to `openai`, using database-aware backups and a field-level rollback manifest. Do not assume the first JSONL line is the only copy.
14. Journal the previous state before every multi-file transition. Use OS-protected storage for inactive credentials.
15. Keep full history preparation separate from ordinary switching. Treat provider normalization and response-item compatibility as separate rules, then gate official-mode activation with a cheap fingerprint of the prepared history.
16. Provide an offline config-recovery path for empty, malformed or generic-template files. If Codex cannot converse, allow a local script or another agent to reconstruct from the user's known-good config without exposing credentials.
17. Validate effective behavior after the relevant restart: route, authentication type, model availability, proxy path, transport, new-session provider metadata, representative old-conversation resume in both modes, rollback and preservation of unrelated configuration.
18. After any Codex upgrade, rerun discovery and the transport/history probes before trusting the `openai` normalization contract again.

## Non-negotiable safety rules

- Never expose, log, commit or ask a model to inspect credential values.
- Never mark a newly created profile ready from pre-restart file inspection alone.
- Never replace an entire live configuration merely to change auth mode.
- Never let two profile managers alternate ownership of the same live `config.toml`.
- Never claim that a deleted config value was recovered when it was inferred or recreated.
- Never rewrite active JSONL history or raw-copy a live WAL database.
- Never normalize provider values with global text replacement or assume all provider names have equal byte length.
- Never change cloud ChatGPT Work/Chat records as though they were local rollout files.
- Never rename generic response identifiers blindly. Classify records by semantic type.
- Never fabricate a reasoning identifier when the protected reasoning payload required by the target endpoint is unavailable.
- Preserve tool-call and tool-result pairing.
- Abort before the first write when preflight or compatibility gates fail.
- Roll back only journaled fields or records; do not overwrite newer user activity.

## Read references as needed

- Start with [discovery](references/discovery.md).
- Read [architecture](references/architecture.md) before implementation.
- Read [first use and restart checkpoints](references/first-use-bootstrap.md) whenever either auth mode is absent or a setting needs a fresh Codex process to verify.
- Read [config recovery and external writers](references/config-recovery.md) when CC Switch or another manager is present, configuration fields disappeared, or Codex cannot converse.
- Read [optional multi-relay profiles](references/multi-relay-profiles.md) when the user wants several relay providers without CC Switch.
- Read [history compatibility](references/history-compatibility.md) whenever existing conversations must survive a route or auth change.
- Read [network diagnostics](references/network-diagnostics.md) for reconnects, timeouts, proxy behavior or endpoint differences.
- Read [safety and rollback](references/safety-and-rollback.md) before any mutation.
- Finish with [validation](references/validation.md).

## Deliverable

Produce a machine-specific design or implementation with:

- a state inventory;
- explicit field ownership;
- a first-use flow;
- one-writer ownership and offline config-recovery instructions;
- optional multi-relay profile behavior when requested;
- secure credential handling;
- transaction and rollback behavior;
- a separate history-preparation command;
- a redacted before/after inventory proving historical and future local provider metadata use the verified stable identity;
- a versioned validation report;
- known limits and recovery instructions.
