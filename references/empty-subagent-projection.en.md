# Empty subagent projection: do not reject a proven interrupted terminal state

[简体中文](empty-subagent-projection.md)

Recorded on 2026-10-23. This is a redacted implementation lesson; it contains no local task IDs, transcript text, credentials or directly runnable repair program.

## Symptom

History preparation stopped before switching with:

~~~text
模型编号与界面索引未证实独立，拒绝清除
~~~

The refusal is normally protective: a model `response_item` ID must not be cleared from JSONL merely because it looks optional. First prove that the UI index comes from independent events and that no turn reference would become dangling. One real record showed another valid layout: a native subagent can be interrupted before producing its first UI item, so there is no UI row to prove. A strict checker then misclassified a normal layout as unknown.

## Root cause

The old rule accepted only one empty-projection terminal state: a failed turn ending with `task_complete`. The real native layout had all of these properties:

- `session_meta` identified a paginated subagent, with matching parent thread, agent path and recipient;
- `thread_items` was empty for that thread, and `thread_turns` had no first-user or final-agent item reference;
- the turn status was `interrupted`, ending with `turn_aborted` whose reason was `interrupted`;
- JSONL ordinals were contiguous from zero, and task-start offset, file end and SQLite cursor agreed exactly;
- after system/developer/user inputs and the inter-agent message, there was no assistant output, unknown event or tool pairing to modify.

This is not permission to treat every empty table as safe. It is a special layout with complete terminal evidence but no UI projection. `failed + task_complete(error)` and `interrupted + turn_aborted(reason=interrupted)` are separate terminal states and each requires field-by-field proof; do not replace the check with “anything that is not in progress.”

## Safe write boundary

Only when every piece of evidence matches may an implementation reuse a rule already validated on a copy of the installed client and clear proven-optional old IDs in model input fixed slots. The repair must:

- preserve messages, tool relationships, `call_id`, encrypted content, ordinals, line count and byte boundaries;
- never delete or rewrite UI events, fabricate UI items, or write `thread_items`/`thread_turns`;
- never change current-turn IDs, parent-thread relations or pagination cursors;
- persist recoverable evidence first and undo only the equal-width changes in this operation if it fails;
- stop on any state, reason, parent, recipient or cursor mismatch instead of bypassing the gate.

If UI rows, turn references, assistant output, unknown events or an unfinished state exist, this lesson does not apply. Return to ordinary event-provenance verification.

## Validation

Start with a credential-free copy. Positive and negative fixtures should cover `failed`, `interrupted`, a wrong interruption reason, wrong turn/root, non-subagents, existing UI rows, CRLF, incremental append and exact rollback. Then use a redacted copy of one real record to check fields, byte boundaries, unchanged database state and rollback. Only after that should the stopped-writer production run happen, with separate acceptance for old visibility, model continuation and new-message indexing.

This implementation added 23 positive/negative PowerShell 7/5.1 cases and exercised a temporary copy of 79 history files with 3 related databases. Those numbers describe that layout's evidence, not a guarantee for future Codex versions.

## Guidance for implementers

Keep “failed preparation means no switch” as the safety rule. The correct change is to add a proven terminal state, not to remove the refusal for unverified UI provenance. Keep terminal classification, event-source proof, model-input cleanup and auth activation separate; unknown layouts still stop before target credentials are activated.
