# Incremental preparation: faster checks without narrowing compatibility scope

[简体中文](incremental-preparation.md)

Local implementation evidence from 2026-10-14, documented on 2026-10-18. This is an optional implementation route, not an executable migration program. First understand the semantic, pagination and inheritance boundaries in [history compatibility](history-compatibility.en.md). Small histories may be better served by simpler complete checks.

## Two levels of evidence

Final readiness binds the current history inventory, related databases, target protocol, repair rules and check cache. Further chat activity expires that conclusion, without necessarily requiring every old file to be parsed again.

Per-file evidence records a verified clean range: path and stable identity, length/mtime, complete-prefix hash, complete-line boundary, last ordinal, ownership, layout/rule fingerprints and applicable UI-provenance evidence. Version and integrity-check the cache. Missing fields or failed checks cannot mean empty history or successful preparation.

Local final readiness remains version 3 and additionally binds the cache hash; the per-file cache has its own version. These are local formats, not prescribed version numbers for other implementations. Never manually upgrade an old readiness record.

## Route changes within one preparation

| Change | Verified route |
| --- | --- |
| Clean file identity, size, timestamp and applicable rules unchanged | Reuse its result without reparsing the body |
| A verified paginated file grew | Hash the entire old prefix; parse the append only if old/new tails end on complete lines and no new session metadata appears |
| New file, prefix mismatch, rewrite/truncation/replacement, move/archive or new metadata | Completely recheck the affected file and dependencies; movement alone is not corruption |
| Changed legacy nonpaginated format | Retain complete checking; its semantics may depend on earlier records |
| Damaged cache, changed relevant rules or history schema | Discard old certificates and rebuild a complete baseline; stop if compatibility remains unknown |
| Database-only change | Recheck relevant providers, UI provenance, turns, cursors and inheritance dependencies despite unchanged JSONL |

This is change detection, not a universal semantic allowlist. Parent-segment, inherited-baseline or related-row changes invalidate dependent conclusions. Growth, a few sampled hashes or a previously clean cache alone cannot establish append-only behavior.

**Parsing only appended lines is not reading only appended bytes.** The local append path still reads the entire old prefix for hashing. Pre-write/recovery checks can read the whole file. Unchanged-file identity/size/time detect ordinary changes, not malicious edits preserving metadata.

## Body caches cannot replace UI-index validation

Database UI rows can change while the transcript prefix remains unchanged. The local PowerShell 7 path reuses old source evidence only when fingerprints of the relevant old projection fields, turns and related state match, then verifies new sources. Otherwise it fully rechecks the affected file. PowerShell 5.1 retains complete UI-source checks, so timing can differ.

SQLite provider rows are still read live, and schema discovery cannot rely on one filename. Schema changes may invalidate all file certificates; content changes require relevant rechecks. Final readiness also binds database/WAL state. Database-query costs must not disappear behind an “only a few lines” claim.

## Small edits can use small backups within a narrow boundary

The local fixed-byte-slot path applies only to appended records in a verified paginated file when every action clears a proven-optional old model-input ID:

1. Record exact offsets, before/after bytes, file identity/length and original/expected hashes. Durably save slot data, checksums and the manifest before mutation.
2. Recheck identity and normalized whole-file hashes on the same exclusively held handle, write `null` plus padding spaces, then flush to storage.
3. Verify actual output, semantics and unchanged projections before saving renewed certificates/readiness.

Normalized hashes virtually substitute recorded original/target slot bytes while checking the entire file, not just edited locations. Recovery can accept verified partial application composed of old/new bytes inside slots. Unrelated changes, later appends, length changes or file replacement must refuse overwrite.

Only proven-optional old model IDs at `response_item.payload.id` and `compacted.payload.replacement_history[*].id` qualify. Preserve content, tools, `call_id`, encrypted data, UI events, guardian records and current-turn IDs. Initial complete preparation, provider migration, unreplayable-reasoning placeholders and layout recovery retain their separately verified full-backup paths. Small backups are not universally safe for every repair.

## Reconcile unfinished work before a new preparation

Persist a pending-transaction marker before writing and reject final readiness while it exists. The next stopped-writer preparation reads its manifest, verifies and reverses known unfinished changes, then prepares again. Never create a new plan over old evidence. Slot recovery and SQLite transactions are separate; multiple files are not one atomic transaction.

Missing material, failed checksums, out-of-scope paths or later changes retain evidence and require explicit manual recovery. See [safety and rollback](safety-and-rollback.en.md). Local tests simulate partial application, torn slots and re-entry with durable markers; they do not certify actual power loss, every forced-termination point or every legacy format.

## Keep complete checks, useful timing and a small footprint

- Retain one routine action, an explicit forced-complete check and read-only scanning. Valid readiness must not short-circuit an explicit full-check request.
- Unchanged checks create no history backup. Overwrite one cache, latest failure summary and latest timing report. Bound actual recovery retention without deleting an unfinished transaction's only evidence.
- Report skipped/tail/full file counts, parsed bytes, prefix-hashed bytes, projection checks, backup/mutation and auth phases. Total time includes first-login waiting. Optional timing-log failure warns rather than misreporting an already-completed credential switch as failed; mandatory journals must persist reliably.
- A latest-failure summary can describe an older run, not live health. Inspect its time, this run's stage and the actual current mode; a stale error file must not automatically trigger history repair.
- No resident scanner is needed. Separate rules, cache and coordination. Keep local source versions and concise changes; exclude credentials, configuration, transcripts, databases, backups and runtime output from source Git.

A roughly 3.8 GB/349-file copy took about 74 s for initial preparation and 1.83 s unchanged. Two synthetic-append rounds each parsed 234 bytes, skipped 348 old files and took 4.65/4.60 s, while still hashing roughly 23.4 MB of old prefix each round. These are not total account-switch timings. See [validation](validation.en.md) for field comparisons, unchanged databases, exact rollback and untested boundaries.
