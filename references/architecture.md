# Architecture

The safest design treats switching as a transaction across several independent state domains.

## State domains

### Live configuration

This remains the source of truth for everything that evolves during normal Codex use. The switcher reads it at switch time and changes only owned fields.

Typical owned fields may include:

- provider identity;
- endpoint override;
- model selection;
- one transport or proxy feature flag.

The exact list must come from discovery. A field should not be owned merely because it appeared in one working example.

### Active credential

Codex needs its live credential in the format and location supported by the current build. Do not encrypt or reshape the active document if Codex cannot read that form.

### Inactive credential snapshots

Inactive profiles belong in an OS-protected local store. Each snapshot should include metadata such as profile ID, auth type, creation time and a hash of the encrypted blob. The metadata must not contain secret values.

On Windows, DPAPI is one reasonable local primitive. It normally binds a protected blob to a Windows identity, and sometimes to the machine, so it is not a portable backup strategy.

### Profile manifest

A profile is intent, not a full copied config:

~~~text
profile_id
display_name
route_kind
endpoint_reference
credential_snapshot_reference
preferred_model
proxy_policy
last_validated_codex_version
~~~

An endpoint may be stored as ordinary configuration if it contains no credentials. Tokens and signed URLs belong in the protected credential boundary.

### History compatibility gate

This stores a fingerprint of the history state that was explicitly inspected and prepared for a target mode. It should record:

- scope of files and databases;
- sizes and modification times;
- stable identities where available;
- manifest hash;
- repair-tool version;
- target compatibility rules.

It must not contain conversation text.

### Transaction journal

The journal describes the previous and intended states, stages completed, field-level changes and rollback material. It is written durably before the first mutation.

## Surgical configuration merge

At switch time:

1. parse the current live TOML;
2. verify it still matches preflight expectations;
3. remove or set only owned fields;
4. preserve unknown tables, comments and unrelated additions when the chosen TOML library permits;
5. serialize to a sibling temporary file;
6. parse the temporary file again;
7. replace the live file atomically where Windows semantics allow;
8. verify the resulting effective configuration.

If comment preservation matters and the parser cannot round-trip comments, use a syntax-aware editor or an explicitly tested narrow patcher. Do not fall back to global string replacement.

## Profiles, accounts and providers

Keep these concepts distinct:

- A provider describes routing semantics.
- An account describes an identity.
- A credential snapshot enables an account or API identity.
- A model choice may belong to a provider profile.

Several official accounts can share the same official route but require different protected OAuth snapshots. Several API providers may use the same provider identity but require different base URLs, keys and model choices.

This separation allows a user interface to show:

~~~text
Official
  - Personal account
  - Work account

API-compatible
  - Provider A / model family A
  - Provider B / model family B
~~~

The displayed hierarchy does not require swapping full configs.

## First-use protocol

Every first-use flow below is a durable multi-stage workflow. Persist a checkpoint before each required shutdown or restart, and do not mark a profile ready until a fresh Codex process has loaded and passed the expected probes. See [first use and restart checkpoints](first-use-bootstrap.md).

### Machine currently in official mode

1. Validate that the route and credential are genuinely official.
2. Register the current state as the first official profile.
3. Protect a snapshot without exposing it.
4. Ask the user to intentionally configure and test an API mode.
5. Capture the API state only after a successful minimal request.
6. Restore the requested final mode through the normal transaction engine.

If the API endpoint or key does not yet exist, collect endpoint/model intent and use a local secret-entry path before the staged restart. Do not ask for the key in chat.

### Machine currently in API mode

Use the symmetric flow. Register and protect the known-good API state, then guide the user through one official login. The login must occur after removing route overrides that would send the OAuth-backed request to a relay.

The OAuth result must be inspected only after the login process and a subsequent clean shutdown have stabilized the credential store.

### Inconsistent machine

Examples include an official route with an API key, or an API endpoint with an OAuth snapshot intended for another route. Do not capture this as a valid profile. Explain the conflict and require the user to choose a recovery direction.

## Switch transaction

A robust transition follows these stages:

1. acquire an exclusive switch lock;
2. confirm all Codex writers are stopped;
3. validate source state and target profile;
4. check the target history gate when required;
5. write the recovery journal;
6. preserve the current credential as its source profile snapshot;
7. stage the new live configuration;
8. stage and activate the target credential;
9. verify file permissions and parseability;
10. validate route/auth/model consistency;
11. commit the journal;
12. emit a short maintenance marker for cooperating monitors;
13. instruct the user to reopen Codex.

If any stage fails, rollback should use the journal and verify the restored state. Never continue from a half-applied state merely because the UI still opens.

## Keeping live configuration current

Because each switch begins from the live file, a plugin installed yesterday or an MCP server edited today survives. Profile data contributes only owned values. This is the central reason to prefer a merge-based switcher over whole-file snapshots.

When the owned-field schema changes, migrate the manifest explicitly and retain the previous schema version for rollback.
