---
name: codex-auth-switching-field-guide
description: Design, review or repair a machine-specific Codex official OAuth/API relay switcher while preserving evolving configuration, local history and failure recovery. This is implementation guidance, not an installer.
---

# Product brief for agents

[简体中文](SKILL.md)

## Product-brief status

This is reference experience, not a specification to copy mechanically. Choose an implementation after understanding the user's goals, installed Codex, OS credential mechanisms and history layout. Scripts, small apps and native profiles are all possible; add or remove capabilities to fit the request. Windows evidence does not establish compatibility elsewhere.

The one-prompt request authorizes building, not secret publication, unexplained service installation, live identity replacement or history mutation. Honor authorization already given without asking again for the same action; explain shutdown, login or expanded mutation scope before proceeding.

## Start here

Read [discovery](references/discovery.en.md). Inspect facts safely available on the machine. Ask only unresolved choices affecting the result: account/relay count, old-thread continuity, interface, model preferences and acceptable shutdown timing. Do not ask for an OS you can inspect or a key pasted into chat.

The one configuration writer principle coordinates routing ownership; it does not prohibit user edits. Preserve unowned live settings. Coexistence with other managers requires a verified coordination mechanism.

## Implementation path

1. Read [architecture](references/architecture.en.md). Separate route, credentials, history and post-restart verification states. Define acceptance for the capabilities the user selected.
2. Handle no official login yet, no API/relay configuration yet, expired credentials and incomplete profiles through [first use](references/first-use-bootstrap.en.md). The user completes actual login; the tool persists progress, never fabricates OAuth.
3. For cross-mode old-thread continuity, read [history compatibility](references/history-compatibility.en.md). Common provider identity and response-item compatibility are separate tasks. Verify and preserve pagination projections and inheritance.
   Prefix, length and reasoning-content checks are insufficient: legal IDs with encrypted content can still trigger server lookup during native continuation after warmup. For that error or a proposed old-ID change, read the [continuation case study](references/continuation-case-study.en.md) and reproduce the actual request path first. Clear only old model-input IDs proven optional through type, reference and native-copy checks, never every ID or the reasoning content. If the gate reports unverified model/UI independence for a terminated subagent with no UI items, read [empty subagent projection](references/empty-subagent-projection.en.md); it adds only the proven `failed + task_complete` or `interrupted + turn_aborted(reason=interrupted)` states and does not remove general provenance gates.
4. A routine one-action flow may be: stopped-writer check → quick readiness check → necessary preparation → route/credential transaction → restart and acceptance guidance. Separate internal stages without forcing multiple manual commands.
5. Implement failure paths using [safety and rollback](references/safety-and-rollback.en.md), and test selected capabilities with [validation](references/validation.en.md). Failed preparation must precede activation of target credentials.

Keep responsibilities clear: centralize switch sequencing, failure handling and transaction coordination; isolate version-dependent config/auth representations, history and transport decisions. A few functions or files are sufficient, with no plugin framework or resident service required. Implement only selected capabilities; see architecture for upgrade and cache rules.

## Conditional routes

- Multiple providers, models or reasoning levels: [multi-relay profiles](references/multi-relay-profiles.en.md).
- Empty/template-overwritten config or CC Switch coexistence: [config recovery](references/config-recovery.en.md).
- First-turn retries, proxies or timeouts: [network diagnostics](references/network-diagnostics.en.md).
- Slow switching: measure stages first. When scale warrants optimization, read [incremental preparation](references/incremental-preparation.en.md). Reuse valid file results and parse appends after full-prefix proof; still check database dependencies and retain forced-complete inspection. Small slot backups have a narrow boundary. Less parsing does not mean no old-data reads.
- A stable context limit across modes: see architecture's context policy. Honor the user's choice and verify config, catalog, cache and new-process effective values. The local 272000 choice is not a default for everyone or a claim that every request is billed at the maximum.
- After a Codex update: establish whether relevant behavior remains covered by verified rules. A new version does not necessarily need a code change, and unchanged table structure does not prove unchanged behavior. Keep unknown compatibility write-gated and update readiness evidence only after verification.

## Invariants

- Never display or publish credentials, real transcripts or history backups. Prefer types, counts and redacted diagnostic categories.
- Do not overwrite evolving live settings with a saved whole config, or silently downgrade model or reasoning level.
- Formal bulk history repair requires stopped writers. An exceptional live single-thread recovery does not remove that gate.
- Mutate only proven local history. Do not sweep cloud Chat/Work or database rows without a local correspondence into the migration.
- Do not truncate or fabricate reasoning IDs/encrypted payloads, break tool pairing or create paginated ordinal gaps by deleting lines.
- Unknown layouts, inconsistent provenance or concurrent changes require a stop, not a manually bumped readiness version.
- Rollback cannot overwrite activity created after the repair. If reversal is unsafe, expose a clear manual-recovery state.
- Inspect durable manifests before starting new switching or repair when history work is unfinished. Accept exception handling, simulated interruption, actual process termination and power-loss recovery separately. Reverse only known changes; one simulation cannot prove universal automatic crash recovery.
- Report file activation, local checks and new-process real-request verification separately.

## Handoff

Provide entrypoints, first-use/resume/recovery instructions, field ownership, bounded retention, source revision and concise changes, stage timings, test results and remaining risks. Exclude private state from source control. Pending restart, login or real-request verification needs an explicit next step. Promise only the environment and scope actually verified, not eternal lossless compatibility across all builds.
