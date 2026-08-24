<div align="center">

# Codex Auth Switching Field Guide

**Build a machine-specific, rollback-first workflow for switching Codex between official OAuth accounts and API-compatible endpoints on Windows.**

[![Field Guide](https://img.shields.io/badge/type-field%20guide-6f42c1)](#what-this-is)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4)](#scope)
[![Codex](https://img.shields.io/badge/focus-Codex%20Desktop%20%2B%20CLI-111827)](#scope)
[![Validation](https://github.com/IIMovoMII/codex-auth-switching-field-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/IIMovoMII/codex-auth-switching-field-guide/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

[简体中文](README.zh-CN.md) · [Agent entrypoint](SKILL.md) · [Companion notification guide](https://github.com/IIMovoMII/codex-desktop-notification-field-guide)

</div>

## What this is

This repository is **not a universal switcher to install**. It is a field guide for an engineer or coding agent to inspect one Windows machine, understand its Codex version and local state, then build the smallest safe switcher that fits that environment.

The hard part is not changing one URL. A dependable design must preserve a live <code>config.toml</code>, isolate credentials, keep old conversations resumable, survive interrupted writes, and explain exactly what happens on first use.

## The problem

A single Codex installation may need to alternate between:

- official OpenAI OAuth accounts;
- one or more API keys or relay providers;
- provider-specific model catalogs;
- different proxy requirements;
- a shared set of plugins, MCP servers, skills, hooks, permissions, and projects;
- local conversations created under earlier routing choices.

Copying entire configuration files appears simple, but it silently freezes unrelated settings. Reusing one credential file without a transaction can leave configuration and authentication out of sync. Rewriting active conversation files can corrupt history. Treat switching as a state transition, not a file-copy trick.

## Concrete use cases

| Situation | What a machine-specific implementation should achieve |
| --- | --- |
| One PC alternates between official OAuth and an API-compatible relay | Switch route and credential as one transaction while keeping one evolving Codex configuration |
| Several official accounts are used on the same Windows profile | Keep each OAuth snapshot protected and make account identity explicit before activation |
| Several API providers expose different model catalogs | Bind endpoint, credential, model and proxy policy to each profile without cloning the whole config |
| Plugins, MCP servers, skills or hooks are edited frequently | Start every switch from the live configuration so unrelated changes survive |
| Old local conversations contain provider names from earlier relay definitions | Inventory active and archived history, then normalize every proven local provider field to `openai` before cross-mode use |
| Relay-created conversations fail when resumed through the official endpoint | Prepare response-item compatibility separately from provider normalization, preserve valid records and keep a tested rollback manifest |
| The first turn repeatedly reconnects or times out | Diagnose HTTPS, WebSocket, base-path and system-proxy behavior instead of blaming auth or history blindly |
| No official OpenAI login has ever existed on the machine | Preserve the known API state, stage the official route, let the user complete OAuth, restart Codex and verify the resulting official session before capturing it |
| No relay/API profile or key has ever been configured | Ask for non-secret endpoint and model choices, provide a local secret-entry path, restart Codex and verify the real route before calling the profile ready |
| Some settings are observable only after a Codex restart | Persist a bootstrap checkpoint, tell the user exactly what to do next, and continue post-restart verification instead of claiming success in one pass |

This guide is not intended to sync cloud ChatGPT conversations, bypass account policy, share credentials between people, or provide a universal executable that assumes every Codex release has the same storage layout.

## Deploy in one prompt

Copy this sentence into a new Codex task:

~~~text
Codex, read https://github.com/IIMovoMII/codex-auth-switching-field-guide, begin with a read-only inspection of this Windows machine's Codex version, effective configuration, authentication type, local history stores and network routes, then design and build a rollback-first switcher tailored to this machine for official OAuth accounts and API-compatible providers, explicitly handling a missing official login and a missing API/relay configuration, using local secret entry rather than asking for keys in chat, preserving the live config's plugins, MCP servers, skills, hooks, permissions and projects, supporting provider-specific models and proxy policies, and using `model_provider = "openai"` for both official and API-compatible profiles only after proving that contract on the installed Codex build. Make history preparation a separate operation: scan every active and archived local rollout plus every relevant SQLite store, report distinct provider values without exposing conversation text, and, after my confirmation and a full Codex shutdown, use verified backups and a field-level rollback manifest to normalize all semantically equivalent local provider metadata to `openai`; keep cloud ChatGPT Work/Chat records out of scope, keep response-item ID repair separate, and ensure future sessions are also created as `openai`. Implement first use as persistent restart checkpoints because some values can only be verified after Codex fully restarts, pause for my confirmation before changing live credentials or conversation history, and finally validate every post-restart state, profile switching, rollback, network behavior, new-session metadata and representative old-conversation resume in both modes.
~~~

This is “deployment” by delegation, not a binary installer. The sentence authorizes read-only discovery and construction of a local solution; it does not authorize silent third-party installation, credential disclosure or unconfirmed history mutation.

## Architecture

~~~mermaid
flowchart LR
    U[Requested profile] --> P[Preflight and process barrier]
    P --> F[Read the live configuration]
    F --> M[Patch only owned fields]
    M --> A[Activate protected credential snapshot]
    A --> V[Validate route, auth, model and history gate]
    V --> C[Commit transaction]
    V -->|failure| R[Field-level rollback]

    H[Explicit history preparation] --> G[Compatibility fingerprint]
    G --> V
~~~

The switcher owns a narrow set of fields. Everything else remains live and keeps evolving.

| Concern | Recommended source of truth |
| --- | --- |
| Plugins, MCP, skills, hooks, permissions | Current live Codex configuration |
| Active endpoint and model | Selected profile, applied as a surgical patch |
| Active credential | Codex credential file or supported secure store |
| Inactive credentials | OS-protected snapshots, never plain project files |
| Conversation compatibility | Separate, explicit preparation record |
| Recovery | Durable transaction journal plus verified backups |

## Core design rules

1. **Discover before designing.** Codex configuration, storage, process names and transport behavior change across releases.
2. **Never swap the whole configuration.** Patch only the fields the switcher explicitly owns.
3. **Separate routing, authentication and history.** They interact, but they are different state domains.
4. **Stop writers before sensitive changes.** Configuration, credentials and history should not be mutated while Codex processes can append or reload them.
5. **Make first use a real workflow.** Detect whether the machine starts in official, API or inconsistent state; do not invent a missing credential snapshot.
6. **Keep history repair out of the fast path.** Inventory and normalize historical provider identity once, run response-item repair separately, then use a cheap fingerprint gate during switching.
7. **Journal before writing.** Every multi-file transition needs a recoverable previous state.
8. **Verify the route, not just the TOML.** A syntactically valid profile can still use the wrong credential, proxy, transport or model.

## First-use decision tree

~~~mermaid
flowchart TD
    S[Inspect current machine] --> K{Current state is consistent?}
    K -->|No| X[Stop and explain the mismatch]
    K -->|Yes, official| O[Register official state]
    K -->|Yes, API| A[Register API state]
    O --> L[Ask the user to perform one intentional API login/setup]
    A --> L2[Ask the user to perform one intentional official login]
    L --> P[Capture the second state only after validation]
    L2 --> P
    P --> R[Profiles are ready]
~~~

The arrows are restart checkpoints, not one uninterrupted inspection. Stage the intended change, save progress, fully restart Codex, verify what the fresh process actually loaded, and only then advance to the next phase.

A switcher cannot create an official OAuth session that has never existed, nor should it ask a model to read secrets. On first use, it records the known-good current state, guides the user through one intentional setup of the missing mode, validates it, and only then creates the second protected snapshot.

## One provider identity for old and new local conversations

For the official-plus-API-compatible architecture described here, the preferred target is:

~~~toml
model_provider = "openai"
~~~

Official mode removes `openai_base_url`; an API-compatible profile sets that top-level override and activates its own credential. The current [Codex configuration reference](https://developers.openai.com/codex/config-reference) identifies `openai` as the built-in default provider and `openai_base_url` as its endpoint override. Do not try to redefine the reserved built-in provider with a `[model_providers.openai]` table.

Before relying on that layout, prove it on the installed Codex build and intended endpoint. Then run a separate history-preparation operation:

1. scan active and archived local JSONL plus every relevant SQLite store and count each provider value;
2. distinguish local rollouts from cloud ChatGPT Work/Chat records;
3. fully stop every Codex writer, create database-aware backups and write a rollback manifest;
4. structurally normalize every proven local provider field to `openai`, not only the first metadata line;
5. validate JSONL, SQLite, new-session metadata and representative old-session resume in both official and API-compatible modes.

Provider normalization makes local conversation identity consistent. It does not repair incompatible historical response-item IDs; run that semantic check in the same preparation phase but as a separate repair rule.

## Guide map

| Read this | When you need to |
| --- | --- |
| [Discovery](references/discovery.md) | Inventory Codex, configuration, credentials, history and endpoint capabilities |
| [Architecture](references/architecture.md) | Define profile ownership, first-use flow and transactions |
| [First use and restart checkpoints](references/first-use-bootstrap.md) | Initialize a missing official or API state across the required Codex restarts |
| [History compatibility](references/history-compatibility.md) | Keep local conversations resumable across auth modes |
| [Network diagnostics](references/network-diagnostics.md) | Separate HTTPS, WebSocket, relay and system-proxy failures |
| [Safety and rollback](references/safety-and-rollback.md) | Protect credentials and recover from interrupted writes |
| [Validation](references/validation.md) | Build a test matrix before trusting the switcher |

## Hard-won lessons

- A provider label can affect how local conversations are discovered even when the effective endpoint comes from another setting; fixing only future configuration leaves old mixed-provider sessions behind.
- Provider identity can be repeated in session metadata, thread-settings events and SQLite thread rows. Normalization must cover every semantic copy discovered for that build.
- A relay that accepts HTTPS Responses requests may still reject or omit the Responses WebSocket route.
- Repeated reconnect messages on the first turn can be a transport fallback symptom, not a damaged conversation.
- OAuth and API credentials may share a live storage location; configuration switching alone does not switch identity.
- A valid pre-restart file is only a staged intention. Values that Codex loads at process start must be verified from a fresh process before the profile is marked ready.
- A historical response item with a generic identifier is not automatically valid for an official endpoint that expects a typed identifier.
- Reasoning records are special: if their required protected content cannot be recovered, deleting the model-input copy can be safer than fabricating an identifier.
- SQLite databases using WAL require database-aware backup and integrity checks.
- Equal-length in-place JSONL edits can reduce risk in a narrowly proven case, but a stopped-writer repair remains the default.
- A full history scan on every switch creates delay without improving safety. Prepare once, fingerprint, then re-prepare only after the history changes.
- Version-sensitive feature flags must be probed after upgrades rather than treated as permanent facts.

## Using this with a coding agent

Point the agent at [SKILL.md](SKILL.md) and ask it to design a switcher for the current machine. The agent should:

1. perform read-only discovery;
2. show the detected state without exposing secret values;
3. propose a field-ownership and recovery model;
4. obtain user confirmation before credential or history mutation;
5. implement a local solution appropriate to the detected Codex build;
6. run the full validation matrix.

The guide deliberately avoids distributing a ready-made credential manager. Local paths, Codex builds, relay behavior, account count and acceptable risk differ too much for blind installation to be responsible.

## Scope

The patterns are aimed at Codex Desktop and Codex CLI on Windows. They may help on other platforms, but path handling, process barriers, credential storage and filesystem semantics must be redesigned.

An observed setup successfully used `openai` for both future and historical local provider metadata while changing only the top-level endpoint and credential state. That is evidence for a pattern, not a promise that the same history fields or semantics remain valid in every Codex release. Re-run discovery after upgrades.

## Security

- Never commit <code>auth.json</code>, tokens, relay URLs containing credentials, or local state snapshots.
- Do not print token values during diagnostics.
- Protect inactive credentials with the operating system and restrict file permissions.
- Keep a redacted audit trail of transitions.
- Treat conversation files as private user data.

See [SECURITY.md](SECURITY.md) before sharing logs or examples.

## Contributing

Contributions should add reproducible observations, version context and a safe validation method. Avoid machine-specific code presented as universal behavior. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). The guide is provided without warranty; authentication and history migration remain the operator's responsibility.
