# Safety and rollback

Authentication switching handles secrets and user history. Recovery design is part of the feature, not a later addition.

## Secret boundary

Never place these in the repository, prompt, console transcript or normal log:

- API keys;
- OAuth access or refresh tokens;
- cookies;
- complete authentication files;
- signed endpoint URLs;
- private account identifiers;
- conversation bodies.

The switching process can copy opaque credential bytes without displaying or parsing secret fields. Diagnostics should expose type, hash, age and validity result only.

## Local protection

Use the current operating system's user-scoped secret store and permissions—for example DPAPI and ACLs on Windows, Keychain on macOS, or an available keyring plus restrictive file modes on Linux. In every implementation:

- avoid inherited broad permissions;
- protect transaction rollback material as carefully as credentials;
- document that protected snapshots are not portable backups;
- provide a deliberate delete-profile operation.

The active credential may need to remain in Codex's expected plain file format. Protect it with filesystem permissions and minimize its exposure window.

## Process barrier

Before a sensitive transition:

1. identify all Desktop, CLI, helper and external config-manager processes that can read or write the state;
2. create a short expiring maintenance marker before asking the user to close Codex;
3. ask the user to close the relevant writers;
4. wait for clean exit with a bounded timeout;
5. refuse the write if any writer remains and clear or shorten the marker.

Do not terminate unrelated processes by name. Resolve exact executable paths and parent relationships.

CC Switch and a custom live-config switcher are incompatible owners of one Codex `config.toml`. A process-name check is only a convenience guard; the real safety rule is that the user selects one writer and stops using the other for Codex configuration.

## Transaction journal

The journal should contain:

- transaction ID and schema version;
- source and target profile IDs;
- start time and Codex version;
- hashes of source files;
- intended field changes;
- protected rollback blobs;
- completed stage markers;
- final verification result.

Write and flush the journal before the first state mutation. Update it after each durable stage. On next launch, detect an unfinished journal and offer verified recovery before any new switch.

## Backup rules

- Before introducing a config manager, ask the user to save one complete config that has passed a real request from a fresh Codex process.
- Do not require an ever-growing config archive. One deliberately managed known-good config is a valid bounded recovery policy; replace it only after the new state is accepted and tested.
- Use sibling temporary files on the same volume for atomic replacement.
- Verify a backup hash before relying on it.
- Use the SQLite backup API and an integrity check; do not treat the main database file alone as a complete WAL-aware backup.
- Keep history repair backups separate from ordinary profile snapshots.
- Apply retention limits only after at least one known-good rollback point exists.
- Never restore a full older history file over content that changed after the backup.

Config backup and history-repair backup are different things. The first protects a relatively small user configuration; the second may contain private conversations and live database state and must follow the stricter history workflow.

If `config.toml` is empty or reduced to a generic template, ordinary switching must stop. Use the offline playbook in [config recovery and external writers](config-recovery.en.md). When no good config exists, label reconstructed values explicitly and never invent missing commands, paths, endpoints or models.

## Rollback rules

Rollback should:

1. reacquire the same exclusive lock;
2. verify current file identity and expected post-write state;
3. reverse only the journaled fields or records;
4. restore the prior protected credential atomically;
5. parse configuration and authentication structure;
6. validate route/auth consistency;
7. mark the transaction rolled back;
8. retain a redacted audit record.

If current state no longer matches the journal, stop and require manual review. Silent force-restore risks deleting newer user activity.

## Failure injection

Test recovery by deliberately interrupting fixtures after:

- journal creation;
- configuration staging;
- configuration activation;
- credential staging;
- credential activation;
- history database update;
- verification but before commit.

Every interruption point should converge to either the complete old state or the complete new state. “Mostly switched” is not acceptable.

## User-facing safety

Before writing, show:

- source profile;
- target profile;
- fields to be changed;
- whether a history gate is required;
- whether Codex is fully closed;
- where recovery material will be stored.

After writing, show:

- resulting profile and auth type;
- validation result;
- whether a restart is required;
- exact rollback command or recovery path.

Never display the credential value.
