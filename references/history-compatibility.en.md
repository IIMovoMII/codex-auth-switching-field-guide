# History compatibility

Local conversation history is an API input cache, a UI record and an index at the same time. Repair must preserve all three roles.

## Why a route switch can expose old defects

An API-compatible provider may return response items with identifiers or payload shapes that its own server accepts later. An official endpoint can apply stricter type-specific rules when the old conversation is resumed.

A representative failure is a generic item identifier appearing where the target endpoint expects a reasoning-specific identifier. The important point is not one prefix: the repair decision depends on the semantic record type and the target version's protocol.

## Storage layers to inspect

Depending on the Codex build, history can include:

- append-only JSONL rollout files;
- active and archived session roots;
- first-line session metadata;
- repeated thread-settings events;
- response items that are later sent back to the model;
- UI-only events;
- SQLite thread indexes;
- SQLite WAL and shared-memory files;
- cloud-backed Chat or Work conversations that are not equivalent to local rollouts.

Do not assume changing one metadata line updates every copy of a provider identity.

## Classify before changing

For every suspicious record, identify:

- JSONL record type;
- response-item semantic type;
- whether it is included in future model input;
- whether it contains protected or encrypted reasoning material;
- whether a tool call or tool result points to it;
- whether the same identity appears in SQLite;
- whether the file is still changing.

A generic identifier on a user or assistant message does not justify the same transformation as a generic identifier on a reasoning item.

## Reasoning records

Reasoning items can have stronger invariants than ordinary messages. If the target endpoint requires protected content that is absent, simply renaming the identifier may create a record that looks valid but cannot be verified.

Safer decision order:

1. retain a record unchanged when it is already valid;
2. use an exact, version-proven type conversion only when all required fields are present;
3. remove only the model-input copy when the reasoning payload is unrecoverable;
4. preserve UI-visible messages and independent event history;
5. never synthesize protected reasoning or pretend an unverifiable item is authentic.

The goal is resumability without falsifying protocol state.

## Tool relationships

Before removing or rewriting any item, construct a relationship graph for:

- tool call IDs;
- tool result call IDs;
- response-item IDs;
- parent or previous-response references;
- UI event references.

Every retained tool result must still have a retained call. Every retained call that requires a result should remain coherent. A repair that fixes one identifier error but breaks call pairing is not successful.

## Provider metadata

If provider metadata affects session visibility, update every semantically equivalent location discovered for that Codex version. Typical locations include session metadata, thread-settings events and thread-index rows.

Prefer one stable provider identity across official and API routes only after proving that:

- new sessions record it;
- old sessions remain discoverable;
- the live configuration can still express the route difference;
- both endpoints accept the resulting request behavior.

This is a version-specific design choice, not a universal constant.

## Normalize local provider metadata to `openai`

For the architecture in this guide, `openai` is the preferred common identity for official and API-compatible routes. Apply this rule only after the installed Codex build proves all of the following:

- official mode works with `model_provider = "openai"` and no `openai_base_url`;
- API-compatible mode works with the same provider identity plus a top-level `openai_base_url` override;
- a new session in each mode records `openai` and remains discoverable;
- representative old sessions can be resumed after a fixture normalization.

Do not create a `[model_providers.openai]` table. `openai` is a reserved built-in identity. If either route cannot satisfy this contract, stop and retain version-specific provider identities instead of forcing history to match a theory.

### Read-only inventory

Before mutation, scan active and archived local history and group provider values by semantic location and thread identity. Known locations to verify in applicable builds include:

- JSONL `session_meta.payload.model_provider`;
- JSONL `event_msg.payload.thread_settings.model_provider_id` for `thread_settings_applied` events;
- provider columns on the corresponding rows in every relevant SQLite thread index, such as `threads.model_provider`.

These names are observations to confirm, not a permanent schema. Search structurally, report value counts without titles or messages, and discover every active database rather than editing only the first file found. Keep cloud-backed ChatGPT Work/Chat sessions outside the local rollout mutation scope.

### Stopped-writer normalization

After explicit user approval:

1. fully stop Codex Desktop, CLI and helper processes that can append or rewrite state;
2. take content-addressed JSONL backups and WAL-aware SQLite backups;
3. write a durable manifest containing thread/record identity, old provider value, intended `openai` value, hashes and rollback data, but no conversation text;
4. parse JSONL and update only the verified semantic provider fields;
5. update explicit SQLite row IDs inside bounded transactions;
6. leave unrelated records, cloud sessions, titles, content and project placement untouched;
7. validate and commit the manifest only after all stores agree.

An equal-length byte patch is not a general migration technique. If an old provider name and `openai` differ in byte length, use a stopped-writer structural rewrite with atomic replacement and verified backups. Even when lengths match, prefer the structural stopped-writer path unless a narrowly tested recovery case requires byte-level editing.

The live user-level configuration must also keep `model_provider = "openai"` in every official and API-compatible profile so future sessions do not reintroduce mixed values. Provider normalization does not repair generic or type-incompatible response-item IDs; evaluate and repair those separately.

### Provider acceptance checks

Provider normalization succeeds only when:

- every targeted JSONL line parses and every intended semantic provider field is `openai`;
- each targeted SQLite row is `openai`, database `quick_check` or the stronger chosen integrity check passes, and manifest counts reconcile;
- no out-of-scope cloud or unrelated local record changed;
- a new official session and a new API-compatible session both record `openai`;
- after a full restart, representative old sessions open and continue in both modes;
- the named manifest can roll back a fixture without overwriting newer activity.

## Safe mutation protocol

Default protocol:

1. fully stop Desktop and CLI writers;
2. acquire a repair lock;
3. inventory all targeted files and databases;
4. create content-addressed backups;
5. use SQLite's backup API for live-format databases;
6. record file identity, hash and intended record changes;
7. parse JSONL structurally and fail on malformed lines;
8. apply the minimum semantic changes;
9. update SQLite inside a bounded transaction;
10. parse every resulting JSONL line;
11. run SQLite integrity checks;
12. verify relationship invariants and target compatibility;
13. save a redacted repair manifest and history fingerprint.

An equal-length in-place byte edit can be useful when active appenders cannot be stopped and the exact bytes, encoding and file identity have been proven. It remains an exceptional technique. It needs a byte-level journal and convergence scans because an in-memory task may append the old value again.

Never restore an entire old JSONL file over a newer active file. Roll back only journaled changes after confirming the surrounding record still matches.

## Separate preparation from switching

Full history inspection can be expensive. Provide commands with distinct meanings:

- scan: read-only report;
- prepare: stopped-writer repair plus validation and fingerprint;
- rollback: reverse one named repair manifest;
- switch: fast fingerprint check, then configuration and auth transition.

If the history changes after preparation, the fingerprint gate should stop an official-mode transition before credentials or configuration are touched.

## Acceptance criteria

History is prepared only when:

- every JSONL line parses;
- all targeted semantic identifiers satisfy the tested rules;
- tool relationships are coherent;
- SQLite integrity checks pass;
- provider metadata matches the intended discovery strategy;
- every targeted historical provider value and every newly created local session use the verified `openai` identity;
- backups and the repair manifest are readable;
- rollback has been tested against a fixture;
- the target Codex build can open and continue representative old conversations.
