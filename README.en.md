<div align="center">

# Codex Auth Switching Field Guide

**Switch between official accounts and API relays while keeping settings current and local conversations usable.**

[![Field guide](https://img.shields.io/badge/type-field%20guide-6f42c1)](#what-this-is)
[![Structure checks](https://github.com/IIMovoMII/codex-auth-switching-field-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/IIMovoMII/codex-auth-switching-field-guide/actions/workflows/validate.yml)
[![MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

[简体中文](README.md) · [Agent brief](SKILL.en.md) · [Desktop notification guide](https://github.com/IIMovoMII/codex-desktop-notification-field-guide)

</div>

## What this is

This is **a product brief and field guide for coding agents**, not a ready-to-run switching application.

Give the prompt below to Codex. It should inspect your environment and requirements, then build a suitable script or small app. Keep it to official ↔ relay switching, or add multiple official accounts, relays and model preferences. You do not need to copy the author's machine setup.

## Who it helps

- You usually use a relay API but sometimes switch to an official account.
- You frequently update plugins, MCP, skills or hooks and do not want an old config to overwrite them.
- You want to continue the same local conversations across modes.
- Your relays have different models, reasoning levels or proxy requirements.
- Another configuration manager damaged your settings and you want an offline recovery route.

## Deploy in one prompt

Copy this to your coding agent:

~~~text
Read https://github.com/IIMovoMII/codex-auth-switching-field-guide, starting with SKILL.en.md, then build and validate a Codex account/endpoint switcher for my environment and requirements.
~~~

The agent should inspect facts it can safely read and ask only for decisions you need to make. **Login, secret entry, shutting down Codex and history changes must be explained; existing login state cannot be invented.**

## What you can build

| Capability | Practical benefit |
| --- | --- |
| One-action switching | Combine necessary checks, history preparation and activation in one entrypoint; keep advanced repair options separate |
| Preserve evolving settings | Patch the current live configuration instead of alternating between two old copies |
| Old-conversation compatibility | Check provider identity, model input and UI indexes separately; repair only proven-safe cases |
| Multiple accounts and relays, optionally | Keep credentials, model and reasoning level per profile without copying the whole config |
| First-use guidance | Guide OAuth when missing, or collect missing API settings locally |
| Recoverable failures | Distinguish login, configuration and history failures instead of asking users to keep retrying |

These are selectable product capabilities, not an installer or implementation shipped by this repository.

The field evidence mainly covers switching between one official account and one relay on Windows. A complete first-use wizard, multiple accounts and multiple relays are design options requiring implementation and acceptance on the user's machine.

## What “keep my conversations” means

The goal is to preserve local messages, tool results, project placement, and the ability to open and continue the original task.

However, **visible messages do not prove the model can accept every old input**. A relay may return identifiers or reasoning data that an official endpoint rejects. Preserve visible history, disclose any model-input loss, and retain recovery material. Do not delete conversations merely to make a scanner report zero findings.

Acceptance has three parts: **old content remains visible, the model can continue, and new messages are saved and displayed.** This is not a permanent guarantee across every future Codex version, account or relay.

## Why switching can sometimes be slow

History validation often costs more than changing credentials. Unchanged history can use a fast check; new relay records, Codex updates or changed repair rules may require preparation again.

One investigation traced minutes of delay to per-byte decoding in an interpreted script. Measure stages and optimize the actual bottleneck instead of skipping validation. First-use setup and routine switching should also report separate progress.

## Handling Codex updates

A Codex update does not automatically require rewriting the switcher. Check whether the changes affect switching; reuse compatible behavior and adapt the affected parts when necessary. Reuse valid checks for routine switching, reserve full history checks for cases that need them, and explain what is taking time.

When history compatibility cannot be established, stop before switching and preserve the current state. Keeping this fail-before-switch behavior reduces accidental changes but cannot guarantee that future errors never occur. Multiple accounts and elaborate interfaces are optional; a two-mode switcher need not implement everything.

## First use and recovery

You can start without a previous official login, but you still need to complete the first OAuth login yourself. Some checks require a full Codex restart; the tool should save progress and explain the next action, not claim completion early.

If CC Switch or another manager owns the same config, choose one routing owner to avoid competing writes. An empty, template-only or broken config can be restored from one known-good copy. Without a backup, rebuild from trustworthy evidence. See [first use](references/first-use-bootstrap.en.md) and [config recovery](references/config-recovery.en.md).

Saving multiple official accounts does not automatically share cloud chats. Visibility and continuation across accounts need separate tests; this guide has no completed two-official-account acceptance. If chats disappear from view, check identity, data location and filters before concluding that records were deleted.

## Scope and evidence

Field evidence is primarily from Windows. Adapt the design to macOS or Linux using local equivalents; **there is no claim of a finished or fully tested three-platform application**.

This revision includes copied-history tests using native Codex CLI 0.159.2, a later 0.162.0-alpha.2 isolated review of legal IDs with no replayable reasoning content, record-by-record checks after a real switch, and regression tests on PowerShell 5.1 and 7. See [validation](references/validation.en.md) for evidence, gaps and measurements. The green badge checks document structure, links and limited privacy patterns, not successful deployment on your machine.

## Contribute

Share redacted reproductions and validation results. Never submit actual keys, auth files, conversation history or backups. Read [security](SECURITY.en.md) and [contributing](CONTRIBUTING.en.md) before publishing.

[MIT license](LICENSE).
