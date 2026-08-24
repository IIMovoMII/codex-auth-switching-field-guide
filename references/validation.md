# Validation

A switcher is trustworthy only when behavior, preservation and recovery are tested together.

## Static invariants

Verify after every build:

- all profile identifiers are unique;
- no secret value is stored in source or logs;
- all owned fields are declared in one schema;
- configuration output parses;
- credential snapshots are protected;
- file permissions are restricted;
- transaction schemas are versioned;
- history manifests contain no conversation text.

## Configuration preservation tests

Create a fixture with representative unrelated settings:

- plugin entries;
- MCP servers;
- skills;
- hooks;
- permissions;
- projects;
- comments and unknown future keys.

Switch through every profile and assert that only owned fields change. Add a new plugin while one profile is active, switch away and back, and confirm it survives.

## First-use matrix

Test:

| Starting state | Expected behavior |
| --- | --- |
| Valid official state only | Register it, require intentional API setup |
| Valid API state only | Register it, require intentional official login |
| Both protected profiles ready | Switch normally |
| No credential | Stop before writing |
| Route/auth mismatch | Explain conflict; do not capture it |
| Expired OAuth | Require official reauthentication |
| Invalid API key | Keep prior working profile active |

For every row that creates a previously missing mode, test the required restart checkpoints. A pre-restart file inspection must never satisfy the post-restart acceptance gate.

## Profile matrix

For each official account and API provider:

- effective route is correct;
- credential type matches the route;
- selected model is available;
- proxy policy is applied as intended;
- HTTPS Responses works;
- WebSocket capability is measured separately;
- a new conversation works;
- a representative existing conversation resumes;
- a second switch returns to the previous profile cleanly.

## History tests

Use synthetic fixtures, not private conversations, to cover:

- mixed provider names across first-line session metadata, repeated thread-settings events and multiple SQLite stores;
- provider names both equal and unequal in byte length to `openai`;
- active and archived local sessions while cloud ChatGPT Work/Chat records remain untouched;
- valid response item identifiers;
- generic identifiers on different semantic item types;
- recoverable and unrecoverable reasoning records;
- tool calls and results;
- repeated provider metadata;
- archived sessions;
- malformed JSONL;
- SQLite WAL mode;
- history changing after preparation;
- rollback after partial repair.

Acceptance requires structural parsing, relationship checks, SQLite integrity and a target-version resume test.

For the shared-provider contract, additionally verify:

- the live user configuration sets `model_provider = "openai"` in every official and API-compatible profile;
- official mode omits the endpoint override and API-compatible mode supplies the intended top-level `openai_base_url`;
- the historical normalization manifest reconciles every changed JSONL field and SQLite row;
- no unexpected provider value remains in the intended local scope;
- new sessions created after preparation record `openai` in both modes;
- representative normalized old sessions resume through both modes after full restarts;
- response-item compatibility is tested independently, so a provider-only pass cannot hide an `item_`/typed-ID failure.

## Network tests

Separate:

- DNS/TLS;
- HTTPS route;
- WebSocket upgrade;
- proxy inheritance;
- authentication;
- model availability.

Run them with the same environment inherited by a newly started Codex process. Record sanitized results and the Codex version.

## Failure and recovery tests

Inject interruption after every transaction stage. Also test:

- two switch attempts at once;
- stale lock recovery;
- read-only or locked files;
- full disk;
- protected snapshot unavailable;
- state changed between preflight and commit;
- machine or Codex restarted between every bootstrap phase;
- bootstrap resume command run twice;
- rollback state changed by the user;
- Codex process restarts during the barrier.

## Upgrade test

After a Codex update:

1. rerun discovery;
2. compare configuration schema and effective fields;
3. recheck auth storage;
4. inspect new session records;
5. repeat HTTPS and WebSocket probes;
6. run history fixtures;
7. switch only after the version gate passes.

## Release evidence

A release or local deployment report should include:

- operating system and Codex version;
- tested profile types;
- configuration preservation result;
- history fixture result;
- network capability matrix;
- failure-injection result;
- privacy scan result;
- known limitations;
- recovery instructions.

Do not include tokens, account identifiers, private hosts or conversation text.
