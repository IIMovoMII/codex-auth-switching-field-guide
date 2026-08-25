# Optional multi-relay switching without CC Switch

Some users need official OAuth plus several API-compatible relays, each with different models, credentials and proxy behavior. A machine-specific switcher can support that directly. This is an optional implementation path, not a feature every deployment must enable.

## Profile model

Store intent per profile instead of storing a complete `config.toml`:

~~~text
profile_id
display_name
kind: official | api_compatible
official_account_hint (non-secret)
base_url (API profile only, no embedded credential)
credential_snapshot_reference
preferred_model
optional_fallback_models
proxy_policy
transport_policy, only if verified on this Codex build
last_validated_codex_version
last_validated_at
ready: true | false
~~~

The profile manifest must not contain an API key, OAuth token, cookie or signed URL. Each inactive credential is stored separately with operating-system protection. The live Codex credential remains in the format required by the installed version.

## Field ownership

For the built-in OpenAI provider plus compatible endpoint overrides, the optional multi-relay switcher normally owns only:

- `model_provider`;
- top-level `openai_base_url` presence or value;
- `model`;
- a specifically verified proxy feature flag;
- a specifically verified transport feature flag, if the user chooses to manage it.

Plugins, MCP servers, skills, hooks, permissions, projects and unknown future settings remain owned by the current live Codex file. Every switch reads that file first and patches only the owned fields.

If a relay requires a genuinely different wire protocol, custom headers, or a custom provider definition that cannot use the built-in endpoint override, do not pretend it is equivalent. Give it an explicit provider contract, retest history behavior and explain that shared `openai` history compatibility may not apply.

## Why relay-specific models belong to profiles

Different relays expose different model names and capabilities. Each API profile therefore carries its own preferred model and optional user-approved fallbacks. During onboarding:

1. collect the base URL and requested model without a secret;
2. accept the API key through a masked local input, never through chat;
3. stage route, credential and model together;
4. restart Codex when required;
5. run a minimal real request and capability probe;
6. mark the profile ready only if the selected model succeeds.

Do not silently substitute another model. If the saved model disappears, stop and show the profile name, requested model and redacted validation error so the user can choose a replacement.

## Suggested user commands

A generated CLI or small desktop app may expose actions such as:

~~~text
init
status
profile list
profile add official
profile add relay
profile update <profile-id>
profile remove <profile-id>
switch official:<profile-id>
switch relay:<profile-id>
config check
history scan
history prepare
recover
~~~

Names are illustrative. The important separation is functional:

- profile management handles intended endpoint, account, model and proxy policy;
- switching changes live route plus credential as one transaction;
- `config check` is read-only;
- history preparation is slow, explicit and separate;
- recovery is not hidden inside an ordinary switch.

## First profile of each type

An implementation cannot create a valid official profile without a real OAuth login, and it cannot create a relay profile without a real endpoint, key and working model.

When only API mode exists:

1. register the tested current relay profile;
2. protect its inactive credential state;
3. remove the endpoint override and let the user complete official OAuth;
4. fully restart Codex and validate a real official request;
5. register the official profile;
6. return to the user's requested final profile through the normal switch transaction.

When only official mode exists, use the symmetric flow. Ask for relay metadata, collect the key locally, then validate after the required restart. Persist a bootstrap checkpoint before closing Codex so the process can resume safely.

## Switching transaction

1. Acquire an exclusive lock and confirm Codex plus every competing config manager is closed.
2. Read and parse the current live configuration.
3. Validate the target profile, protected credential and history gate.
4. Write a durable transaction journal containing hashes and rollback material.
5. Save the current live credential back to its source profile if it has been validated.
6. Create a staged config by changing only owned route/model/proxy fields.
7. Stage the target credential.
8. Parse both staged structures and verify route/auth consistency.
9. Atomically activate config and credential according to ordering tested on the current operating system and filesystem.
10. Verify file identities and mark the transaction committed.
11. Tell the user a full Codex restart is required; validate the effective route from the fresh process.

If any step fails, restore only the journaled pre-switch state. Do not overwrite a newer live file whose identity no longer matches the journal.

## Official versus relay behavior

For a proven compatible build:

| Profile type | `model_provider` | `openai_base_url` | Credential | Model |
| --- | --- | --- | --- | --- |
| Official account | `openai` | absent | that account's OAuth state | official supported model |
| Relay A | `openai` | Relay A URL | Relay A API key | Relay A model |
| Relay B | `openai` | Relay B URL | Relay B API key | Relay B model |

This stable provider identity helps new local sessions remain discoverable across profiles. It does not prove that every relay produces response items compatible with the official endpoint. Run the separate response-item history probe before resuming relay-created conversations through OAuth.

## Removing CC Switch from the workflow

Import only the information the user confirms: profile display name, endpoint, model and intended proxy behavior. Enter keys again through the new switcher's local secret boundary instead of reading or copying another tool's internal database through a model.

After every required profile works in the custom switcher:

1. fully close CC Switch;
2. disable its startup/background behavior;
3. run the custom switcher's read-only config check;
4. perform one full official-to-relay-to-official validation cycle;
5. keep CC Switch from writing the same live `config.toml` again.

The user may keep CC Switch installed for unrelated tools, but it must not remain an alternative owner of Codex's live configuration.
