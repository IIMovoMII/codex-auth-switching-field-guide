# Continuation case study: why an official request failed after a clean scan

[简体中文](continuation-case-study.md)

Recorded on 2026-10-13; experiments and the stopped-writer run took place on 2026-10-12. Environment: Windows and Desktop's native runtime `0.162.0-alpha.17.2`. This redacted account includes no local repair program, real transcripts, credentials or backups.

## One error, two gaps

Old-thread continuation and context compaction after switching to official mode returned:

~~~text
Supplied input item IDs require persisted-item lookup that is not supported by rustresponsesapi.
~~~

The scanner already checked generic prefixes, overlong IDs and reasoning without replayable content, yet reported zero findings. Two independent gaps emerged: **nonportable old IDs on the actual continuation path**, and **a pagination segment shortened by an earlier repair**. The transcript was not universally corrupt, and missing encrypted reasoning was not an adequate explanation for this incident.

## Reproduce Desktop's actual request path

The same failing history produced these comparisons:

| Request path | Observation |
| --- | --- |
| Fresh official HTTP request | Succeeded, without establishing Desktop continuation |
| Fresh official WebSocket request | Succeeded, also not the actual failing path |
| Native warmup followed by `previous_response_id` continuation with old history | Required unsupported lookup despite legal IDs and preserved encrypted content |
| Production code cleared proven-optional old model-input IDs, followed by the same warmup/continuation | Succeeded with content, tool pairing, encrypted reasoning and compaction preserved; current-turn IDs remained native-managed |

A comparison clearing ordinary message/tool IDs but retaining other old model IDs also failed. Fixing only the first reported item type was insufficient.

The [official conversation-state guide](https://developers.openai.com/api/docs/guides/conversation-state) distinguishes response references from full-history replay and describes response references in WebSocket continuation. The [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning) explains protected-reasoning replay. These are conceptual sources, not official authorization for the local file patch or a cross-version guarantee.

## Verified write boundary

The local paginated format handled only old, natively recognized model items allowing a null ID at `response_item.payload.id` and `compacted.payload.replacement_history[*].id`. Strings became `null`, with spaces retaining their original byte slots. Line count, UTF-8 boundaries, ordinals and line endings remained intact.

Messages, tool arguments/results, `call_id`, call/result pairing, encrypted reasoning/compaction, independent UI events, guardian history and provenance metadata were preserved. Unreplayable reasoning separately used a verified equal-byte placeholder; this is not permission to delete all reasoning. Legacy nonpaginated files did not receive this new rule.

Changing only model IDs does not prove every client will accept the result. Required IDs, unknown types, affected references and unverifiable layouts require a stop. Do not clear UI IDs, change current-turn response IDs or assume identical error wording proves an identical cause.

## Offset mismatch left by an older repair

One old segment was shorter than its database cursor expected. The original backup and prior manifest proved that an early script deleted a reasoning line and shortened an ID, leaving gaps in byte positions and ordinals.

Recovery requires all of: the current file exactly matching the old transaction output, verified original-backup hash/length, fully explained line differences, original database boundaries and current semantic checks. Construct a new copy from the proven original layout, back up this operation's starting state, and preserve unusable items' positions with a verified equal-byte non-model placeholder. Stop after later appends or missing evidence; do not guess padding, renumber from current line numbers or unconditionally restore an older backup.

Empty UI projections and materialized forks containing copied parent inheritance metadata were also validated. Neither is universally corrupt or writable. Check ownership, cursors, turn references and a complete compacted baseline, then prove native reading and append indexing on copies.

## Separate validation layers

- **Real-request copy:** the failing copy processed by production code passed official warmup and continuation, with tool execution disabled and no message sent to the original task.
- **Complete offline copy:** 415 files and 3 related databases. After 392 file repairs, line-by-line checks preserved content, tools, encrypted fields and UI records; database hashes were unchanged and all files rolled back exactly. Copies contained no real auth and were cleaned afterward.
- **Stopped-writer run and reopening:** the user exited all writers before running it. All 392 repaired-prefix hashes matched, critical files preserved content/byte boundaries, and three databases passed integrity checks. The current chat continued, compacted and indexed new messages.
- **Not covered:** real-model acceptance for every old task, account, supplier or platform; direct application of this rule to legacy layouts; automatic recovery after forced termination or power loss during history repair.

Preparation on a roughly 2.5 GB copy took about 313 seconds; the complete copy/comparison/rollback exercise took about 359 seconds. Batch parsing/writing and fewer repeated database queries improved performance without changing safety decisions. First bulk preparation and exercise totals are not routine-switch speed claims; temporary test copies and required user recovery material are different classes of files.

## Lessons for future implementations

Keep failed-preparation-before-switch behavior, and extend it to startup after interrupted history work: detect unfinished or rollback-failed manifests, reconcile original/applied/unknown states, and decide recovery before new work. Stop when reconciliation is unsafe. Caught exceptions and config recovery do not prove history power-loss recovery. This remains a local hardening gap; this update records the experience without implementing that capability.

Retain one-action entrypoints and a few clear modules rather than building a general Codex repair suite. Separate verified rules, the production writer and one-off rescue material. Unknown cases stop; timeouts, 503 responses and model capacity must not automatically trigger history cleanup.

Read [history compatibility](history-compatibility.en.md), [safety and rollback](safety-and-rollback.en.md) and [validation](validation.en.md), then adapt to the local machine. This case is not a directly executable migration command.
