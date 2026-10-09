# Validation and evidence limits

[简体中文](validation.md)

Validate the selected capabilities; do not present a suggested checklist as already tested. This repository ships no switcher. The evidence below is separate from acceptance criteria for a future implementation.

## Evidence behind this revision

Environment: Windows, native Codex CLI 0.159.2; local scripts supporting PowerShell 7 and Windows PowerShell 5.1. Recorded on 2026-10-01, not a pass for future versions or other operating systems.

| Check | Observed evidence | Limit |
| --- | --- | --- |
| Content after a real switch | Manifest/backups checked: 80 ID renames, zero removals; untouched lines byte-identical, changed lines differ only in the designated ID; database integrity passed | Proves this recorded mutation, not all history on every endpoint |
| Pagination and continuation | Native client read old UI history from isolated copies and indexed appended synthetic events, including inherited history | No credentials or model requests; not official continuation acceptance |
| Rejection and rollback | Synthetic cases cover wrong segment, cursor, event source, inheritance boundary, tool pairing and reversal of applied changes | No claim that every power/hardware failure was injected |
| Bidirectional switching | Temporary homes and fake login exercise one-action initialization, required preparation and official/API transactions; configuration-preservation checks passed | Fake login cannot validate token lifetime or provider permissions |
| Chinese and shell compatibility | Both PowerShell generations passed Chinese output, proxy switching, history and decoder tests | Not a tested three-platform app |
| Performance | The same read-only projection-evidence check fell from 133.53 to 11.85 seconds while retaining the same rejection result; a separate full scan took about 8.46 seconds | Component benchmark, not total switching time or proof that this thread passed the repair gate |
| Fast readiness | Unrelated logs do not invalidate preparation; history tables under unfamiliar filenames still count; rule-hash changes invalidate stale readiness | Metadata fingerprinting is not tamper-proof content validation |
| Unreplayable reasoning items | A read-only scan of 405 local history files found 7 legal `rs_` items across 2 paginated files with no replayable content; an isolated copy preserved 7 UI items and indexed an appended event | Evidence is for this local layout/client copy; production repair still needs the shutdown gate and separate acceptance |

A recorded real transaction took about 29 seconds for backup, mutation and recheck, excluding scanning/planning. That does not contradict several minutes observed by the user. Retest the same component and never create speed by turning a rejection into acceptance.

Private local tests/data are not distributed here. The reusable material is the reasoning, boundaries and test design below, not a certificate for someone else's deployment.

## Minimum implementation acceptance

| Scenario | Required evidence |
| --- | --- |
| Config preservation | Synthetic plugins, MCP, skills, hooks, permissions, projects, comments and unknown keys survive; only owned fields change, including settings added between switches |
| Model/reasoning level | Exact pair supported without silent downgrade; unowned settings remain unchanged |
| Missing credentials | Official-only, API-only, neither and incomplete setup have a next step; cancellation preserves the valid source |
| Auth failure | Local-kind checks, real requests and token refresh tested separately; failures never marked ready |
| Damaged config | Empty/invalid/template-only config, missing fields and concurrent edits recognized; known-good and no-backup recovery exercised |
| One-action flow | Uninitialized, valid readiness, stale readiness and failed preparation converge; history failure precedes auth activation |
| Logs/capacity | Redacted errors, stage timing and bounded retention; stop before sacrificing the only recovery material |

## History fixtures

Cover the supported layouts' relevant boundaries:

- active/archive roots, both provider fields, multiple WAL databases and excluded cloud rows;
- shorter, longer and equal-width providers; insufficient paginated space rejected;
- valid, generic and overlong IDs, target protocol length boundaries, collisions and unknown types;
- protected reasoning, independent visible events and tool call/result pairing;
- legal-prefix reasoning with only an ID/blank summary, older segments without a model projection row, and refusal when a turn references the item;
- direct model projections versus event projections, logical IDs versus storage segment IDs;
- nonzero inherited baselines, missing segments, invalid ordinals/byte cursors and incomplete indexing;
- appended events after repair, reopening, repeated rollback and newer activity;
- changed rules, related database changes, unrelated log changes and damaged readiness records.

Accept old-content visibility, model continuation and new-message indexing separately. Native offline copy tests cover visibility/indexing only; real model requests need their own result, not “scanner found zero.”

## Failure and upgrades

Inject risks relevant to the implementation: concurrent switching, locked files, denied writes, full disk, unreadable snapshots, interrupted writes, rollback failure and intervening user config edits. Outcomes should be restored source, verified target, pending restart/login, or a clearly recoverable unknown state, never vague partial success.

After Codex updates, recheck config, auth, history layout and transport. Preserve data and disable unverified history mutation until adapted; do not manually increase readiness version numbers. Upgrade detection can be cheap; expensive probes should run for a reason, not on every invocation.

## Repository-check limits

Run python scripts/validate_pack.py for required files, relative links, bilingual reference coverage and limited secret patterns. Skill quick validation checks entrypoint format only. Neither executes OAuth, a state machine, SQLite transactions, model requests or Windows fault injection, nor proves translation equivalence. Publication still needs human review of logic, evidence and privacy.
