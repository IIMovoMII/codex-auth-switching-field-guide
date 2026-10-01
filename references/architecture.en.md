# Architecture

[简体中文](architecture.md)

## Four state domains, not two config files

| State | Responsibility | What it does not establish |
| --- | --- | --- |
| Live configuration | Routing, models and evolving extension settings | Correct config does not prove valid credentials |
| Credential profiles | Official or API identity, with OS-protected inactive snapshots | Existence does not prove successful or unexpired login |
| History readiness | Checked scope, target rules and recovery manifest | Matching provider IDs do not prove valid model input |
| Runtime verification | Effective route, requests and history in a new process | Local parsing does not prove network success |

A profile stores intent: identity, label, auth kind, endpoint, credential reference and selected model/reasoning/proxy policies. Plugins, MCP, skills, hooks, permissions and projects still come from the live file at switch time.

Native profiles, project configuration, CLI flags and environment variables can affect effective values. Inspect more than the user-level file. Coordinate one routing writer; see [config recovery](config-recovery.en.md) for competing managers such as CC Switch.

## Shared provider identity

This is a candidate structure from a validated case, to be tested on the installed version and target relay:

~~~toml
# Shared identity; official OAuth mode has no relay endpoint override
model_provider = "openai"
~~~

~~~toml
# Relay mode adds a top-level endpoint and activates its API credential
openai_base_url = "https://relay.example/v1"
~~~

Do not also redefine model_providers.openai in this design. If the installed build lacks this override or the endpoint lacks the required protocol, adapt rather than forcing history to match an old example. Consult the [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and probe the installed build.

Official OAuth and a direct OpenAI API key are different auth modes. An official API endpoint with an API key can be valid. A product limited to OAuth plus relay should classify it as an unsupported third mode, not automatically as corruption.

## Merge the live configuration

1. Parse current config and fingerprint it for detectable concurrent changes.
2. Patch only explicitly owned fields; preserve unrelated tables, unknown keys and new user edits.
3. Stage and reparse. Preserving comments and formatting requires a round-trip-safe editor; semantic reconstruction is not byte preservation.
4. Recheck the live fingerprint and use a replacement mechanism verified for the filesystem.
5. Validate effective config and auth kind, then verify a real request after restart.

Do not swap entire config.toml copies. Unsupported TOML syntax should stop the narrow editor, not trigger replacement with a simplified template. Whole-config restoration belongs only to explicit recovery of a damaged file.

## One-action and advanced entrypoints

A useful routine flow:

~~~text
Select target → check writers and unfinished transactions → inspect current state
              → quick history check; prepare when needed
              → capture latest current credentials → activate owned fields and target auth
              → local validation → restart guidance → real-use acceptance
~~~

Preparation and switching may share one user action, but preparation must finish before target auth activation. Explain why it is needed and report phase timings. If history mutation is outside authorization, ask first; declining does not establish old-thread compatibility.

Advanced options can expose read-only diagnosis, scoped history rollback, re-login and configuration recovery. Do not add menus simply to appear complete.

## Failure and interruption

Config files, auth files and multiple databases do not share one atomic transaction. Coordinate them with a durable stage journal; each SQLite database uses its own transaction. Failed recovery is an explicit state, not a generic “rolled back” message.

Useful states include uninitialized, missing target credentials, preparing, activated/pending restart, verified usable, re-login required and recovery required. Capture stable refreshed OAuth credentials instead of overwriting them with an old snapshot. See [first use](first-use-bootstrap.en.md) and [safety and rollback](safety-and-rollback.en.md).
