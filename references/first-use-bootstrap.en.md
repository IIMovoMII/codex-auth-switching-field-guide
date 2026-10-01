# First use and restart checkpoints

[简体中文](first-use-bootstrap.md)

First use can span interactive login and multiple process restarts. Saved configuration is not a usable profile, and every machine need not follow a fixed number of restarts.

## Continue from the actual starting point

| Starting state | Next action | If unsuccessful |
| --- | --- | --- |
| Official login only | Protect it, then guide API setup | Retain official state |
| API state only | Protect it, then guide official OAuth | Keep API recoverable |
| Both tested | Use routine switching | Transaction recovery |
| Neither exists | Ask which to establish first, then native login/local entry | Remain uninitialized |
| Snapshot exists but is unverified | Resume its checkpoint | Do not claim readiness |
| Unclear origin or route/auth conflict | Diagnose before overwriting snapshots | Expose the specific conflict |

A direct OpenAI API key may be a valid third mode. If the selected product only covers official OAuth and relay, classify it as unsupported rather than corrupted. Distinguish locally readable auth kind from a successful real request.

## No official login

Protect the working state, stage the official route and remove relay endpoints and other effective overrides. Then let the user complete the official login flow supported by this build. Never send official OAuth credentials to a relay URL.

Credentials must come from actual login; empty auth.json or sample tokens do not create a profile. Mark it usable only after the expected account/route and a minimal real request work in a new process. Capture snapshots only with stopped writers and stable refreshed auth.

On cancellation or login failure, retain the original profile and recovery path. Leave the target incomplete instead of overwriting a previously valid snapshot.

## No API/relay setup

Ask only unresolved non-secret preferences: provider, endpoint, model and reasoning level. Probe transport capabilities where possible rather than expecting the user to understand protocol terminology.

Collect the key through masked local input or a system credential UI, never chat. Verify the endpoint, supported configuration shape and target model, then activate route and auth transactionally. Failed new-process requests cannot produce verified-ready state. Keep rollback available and ask before changing an unavailable model or reasoning level.

## First history preparation

For cross-mode old-thread continuity, prove shared provider routing, then stop writers and prepare history. One first-switch entrypoint may chain these stages; separate manual commands are unnecessary. Unknown paginated layouts or unrecoverable model input require the disclosure or stop described in [history compatibility](history-compatibility.en.md), before activating target auth.

## Resumable progress

Persist non-secret checkpoints: workflow version, source/target profile IDs, stage, pre-change fingerprint, transaction reference, post-restart expectation, next user action and verified client version. Keep credentials and messages out of progress summaries.

Possible stages:

~~~text
Source protected → target needs login/input → staged → pending restart verification
                                                   → verified usable
                                                   → resume/rollback required
~~~

On re-entry, inspect actual state first; repeated clicks must not repeat overwrites. Explain how to continue before asking the user to close Codex. If a notification monitor is installed, use its supported bounded maintenance mechanism; never suppress errors indefinitely.

Startup-loaded settings require a new process. You may deliver the tool with pending acceptance steps, but cannot mark unperformed restart tests complete. Cancellation cleans only temporary profiles owned by this operation, not existing credentials or newer user data.
