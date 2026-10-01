# Config recovery and external writers

[简体中文](config-recovery.md)

An empty, template-only or syntactically broken config.toml may prevent Codex from starting a conversation. Recovery therefore cannot depend on a working Codex chat.

## Evidence boundary for CC Switch

A reported switch left incomplete configuration and unusable Codex, but before/after files and the exact version were not retained. Do not claim every CC Switch release corrupts config or invent the incident's precise cause.

Previously examined revision 9a596158ca926e74b56243c08af67d9dd13fc27c manages saved configuration in its database/profiles and writes target text into the live file. See its [configuration model](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/docs/user-manual/zh/5-faq/5.1-config-files.md#L295-L322), [switch flow](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/src-tauri/src/services/provider/mod.rs#L4931-L4942) and [write path](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/src-tauri/src/codex_config.rs#L864-L880). This is pinned-revision design evidence, not a review of today's latest release.

A live-config-based switcher may conflict with another manager projecting full saved configs, overwriting new fields in either direction. Default to one user-selected routing manager unless a tested coordination mechanism exists. Unrelated features do not need uninstalling.

## Stop before recovering

For empty files, parse errors, missing fields, missing providers or immediate request failures, stop writers and repeated switching. Inspect effective overrides and actual auth; a smaller file alone does not prove damage.

Suggest one private known-good full config outside public repositories and external-manager control. It is not an auth snapshot and does not prove old credentials still work. Keeping a damaged file for investigation is a user choice, not unbounded backup accumulation.

## Known-good restoration

1. Stop Desktop, CLI and relevant configuration managers.
2. Verify the recovery point's version, hash and field structure; classify current auth without secrets.
3. Restore full structure, then patch only route/model/proxy fields matching the intended target.
4. Official OAuth removes relay overrides; relay mode uses that profile's endpoint, API auth and supported model. Restoring config does not change auth automatically.
5. Stage, parse, activate and verify unowned settings remain.
6. Use a new process to test a real request and key extensions; old-task continuation also needs history readiness.

The version-proven shared structure uses model_provider = "openai" with a top-level openai_base_url for relay mode. Example routing lines are not a full replacement config. Fix missing provider definitions before deleting auth or history.

## Recovery when no good config exists

Missing values cannot be reconstructed exactly without evidence:

- Start with a minimal configuration supported by this build and the actual auth mode; never guess secrets.
- Recover settings from trustworthy local project notes, extension inventories, hook files and user confirmation.
- Verify each subsystem separately; startup-loaded changes need a new process.
- Test a disposable new task first, then old tasks after the history gate.
- If Codex cannot work, use local commands or another coding agent, such as Claude, to inspect redacted structure.
- Distinguish evidence-restored, user-supplied, newly created and still unknown values.

Validate before making the result the new known-good recovery point. A tidy generic template must not conceal lost capabilities.

## Optional recovery entrypoints

Implement read-only config checks, recovery-point selection, re-authentication, relay/model updates and unfinished-transaction recovery according to scope. Recovery is not automatic guessing: disclose changes and respect later user edits. Routine one-action switching must not silently perform disaster recovery.
