# Config recovery and external config writers

Codex can fail before an in-app agent is available when the user-level `config.toml` is empty, malformed, or replaced by a partial provider template. Recovery must therefore have an offline path that does not depend on Codex Desktop being able to start a conversation.

## Evidence boundary for CC Switch

A user-observed incident found Codex unable to converse after CC Switch had changed the live configuration. The damaged before/after files and exact CC Switch version were not preserved, so this guide does not claim a reconstructed root cause or that every current CC Switch release corrupts Codex configuration.

There is nevertheless a concrete ownership conflict in the current public design:

- CC Switch documents its database as the source of truth and the live configuration as output written during switching ([configuration model](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/docs/user-manual/zh/5-faq/5.1-config-files.md#L295-L322)).
- Its switch path backfills the outgoing profile and writes the selected profile to the live file ([switch flow](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/src-tauri/src/services/provider/mod.rs#L4931-L4942)).
- The Codex writer atomically replaces the live `config.toml` with the selected configuration text ([write path](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/src-tauri/src/codex_config.rs#L864-L880)).
- Current releases contain backfill and common-configuration protections, but common-config synchronization is still an explicit profile operation rather than proof that every externally added field will always be retained ([common-config synchronization](https://github.com/farion1231/cc-switch/blob/9a596158ca926e74b56243c08af67d9dd13fc27c/src-tauri/src/services/provider/mod.rs#L5418-L5460)).

This field guide uses the live Codex file as the source of truth and edits only declared route fields. The two ownership models must not control the same file.

> Choose one configuration writer. Do not let CC Switch and a custom live-config switcher both own the same `~/.codex/config.toml`.

If the user adopts the custom switcher described here, fully close CC Switch and disable any background or startup action that can rewrite Codex configuration. Import the required provider information deliberately; do not keep alternating between the two tools.

## Before introducing any switcher

Ask the user to save one known-good copy of the complete live configuration before the first write. The copy must:

- come from a state in which Codex has actually completed a request after a fresh restart;
- be stored outside the public repository and outside any directory an external config manager rewrites;
- preserve the complete file, including plugins, MCP servers, skills, hooks, permissions, projects, comments and unknown future keys;
- never include `auth.json`, OAuth tokens or API keys in source control;
- be replaced only after the user has deliberately accepted and tested a newer configuration.

This is a recovery checkpoint, not a requirement to accumulate unlimited generations. One user-managed known-good copy is a valid bounded policy. A script may offer an optional backup command, but it must not silently create an ever-growing archive.

## Recognizing damage

Treat any of these as a recovery event, not as an ordinary profile switch:

- `config.toml` is empty, missing or cannot be parsed;
- the file suddenly shrank to a small generic or common-provider template;
- previously present plugin, MCP, skill, hook, feature, permission or project keys disappeared;
- Codex reports that a referenced provider does not exist;
- route and credential type contradict each other;
- Codex opens but every request fails immediately after another config manager switched profiles.

Do not press another switch button in the hope that it will repair the file. Another projection may overwrite more evidence.

## Offline recovery with a known-good config

1. Fully stop Codex Desktop, Codex CLI, CC Switch, the custom switcher and every helper that may write `CODEX_HOME`.
2. Record the Codex version, damaged file size and a hash. If the user wants diagnostic evidence, copy the damaged file to a separate private location; never publish its values.
3. Check that the known-good copy is complete and parses as TOML. Compare key paths, not secret values.
4. Decide which authentication is currently active without exposing credential contents: official OAuth or API key. Configuration recovery does not itself convert one credential type into the other.
5. Restore the known-good file as the structural base.
6. Reapply only the route fields required by the active authentication:
   - official route: use the verified built-in provider identity and remove the relay override;
   - API-compatible route: use the verified built-in provider identity, set the intended endpoint override and select a model supported by that relay.
7. Parse the staged result, write it atomically, parse the live file again and confirm that unrelated key paths still exist.
8. Start a fresh Codex process. Verify effective route, auth type, model, plugins, MCP, skills, hooks, permissions and one new conversation before accepting the recovered file as good.
9. Resume a representative old local conversation only after the history compatibility gate has passed.

For a Codex build and relay that have passed this guide's shared-provider probe, the route-only difference is conceptually:

~~~toml
# Official OAuth profile
model_provider = "openai"
~~~

~~~toml
# API-compatible relay profile
model_provider = "openai"
openai_base_url = "https://relay.example/v1"
model = "relay-supported-model"
~~~

These fragments are not complete replacement configs. They are fields to merge into the restored live file. The [official Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) is authoritative for the installed release. Do not create a `[model_providers.openai]` table to redefine the reserved built-in provider.

## Recovery when no good config exists

Deleted values cannot be recovered exactly from nothing. The goal becomes controlled reconstruction:

1. Keep every writer stopped and preserve the damaged file privately.
2. Use the installed Codex version's configuration reference and startup diagnostics to build the smallest parseable configuration for the active authentication.
3. Recover non-secret key paths from trustworthy local evidence: project documentation, exported plugin/MCP lists, hook files, version-controlled project settings and user-confirmed recollection. Never scrape tokens into a prompt.
4. Add one subsystem at a time and restart when the installed build only loads that setting at process start.
5. Test a new disposable conversation before touching local history.
6. When Codex itself cannot converse, run a local offline PowerShell repair tool or use another coding agent such as Claude to inspect and reconstruct the file. Give that agent file paths and redacted structure, not credential values.
7. After the reconstructed file passes a real request and subsystem checks, ask the user to save it as the new known-good copy.

An agent must say which values were reconstructed, which were user-supplied and which remain unknown. It must never invent deleted MCP commands, hook paths, provider URLs or models.

## Recovering a provider-not-found failure

If Codex reports `Model provider '<name>' not found`, inspect the top-level `model_provider` and the matching provider definition before changing authentication. For the shared official/API-compatible design in this guide, both routes should use the verified built-in name `openai`; official mode omits `openai_base_url`, while a relay profile adds the top-level override. A stale custom name such as `relay` without a corresponding table is a configuration error, not an OAuth failure.

After repairing the live config, restart Codex. Existing local history may still contain the stale provider name; repair that separately through the stopped-writer history-preparation workflow rather than global text replacement.

## What the custom switcher should do about external writers

A machine-specific implementation may add a preflight warning that detects known config-manager processes and refuses a write while one is running. This is a concurrency guard, not a guarantee that a background process is absent. The durable rule is organizational: one tool owns live routing changes, every other tool is closed and no longer used for that file.

The switcher should also offer a read-only `config check` action that parses the live file and reports missing expected key paths without printing values. Recovery and backup remain explicit user actions; ordinary profile switching must stay fast and must not silently rewrite unrelated configuration.
