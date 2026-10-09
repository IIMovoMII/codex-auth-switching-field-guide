# History compatibility: preserve content without fabricating protocol state

[简体中文](history-compatibility.md)

## Define preservation first

Local history serves three roles: visible conversation, future model input, and indexes for opening/paging/searching. They may come from different records. A successful model request alone is insufficient.

Preserve messages, tool results, attachment references, project placement, original task identity and visible history. Protected reasoning that cannot cross endpoints may no longer be usable as model input. Disclose this context loss instead of claiming the model remembers everything. Validate on copies, confirm the accepted scope, then handle production history.

## Inventory scope

Inspect active and archived JSONL, session metadata, repeated thread settings, model response_item records, independent UI events, and all related SQLite databases and WAL files. Discover relevant databases by schema, not one fixed filename.

Known locations to verify for shared provider identity:

- session_meta.payload.model_provider;
- thread_settings.model_provider_id in event_msg of type thread_settings_applied;
- SQLite threads.model_provider for proven local tasks.

Confirm paths on the installed build. Scope database rows to verified local IDs. Exclude cloud Chat/Work and rows without corresponding rollouts. Never replace arbitrary matching strings or assume the first metadata line is sufficient.

Prove both routes and new tasks work before adopting shared model_provider = "openai". Provider normalization and response-item compatibility require separate counts and acceptance; the former cannot repair the latter's 400 responses.

## Response-item decisions

Check semantic type, prefix, length, required fields and references, not just item_:

| Finding | Action |
| --- | --- |
| Already valid for the target protocol | Leave unchanged |
| Incompatible ordinary message/tool item ID | Map only with verified type/references, collision checks and tested rules |
| rs_ prefix but excessive length | Still invalid; a valid prefix is insufficient |
| Reasoning has a valid ID but no `content` or `encrypted_content` (including a blank/zero-width summary) | It is still not replayable; the official endpoint may treat it as a persisted-item lookup. Remove only the model-input copy after UI provenance is verified and no turn references it |
| Missing protected reasoning content | Renaming cannot make it valid; disclose the effect and remove only a proven model-input copy |
| Unverifiable encrypted reasoning, unknown type or unclear references | Stop and investigate; do not truncate IDs or invent fields |

One observed incident had 79-character reasoning IDs. The old prefix-only scanner missed them; tests were added for a 64-character limit on that target protocol. Bind limits to version/protocol evidence rather than every endpoint forever. Never manually bump an old readiness record to bypass new rules.

A later review found that a legal `rs_` prefix is not enough: a relay may store only an ID and a blank summary, with no replayable body. The official endpoint can then return an error saying that a persisted-item lookup is required but unsupported. Scan content presence as well as prefix and length; neither prefix nor length alone proves compatibility.

Response-item IDs, call_id and tool-result relationships are distinct. Preserve call/result pairing, inspect parent-response and UI references, and detect collisions. Provider-side stored response state may also be nonportable; verify the client's actual replay path instead of bulk-replacing strings.

## Paginated history: the fragile layer

A validated case uses thread_history_1.sqlite; filenames, tables and fields remain version-specific implementation details. Before editing, establish:

1. JSONL ordinals, byte offsets, encoding and line endings; inherited history may start a segment above ordinal zero.
2. Alignment of next_rollout_byte_offset and next_rollout_ordinal with the current segment.
3. Correspondence among logical task ID, physical segment ID and history_base.
4. Provenance of thread_items, references in thread_turns and inherited history.

Continuation filenames may resemble “timestamp-logicalID_segmentID”: metadata and events retain the logical ID, while SQLite uses the segment ID. Do not validate a continuation against the original segment's cursor or trust a suffix alone. Cross-check metadata, filename and inheritance boundary. Stop for missing segments or inconsistent evidence.

### Two validated projection paths

- **Projection directly from model records:** coordinate database rows and turn references while preserving visible content. Removing the sole visible copy or leaving references cannot be treated as automatically safe.
- **Projection from independent UI events:** prove each row's event source, logical task, turn, ID, type and ordinal. A model response_item may arrive later, so the two ordinals need not match. Repair the model copy and prove UI rows, turns, inheritance and cursors remain unchanged.

An older segment may have an independent visible Reasoning event but no `thread_items` row for the adjacent model `response_item`. Allow a model-only removal only after all remaining UI provenance is verified and `thread_turns` has no reference to that model ID; otherwise refuse.

For unusable model input, one copy-tested approach uses a client-ignored non-model event at the original position, preserving byte length and ordinal. This placeholder format is not universal. The installed native client must prove old-content visibility and indexing of appended events.

Never delete JSONL lines and create ordinal gaps. Equal character counts do not imply equal UTF-8 byte lengths; replacements must fit and preserve line endings. A provider shorter than openai may not fit: stop instead of shifting later offsets. Reordering requires a verified native rebuild of the segment, inherited baseline and new-event projection. Without that path, retain the gate.

## Formal transaction

Default to stopped Desktop, CLI and other state writers:

1. Lock repair, fix the target scope and establish format/recoverability.
2. Back up necessary JSONL content and hashes; use SQLite's own backup facilities to include WAL state.
3. Persist the plan, before/after values, file identity and rollback material before applying.
4. Structurally rewrite ordinary history when safe; preserve positions in paginated history. Use explicit row-scoped transactions per database.
5. Validate JSON, byte/ordinal boundaries, tool pairing, provenance, untouched content and database integrity.
6. Run final compatibility checks and save readiness bound to the repair rules.

Files and databases are not one atomic transaction. See [safety and rollback](safety-and-rollback.en.md) for exceptions and crash recovery. A live single-task rescue does not authorize bulk migration; cached settings can write old provider values again.

## One-action switching and performance

Internally separate read-only scanning, stopped-writer preparation, manifest-scoped rollback and auth activation. The UI may chain them into one action. Failed preparation must not activate target auth. Unknown-layout rejection is not a nuisance to “self-heal” away.

Bind readiness to:

- local scope, paths, sizes, mtimes and available stable identities;
- related databases and WAL, excluding the SHM coordination cache that read-only access can change;
- target provider/protocol and repair-rule version or hash;
- validated client/history-layout version and preparation manifest.

Metadata fingerprints detect normal changes, not adversarial tampering. Add content hashes when stronger assurance is required. Exclude unrelated logs by schema; unfamiliar filenames with history tables still count. Genuine history changes must invalidate readiness.

Measure scanning, projection proof, backup/mutation/recheck and credential activation separately. Timing only the write phase is not total switching time. In one investigation, PowerShell per-byte text decoding dominated; equivalent compiled decoding reduced it substantially without removing checks.

“Only the first switch is slow” is false: new relay records, databases, rules or client changes can require preparation. Invalidate outdated zero-finding results when rules change.

## Completion criteria

Zero scan findings are only one condition. Also verify:

- no unintended content or unowned-field changes; manifest counts reconcile and fixture rollback works;
- new tasks record the shared provider and representative old tasks remain in their projects with visible content;
- the model actually continues in the target mode;
- appended messages are indexed natively and survive reopening;
- remaining auth, network, protected-context or version uncertainties are reported.
