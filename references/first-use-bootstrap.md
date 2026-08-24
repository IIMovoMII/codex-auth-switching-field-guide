# First use and restart checkpoints

First use is not a one-pass inspection. Some configuration, authentication, proxy and plugin state becomes trustworthy only after a fresh Codex process loads it, and OAuth requires an interactive user step. A safe implementation must survive several Codex shutdowns and continue from durable checkpoints.

## Hard invariant

A profile is not ready because its files look correct before restart. It becomes ready only after a fresh Codex process has loaded the staged state and a target-specific probe has succeeded.

The current Codex task may be interrupted when Desktop must close. Before asking for a restart, persist a non-secret checkpoint and show the exact action that resumes the bootstrap.

## Classify the starting state

| Detected state | Required response |
| --- | --- |
| Valid official state, no API profile | Protect the official state, then initialize API in stages |
| Valid API state, no official profile | Protect the API state, then initialize official OAuth in stages |
| Both states already validated | Use the normal switch transaction |
| Neither credential exists | Stop and ask which mode the user wants to establish first |
| Route, auth and model disagree | Do not capture the state; resolve the mismatch first |
| Snapshot exists but its post-restart validation is missing | Resume the recorded bootstrap phase rather than starting over |

Before a first transition between official and API-compatible modes, add a read-only history-provider checkpoint. Inventory all active and archived local provider values. If the installed Codex build has proved the shared `openai` identity contract and the inventory is mixed, require a separate approved history-preparation operation while every Codex writer is stopped. The credential bootstrap resumes only after that operation has its own verified manifest and fingerprint.

## Durable bootstrap record

Store only metadata such as:

~~~text
bootstrap_id
schema_version
starting_mode
target_profile_id
phase
pre_change_fingerprints
expected_post_restart_state
next_user_action
transaction_id
last_verified_codex_version
~~~

Never store a token, OAuth document, conversation body or secret endpoint parameter in this record. Credential bytes belong in the protected snapshot store.

Useful phases are:

~~~text
baseline_verified
target_staged
restart_required
interactive_login_required
post_restart_probe_required
target_verified
rollback_required
complete
~~~

Every phase transition must be idempotent. Repeating the resume command after a crash should verify current state and continue safely, not duplicate credentials or overwrite a newer configuration.

## When no official OpenAI login exists

1. Verify and protect the current known-good API state, if one exists.
2. Confirm Codex Desktop, CLI and helper writers are stopped.
3. Stage the official route by removing API endpoint overrides and applying only the owned official-mode fields.
4. Confirm the live route still uses the verified `model_provider = "openai"` identity. If old local provider metadata is mixed, finish the separately approved normalization and its rollback validation now.
5. Write <code>interactive_login_required</code> before starting Codex.
6. Tell the user to reopen Codex and complete the official OAuth flow in the official route.
7. After login, require another complete Codex shutdown so the bootstrap process can inspect a stable credential store.
8. Resume from the checkpoint and verify:
   - the active auth type is OAuth;
   - no API endpoint override remains;
   - a fresh official request succeeds;
   - the intended model is available;
   - a representative local task can be opened.
9. Only then protect the official snapshot and mark the profile ready.
10. Return to the user's requested final profile through the normal switch transaction.

If the OAuth flow fails or the route still points at an API provider, keep the previous known-good profile and leave a resumable failure state. Do not save the failed login as an official profile.

## When no API or relay configuration exists

1. Ask for non-secret intent:
   - provider display name;
   - base URL convention;
   - supported Responses transport;
   - desired model;
   - proxy policy.
2. Give the user a local masked input or provider-supported credential-entry action. Do not ask for the API key in chat and do not echo it to logs.
3. Validate the endpoint format without credentials where possible.
4. Stop all Codex writers.
5. Stage only the owned route, model and proxy fields, activate the locally entered credential, and save <code>restart_required</code>.
6. Reopen Codex from a fresh process.
7. Run separate post-restart probes for:
   - effective base URL;
   - active auth type;
   - selected model;
   - HTTPS Responses;
   - WebSocket upgrade when relevant;
   - system-proxy behavior;
   - preservation of plugins, MCP servers, skills and hooks.
8. Stop Codex again before capturing the stable credential snapshot.
9. Mark the API profile ready only after every required probe passes.

If the provider needs a model the user has not selected, present the discovered model choices and wait. Do not guess a model ID and call the profile complete.

## Why several restarts may be necessary

Different values become trustworthy at different times:

| Stage | What can be verified |
| --- | --- |
| Before restart | TOML parses, intended fields and rollback material are correct |
| First fresh process | Codex actually loads route, model, feature flags and credential type |
| After interactive OAuth | The official login exists, but the credential store may still be changing |
| After stopping again | The new auth state is stable enough to snapshot |
| Second fresh process | The protected snapshot can be restored and used successfully |

An implementation should display progress such as “stage 2 of 5 — restart required,” not claim that all checks were completed in one uninterrupted task.

## Resume experience

Before every restart, show:

- what has already been verified;
- why the restart is required;
- what the user must do while Codex is open;
- the exact resume command or button;
- what will be checked afterward;
- how to restore the starting profile if the next stage fails.

On resume, compare the live state with <code>expected_post_restart_state</code>. If it differs, explain the mismatch and offer rollback; never skip ahead.

## Validation cases

Test at least:

- no official state, successful OAuth across restarts;
- OAuth cancelled midway;
- no API state, locally entered valid key;
- invalid endpoint, invalid key and unavailable model;
- Codex reopened but not fully stopped before snapshot;
- machine reboot between stages;
- resume command run twice;
- live config edited between stages;
- rollback after each phase;
- final switch to both newly initialized profiles.
