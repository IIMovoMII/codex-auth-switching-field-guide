---
name: codex-auth-switching-field-guide
description: Use when designing, auditing, or repairing a machine-specific Codex workflow that switches official OAuth accounts and API-compatible endpoints while preserving live configuration, credentials, extensions, and local conversation compatibility.
---

# Codex Auth Switching Field Guide

Build a bespoke solution for the current machine. Do not copy a universal switcher blindly.

## Applicable scenarios

Use this guide when the machine needs any combination of official OAuth accounts, API-compatible endpoints, provider-specific models, preserved live Codex configuration, cross-mode local history, or transport/proxy diagnosis.

Do not treat it as a cloud-chat migration method, an account-policy bypass, or a portable credential-sharing mechanism.

## Product-brief status and implementation freedom

This repository is a product brief and experience pack for agents, not a ready-to-deploy application or a mandatory architecture. Understand the user's desired outcome, inspect the current machine, and choose an appropriate script, desktop app, native profile mechanism, or other design. Add, remove, or replace optional features to match the request.

Windows paths, fields, and workflows are validated examples. Use native equivalents elsewhere and re-probe version-sensitive behavior. Do not ask the user for facts that can be inspected safely; ask only for choices that cannot be inferred and materially change the product.

## One-prompt kickoff

When the user arrives through the README's one-prompt deployment sentence, treat it as authorization for read-only discovery and construction of a local solution. It is not blanket authorization to expose credentials, install third-party software, switch the live account, or mutate conversation history. Pause immediately before those sensitive actions when they become necessary.

## Workflow

1. Start with read-only discovery. Identify the operating system, Codex version, active processes, configuration source, credential store, active route, model, history stores, proxy behavior, and external config managers such as CC Switch.
2. Report state without reading secret values into the conversation. Show credential type and consistency, not token contents.
3. Ask one focused set of questions about the choices still unknown: target accounts and relays, whether old conversations are in scope, preferred interface, acceptable shutdown behavior, and profile-specific models or proxy policies. Do not repeat discoverable environment questions.
4. Agree on the smallest useful scope. The modules below are composable; every machine does not need every feature.
5. Establish one configuration writer. If CC Switch or another manager projects profiles into the same live file, explain the ownership conflict and require the user to choose one tool before any mutation.
6. Before the first write, ask the user to save one complete `config.toml` that has passed a real request after a fresh Codex restart. Do not silently create an unbounded backup archive.
7. Define the switcher's owned fields. Preserve every unrelated live setting, including plugins, MCP servers, skills, hooks, permissions and project configuration.
8. Model route, credential and history compatibility as separate state domains.
9. Design first use from the detected starting state. Handle "no official login yet" and "no API/relay configuration yet" explicitly; never manufacture either state.
10. Collect endpoint and model choices separately from secrets. Provide a local masked or OS-supported secret-entry path and never ask the user to paste a key into chat.
11. When requested, model multiple relays as profiles containing endpoint, protected credential reference, model and proxy policy—not full copied configs—so the user can stop using CC Switch for Codex.
12. Prove one stable provider identity for new conversations. For the built-in OpenAI route plus top-level endpoint-override architecture, use `model_provider = "openai"` in both official and API-compatible profiles only after the installed build and endpoint pass the probe; never redefine the reserved built-in `openai` provider table.
13. Treat first use as a persistent, idempotent bootstrap state machine. Save a checkpoint before every required Codex shutdown or restart, then verify the effective state from a fresh process before advancing.
14. When the user requires old conversations across modes, inventory provider values across active and archived local JSONL and every relevant SQLite store. Exclude cloud ChatGPT Work/Chat records.
15. Require a stopped-writer barrier before changing credentials or history. With explicit user approval, normalize every proven semantic local provider field to `openai`, using database-aware backups and a field-level rollback manifest. Do not assume the first JSONL line is the only copy.
16. Keep full history preparation separate from ordinary switching. Treat provider normalization and response-item compatibility as separate rules, then gate official-mode activation with a cheap fingerprint of the prepared history.
17. Use a transaction and rollback design appropriate to the platform for multi-file changes, and protect inactive credentials with native facilities.
18. Provide an offline config-recovery path for empty, malformed or generic-template files. If Codex cannot converse, allow a local script or another agent to reconstruct from the user's known-good config without exposing credentials.
19. After the relevant restart, validate the behavior selected by the user: route, authentication type, model, proxy and transport where applicable, new-session provider metadata, representative old-conversation resume when in scope, rollback, and preservation of unrelated configuration.
20. After any Codex upgrade, rerun discovery and the transport/history probes before trusting the `openai` normalization contract again.

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

- Start with [discovery](references/discovery.en.md).
- Read [architecture](references/architecture.en.md) before implementation.
- Read [first use and restart checkpoints](references/first-use-bootstrap.en.md) whenever either auth mode is absent or a setting needs a fresh Codex process to verify.
- Read [config recovery and external writers](references/config-recovery.en.md) when CC Switch or another manager is present, configuration fields disappeared, or Codex cannot converse.
- Read [optional multi-relay profiles](references/multi-relay-profiles.en.md) when the user wants several relay providers without CC Switch.
- Read [history compatibility](references/history-compatibility.en.md) whenever existing conversations must survive a route or auth change.
- Read [network diagnostics](references/network-diagnostics.en.md) for reconnects, timeouts, proxy behavior or endpoint differences.
- Read [safety and rollback](references/safety-and-rollback.en.md) before any mutation.
- Finish with [validation](references/validation.en.md).

## Deliverable

Cover the user's selected scope and at minimum explain the redacted state inventory, field ownership, first-use flow, credential boundary, failure recovery, validation evidence, and known limitations. Multi-relay support, history preparation, or a graphical interface may be omitted when the user did not select them; if included, close the corresponding loop in the routed reference.
