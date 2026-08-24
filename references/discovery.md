# Discovery

The implementation should begin with a read-only inventory. The output is a redacted state report, not a dump of local files.

## 1. Establish the runtime boundary

Record:

- Windows version and architecture;
- Codex Desktop and CLI versions;
- whether Desktop and CLI use the same Codex home;
- relevant process names and child processes;
- CC Switch or any other config/profile manager that can rewrite the same Codex home, including startup or background behavior;
- whether the current app combines ChatGPT and Codex surfaces;
- configuration reload behavior observed in this build.

Do not assume that closing a visible window ends every process. Prove which processes can still write configuration, credentials, JSONL or SQLite.

## 2. Locate state

Discover rather than hard-code:

- effective Codex home;
- live <code>config.toml</code>;
- active authentication store, such as <code>auth.json</code> or a supported keyring;
- rollout or session JSONL roots, including archived locations;
- SQLite databases and their journal mode;
- plugin, MCP, skill and hook configuration;
- project or workspace metadata;
- any existing profile-switcher state.
- whether the user has a complete, known-good `config.toml` that passed a real request after restart; report presence only, never its values.

Use placeholders such as <code>%USERPROFILE%\.codex</code> in reports. Never publish a real username or absolute home path.

## 3. Parse configuration structurally

Use a TOML parser when possible. Inventory:

- effective <code>model_provider</code>;
- top-level endpoint override fields;
- selected model and reasoning settings;
- custom provider tables;
- feature flags related to transport or proxy handling;
- plugins, MCP servers, skills, hooks, permissions and project entries;
- config layers or profiles that can override each other.
- signs that a complete config was replaced by a smaller generic/common template, such as missing previously expected subsystem tables.

The report should identify where an effective value came from. A visually present field may be shadowed by another layer.

Do not read the configuration as a block of text and replace matching lines. Duplicate tables, comments, ordering and later overrides make text substitution fragile.

## 4. Classify authentication without exposing it

Determine:

- whether the active state is OAuth, API key, absent or malformed;
- whether the credential store is readable by Codex;
- whether its apparent auth type agrees with the active route;
- whether an existing inactive snapshot is protected and current.

Diagnostics should return facts such as <code>auth_type = oauth</code> or <code>auth_type = api_key</code>. They should never print a token, refresh token, account cookie or full credential document.

If official login has never happened on this machine, report that the official profile is uninitialized. Do not create a fake placeholder and call it ready.

## 5. Inventory conversation storage

Count and classify, without copying content into logs:

- active and archived JSONL files;
- distinct session metadata provider values and per-value counts;
- distinct thread-settings provider identifiers and per-value counts;
- response-item identifier families by semantic type;
- every relevant SQLite store, its thread-provider values and per-value counts;
- WAL and shared-memory side files;
- currently open or recently changing files.

Reconcile the provider counts across semantic copies. A provider value present in one session metadata record but repeated in many thread-settings events is not several unrelated problems. Record which local thread IDs and storage layers would be in scope for normalization, but do not log titles or conversation text.

Separately identify cloud-backed ChatGPT Work/Chat records. Do not infer that they are editable local rollouts merely because the combined desktop app displays them beside Codex tasks.

Sample structure, hashes and timestamps rather than user messages. A useful report says “three reasoning items use an unexpected identifier family,” not what the user discussed.

## 6. Test endpoint capabilities

For each intended route, determine:

| Capability | Questions |
| --- | --- |
| Authentication | Which credential type is accepted? |
| Base URL | Does the configured base already include the API version segment? |
| Responses over HTTPS | Is the exact route implemented? |
| Responses over WebSocket | Is the upgrade route implemented and reachable? |
| Models | Which model identifiers are available? |
| Proxy | Does the process honor the expected Windows proxy path? |
| Error shape | Are structured errors preserved or rewritten? |

Use a minimal, non-sensitive probe. Separate connectivity, authentication and model availability so one failure is not misdiagnosed as another.

For the shared-identity design, also prove that the installed build can create a new session with `model_provider = "openai"` in both modes: official routing with no endpoint override, and API-compatible routing with the top-level `openai_base_url` override. If either route requires a different provider identity, do not normalize history to `openai`.

## 7. Define the requested profile set

Ask for intent only after machine facts are known:

- number of official accounts;
- number of API or relay providers;
- preferred model per profile;
- whether profiles need different proxy behavior;
- whether old conversations must be resumed in every mode;
- whether the user accepts a manual login step on first use;
- whether the switcher may require Codex to be fully closed.

The answer determines whether a simple two-state switch or a profile registry is appropriate.

## Discovery deliverable

Produce a redacted table containing:

- detected paths expressed generically;
- effective route and auth type;
- configuration consistency;
- active writers;
- history compatibility summary;
- transport capability summary;
- missing states that require intentional user setup;
- version-sensitive assumptions that must be validated.

Stop here if the state is inconsistent. Resolve the mismatch before designing writes.

If another manager owns the live config, stop and ask the user to select one writer. If the file is already empty, malformed or incomplete, follow [config recovery and external writers](config-recovery.md) before profile design.
