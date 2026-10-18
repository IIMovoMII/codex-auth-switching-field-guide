# Validation and evidence limits

[简体中文](validation.md)

Validate the selected capabilities; do not present a suggested checklist as already tested. This repository ships no switcher. The evidence below is separate from acceptance criteria for a future implementation.

## Earlier field evidence

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

## Evidence added on 2026-10-12

Environment: Windows, Desktop's native runtime `0.162.0-alpha.17.2`. See the [continuation case study](continuation-case-study.en.md) for reproduction and verified write scope.

| Check | Observed evidence | Limit |
| --- | --- | --- |
| Actual official continuation | Production repair code processed an isolated failing copy; real official WebSocket warmup and continuation with `previous_response_id` succeeded while preserving content, encrypted reasoning and compaction | Fresh-request success does not establish this path; only relevant types and paginated layouts were verified, not permission to clear IDs for every service |
| Full-copy repair and rollback | 415 files and 3 related databases; 392 files and 243,163 model records passed line-by-line field checks, database hashes remained unchanged, and every file rolled back exactly | Copy tests contained no real auth and made no production changes; request validation was separate |
| Boundary layouts | Empty projection, materialized fork with copied parent inheritance metadata, and a segment damaged by an older repair passed native-copy reading and append indexing; wrong provenance and changed backups still refused | Does not establish safety for arbitrary empty tables or mixed metadata |
| Stopped-writer production run | 392 files applied; optional IDs cleared in 243,244 model records, one unreplayable reasoning item replaced in its byte slot, and zero database writes. After reopening, all repaired-prefix hashes matched, critical files passed content/byte-boundary checks, and three databases passed integrity checks | The current chat continued, compacted and indexed new messages; the original failing task was reloaded but not individually exercised with a new real task. Not acceptance for every old conversation |
| Scale and timing | Roughly 2.5 GB copy: scanning 38.2 s, projection checks 109.5 s, backup/mutation/recheck 165.6 s; full copy/comparison/rollback exercise about 359 s | Not routine-switch timing or a cross-machine performance guarantee |
| Interruption review | Unified history startup recovery was identified as a gap at that time; see the subsequent revision below | This row does not accept the later recovery implementation or prove actual forced-termination/power-loss recovery |

## Incremental revision evidence from 2026-10-14

These are implementation/tests of the private local program, not a switcher shipped in this repository. Earlier verified history rules remain; see [incremental preparation](incremental-preparation.en.md) for the added route.

| Check | Observed evidence | Limit |
| --- | --- | --- |
| Complete real-history copy | 349 files, roughly 3.8 GB and 3 related databases; 384 model records across 2 files processed with line-by-line preservation checks for content, tools, UI and encrypted fields; database hashes unchanged; all 349 files and databases rolled back exactly | WAL-aware snapshots; active files copied through captured projection cursors. No real auth/config copied, model calls or production writes. Temporary copy cleaned |
| Initial baseline | Scan 67.5 s, projection proof 3.1 s, backup/repair/recheck about 3.0 s; roughly 74 s preparation | Initial preparation remains slow, not a fixed-seconds promise |
| Unchanged preparation | About 1.83 s; 349 files skipped, zero parsed bytes | File/database inspection remains, not zero disk activity |
| Two append rounds | Preparation 4.65/4.60 s; each skipped 348 files, parsed 234 bytes, hashed roughly 23.4 MB of old prefix and used fixed slots with no database writes | Synthetic appends to a real-history copy, not production-switch totals or only 234 bytes read |
| Cache/dependencies | PS 7/5.1 cover new files, append, legacy fallback, rewrite/truncation/replacement/archive moves, damaged cache, related-schema changes and database-only provider drift. Incremental/full findings match locations and actions | Tested layouts, not all future formats |
| Pagination/encoding | Changed old UI evidence forces complete source checking and refuses wrong provenance; Chinese, emoji, UTF-8 BOM, CRLF and invalid-ordinal rejection passed | Conditional old-source reuse on PS 7; PS 5.1 retains complete checks, with different timing |
| Small backups/recovery | Exact rollback, wrong-identity refusal, refusal after append, partial slot writes, torn bytes and re-entry with a pending marker passed | Simulated interruption, not actual forced termination/power loss or every legacy transaction format |
| One-action integration | Temporary profiles/fake login cover preparation after append, forced full checking despite valid readiness, no direct acceptance of corrupt cache, and warning-only failure of an optional locked timing report. Earlier history, projection, bidirectional switch, config-preservation and both-shell regressions passed | This revision has not performed a real production account switch for the user; requests, OAuth refresh and reopened acceptance remain separate |
| Context policy | Temporary two-model catalog/cache tests retain the user's 272000 in official/relay directions without changing model names/effort; 8 live-config-preservation checks passed | File/integration evidence, not runtime acceptance of every reopened old task; 272000 is not a universal recommendation |

The complete copy/check/comparison/rollback exercise took about 107.1 s, distinct from preparation or total real switching. An early benchmark placed a database backup inside active database discovery and correctly triggered global invalidation. The test moved the backup outside discovery instead of weakening the gate. Test layout must not create false application changes.

## Minimum implementation acceptance

| Scenario | Required evidence |
| --- | --- |
| Config preservation | Synthetic plugins, MCP, skills, hooks, permissions, projects, comments and unknown keys survive; only owned fields change, including settings added between switches |
| Model/reasoning level | Exact pair supported without silent downgrade; unowned settings remain unchanged |
| Context policy, if selected | Honor the user rather than hard-coding the author's cap. Check all managed models/catalogs/caches across both directions and repeated switches, preserving unowned fields. Inspect new/old tasks in a new process; distinguish cap, occupancy and compaction threshold, and test these files' own write-failure recovery |
| Missing credentials | Official-only, API-only, neither and incomplete setup have a next step; cancellation preserves the valid source |
| Auth failure | Local-kind checks, real requests and token refresh tested separately; failures never marked ready |
| Damaged config | Empty/invalid/template-only config, missing fields and concurrent edits recognized; known-good and no-backup recovery exercised |
| One-action flow | Uninitialized, valid readiness, stale readiness and failed preparation converge; history failure precedes auth activation |
| Incremental/complete routes | Findings match locations, actions and rejection decisions on one snapshot, not counts alone. Explicit complete checks bypass readiness shortcuts; corrupt caches rebuild or stop; read-only scanning cannot issue readiness |
| Logs/capacity | Redacted errors, stage timing and bounded retention; stop before sacrificing the only recovery material |
| Version update | Reuse the implementation when relevant behavior remains verified-compatible; reject unchanged-schema cases whose read semantics changed; uncertain compatibility gates dependent writes and switching |
| Multiple official accounts | Validate old-task visibility, opening, model continuation and new-message indexing per account; account A's success cannot stand in for account B |

## History fixtures

Cover the supported layouts' relevant boundaries:

- active/archive roots, both provider fields, multiple WAL databases and excluded cloud rows;
- shorter, longer and equal-width providers; insufficient paginated space rejected;
- valid, generic and overlong IDs, target protocol length boundaries, collisions and unknown types;
- protected reasoning, independent visible events and tool call/result pairing;
- legal-prefix reasoning with only an ID/blank summary, older segments without a model projection row, and refusal when a turn references the item;
- legal IDs with complete encrypted content failing after native warmup; repair changes only designated old model IDs, preserving tool pairing, guardian history, UI IDs and newly generated IDs;
- direct model projections versus event projections, logical IDs versus storage segment IDs;
- empty projections versus dangling references, materialized forks with copied parent metadata, proven backup/manifest layout recovery and refusal when evidence is insufficient;
- nonzero inherited baselines, missing segments, invalid ordinals/byte cursors and incomplete indexing;
- appended events after repair, reopening, repeated rollback and newer activity;
- changed rules, related database changes, unrelated log changes and damaged readiness records.

Accept old-content visibility, model continuation and new-message indexing separately. Native offline copy tests cover visibility/indexing only; real model requests need their own result, not “scanner found zero.”

## Failure and upgrades

Inject risks relevant to the implementation: concurrent switching, locked files, denied writes, full disk, unreadable snapshots, interrupted writes, rollback failure and intervening user config edits. Outcomes should be restored source, verified target, pending restart/login, or a clearly recoverable unknown state, never vague partial success.

Interrupt after file replacement but before the manifest update, and after some files are applied but before database work. Re-enter and verify reconciliation precedes any new transaction. Manual rollback and caught-exception tests do not establish this capability. Record simulated partial writes, actual process termination and power loss separately. Do not claim forced-termination recovery without testing it; storage-hardware failures retain separate limits.

After Codex updates, recheck config, auth, history layout and transport. Preserve data and disable unverified history mutation until adapted; do not manually increase readiness version numbers. Upgrade detection can be cheap; expensive probes should run for a reason, not on every invocation.

Component tests cover coordination/recovery and version-dependent config/auth/history/transport separately. Retain one-action integration tests proving that every required preparation failure prevents target activation. Module boundaries do not replace end-to-end validation.

If caching is implemented, test that unchanged history, unrelated logs and menu edits avoid complete preparation, while relevant behavior/rule changes invalidate it. Truncation, rewrites, moves, archives and parent-segment/database changes invalidate dependent results. Beyond result comparisons, test modified old prefixes despite growth, partial-line appends, new metadata, changed old UI rows and replaced caches. Report parsed and prefix-hashed bytes separately, not parsed bytes as all disk reads. Untested target cases/performance remain pending acceptance.

## Repository-check limits

Run python scripts/validate_pack.py for required files, relative links, bilingual reference coverage and limited secret patterns. Skill quick validation checks entrypoint format only. Neither executes OAuth, a state machine, SQLite transactions, model requests or Windows fault injection, nor proves translation equivalence. Publication still needs human review of logic, evidence and privacy.
