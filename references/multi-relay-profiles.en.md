# Optional multi-account and multi-relay profiles

[简体中文](multi-relay-profiles.md)

Implement only when requested. A two-mode single-relay switcher need not become a large account manager. This module is adaptable design, not a claim that every feature exists in the author's local implementation.

## Store intent per profile

| Field | Meaning |
| --- | --- |
| Stable ID, label, auth kind | Human selection; a label is not a credential |
| Endpoint | No relay override for official OAuth; each API profile has its own route |
| Protected credential reference | Reference to local secure storage, not a plaintext key |
| Model and reasoning level | Selected pair, or an explicit preserve-current policy |
| Proxy/transport policy | Fields tested on this OS/client |
| Verification | Client version, capabilities, time and pending checks |

Never copy the whole config. Read common plugins, MCP, skills, hooks and projects from the live file at switch time.

## Different model catalogs

Model and reasoning level form a capability pair. Verify exact model IDs, effort parameters and actual endpoint acceptance, not only provider claims. Menu caches may differ from effective settings; a menu does not establish max support.

When the user selects profile-managed models, switch model and effort in the same transaction. For preserve-current policy, first check target support and ask if unsupported. Never silently downgrade max to xhigh, substitute models or equate different aliases. A candidate list is for selection, not automatic fallback authorization.

## Lifecycle

- **Add official account:** protect the current state, perform native OAuth and new-process validation, then capture. Show account identity locally only as necessary.
- **Add relay:** collect non-secret settings, enter the key locally and test a real request; failures remain unready.
- **Update:** stage endpoint, credential, model or proxy changes and retain the last usable state until verified.
- **Re-login:** expiry/refresh failure affects that profile, not other accounts.
- **Delete:** first rule out active status and unfinished transaction references; clarify whether credentials are deleted too.
- **Cancel/interruption:** resume a checkpoint or recover without overwriting later user configuration.

See [first use](first-use-bootstrap.en.md) and [safety and rollback](safety-and-rollback.en.md).

## Routine switching

On a build with proven shared-provider support, official accounts use openai with their own OAuth; relays A/B also use openai, with their own endpoints, credentials and model policies.

One entrypoint may check state, prepare history when needed and activate the target. Explain history invalidation and progress; failed preparation retains current auth. Advanced menus handle adding, updating, diagnosing and recovering without making every routine switch a manual procedure.

CC Switch is not required. A self-managed profile implementation can stop it from writing this Codex config without uninstalling it for unrelated uses. Do not let uncoordinated managers overwrite the same live file.
