# Discovery

[简体中文](discovery.md)

Inspect read-only before implementing. Return redacted findings, not config, auth or transcript dumps.

## Facts to inspect

- OS, actual Desktop/CLI versions, executables and state locations; they may use different builds or CODEX_HOME directories.
- Active writers, external managers and unfinished transactions. A closed window is not a stopped process; merged/renamed apps invalidate fixed-name assumptions.
- Effective config and its sources: user, project, native profile, CLI and environment. Layer support is version-specific; a visible file value may not win.
- Route, model, reasoning level, transport and proxy; locations of plugins, MCP, skills, hooks, permissions and projects.
- Auth kind/storage: OAuth, API key, missing or unreadable, without credential values.
- Active/archived JSONL, SQLite schema, WAL, paginated/segmented/inherited history and cloud boundaries.
- Protected snapshots, last validation and available recovery material.

Generalize paths in public reports. Determine whether model menus come from cache, service responses or profile settings. A menu entry does not prove endpoint support for the model/effort pair.

## Endpoint probes

Test path composition, TLS, auth, HTTPS Responses, optional WebSocket, exact model and reasoning level separately. Use minimal non-sensitive requests; real requests may incur cost and must stay within the accepted scope. Retain only status categories and timing.

A 401 does not prove a bad provider ID; a 404 does not prove every WebSocket route is unsupported; browser access does not prove Codex inherits the same proxy. See [network diagnostics](network-diagnostics.en.md).

Prove the shared openai identity on both the official route and relay override, including new-task metadata. If the other login does not exist, mark it pending and guide setup rather than inventing a bidirectional pass.

## Ask only for real choices

Group unresolved decisions that affect implementation:

- Two modes or several accounts/relays?
- Must old tasks continue across every profile? What is acceptable when safe conversion is impossible?
- Command-line, small window or an existing system entrypoint?
- Should model/reasoning settings follow profiles or preserve the current selection?
- When can Codex close? What recovery-space/retention tradeoff is acceptable?
- Which tool owns routing, and should existing profiles be imported?

Do not repeat preferences already supplied, turn readable OS/path/version facts into a questionnaire, or request complete config/auth files in chat.

## Discovery handoff

Report current state, chosen scope, missing credentials, shutdown-required actions, history layout and pending checks. Diagnose conflicts before writing. Unknowns need a next probe, not automatic classification as corruption.
