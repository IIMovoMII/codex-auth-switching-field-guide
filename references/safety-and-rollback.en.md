# Safety and rollback

[简体中文](safety-and-rollback.md)

## Credential boundary

Report auth kind, profile status and redacted errors only. Do not expose keys, OAuth content, cookies or signed URLs to models, logs or repositories. Collect secrets through local masked input or native authentication.

Inactive credentials may use Windows DPAPI, macOS Keychain or an available Linux keyring; verify permissions and portability. Active credentials must retain a format Codex understands. Do not encrypt them independently and expect the client to read them. Auth may live in files, a keyring or both; replacing auth.json is not a universal contract.

## Routine switching transaction

- Stop writers, rule out competing managers and acquire an operation lock.
- Validate source config, target credentials, history readiness and recovery capacity.
- Capture current stable refreshed credentials; stage owned-field changes and target auth.
- Persist recovery information before mutation, then reparse and verify route/auth consistency.
- Restore pre-transaction config and auth on failure. If restoration fails, retain evidence and enter recovery-required state.
- Correct files mean activated/pending restart. Runtime acceptance requires a real request from a new process.

Multiple file replacements are not one atomic operation. The journal must distinguish not written, written, verified, rolling back and rollback failed, including an interrupted final journal write.

## Recover the two transactions separately

History preparation precedes auth switching. If history is prepared successfully but OAuth later fails, normally restore only configuration and credentials. Compatible history can remain, with clear disclosure. Restoring pre-repair history requires its own manifest-scoped rollback. Do not silently make verified history incompatible again after a login failure.

A durable manifest coordinates history files; each SQLite database has its own transaction. On unfinished work, classify each target as original, applied or unknown before continuing or rolling back. Without implemented and tested crash recovery, provide an honest manual path rather than claiming universal automatic recovery.

## Rollback must not erase newer activity

- Verify identity, hashes, record location and expected values before reversing journaled changes.
- Full restoration is possible for an unchanged offline file with proven hashes. With appended activity, use only a verified field/record-level reversal or stop.
- Revert SQLite through explicit row IDs and expected values, not an old whole database over new tasks.
- Preserve evidence on mismatch and report conflict, never false rollback success.
- Repeated rollback should be idempotent: leave restored values alone and reject unknown states.

Test exceptions, disk-full failures, denied access, process interruption and intervening user edits separately. Catching exceptions does not prove power-loss recovery.

## Retention and capacity

A human config recovery point can be one known-good file. Original history, SQLite backups and repair manifests are separate recovery material that may contain full private content. A redacted diagnostic does not make the entire repair directory safe to publish.

Agree on a retention count or capacity and stop before insufficient space. One overwritten failure summary is enough; read-only checks need no new backup. Remove older history recovery points only after transaction completion and acceptance, when no unfinished transaction references them, according to the user's retention choice. Never delete the sole viable recovery material merely to satisfy a limit.

Some manifests contain old item_json or field values for rollback. Protect their storage and permissions; do not claim every manifest is transcript-free.

## Failure handoff

Show the remaining active mode, failed stage, recovery outcome, local recovery location and next action without secrets. Avoid unbounded retries. Stop new switching if consistency is uncertain and prioritize offline recovery. If Codex cannot start, a local script or another coding agent can inspect redacted structure.
