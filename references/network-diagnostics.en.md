# Network diagnostics

[简体中文](network-diagnostics.md)

“Reconnecting 5/5” is not one unique failure. Inspect redacted errors, paths and stages before classifying network, auth, model or history problems. A shared UI message does not establish a shared cause.

| Symptom | First checks |
| --- | --- |
| Timeout or broken stream | DNS/TLS, proxy, connection reuse and service state |
| 404 | Effective base URL composition and exact route; one response does not establish all capabilities |
| 401/403 | Auth kind, expiry, permission and destination |
| Model/effort unavailable | Exact model/effort pair, provider capability and UI cache |
| Each new/old task has a slow first turn, then works | Transport initialization, WebSocket retries and HTTPS fallback |
| Official mode still calls the relay | Effective config, profiles, environment or launch-argument overrides |
| 400 points to an old input ID/reasoning item | History protocol compatibility, not only proxy changes |

## Test HTTPS and WebSocket separately

Responses HTTPS support does not prove WebSocket upgrade support. Inspect exact routes, authentication, required headers, proxy forwarding and client fallback.

“5/5” alone does not establish exactly five WebSocket calls; confirm with this build's logs. WebSocket support is not universally mandatory: a client with HTTPS fallback may still use the relay, with first-turn delay.

Manage transport-disable or selection fields only when supported and tested on the installed version. Do not add an internet snippet the build ignores and declare success. If no effective switch exists, disclose the limit instead of disguising network failure through history edits.

## Proxy behavior is more than one flag

“Global VPN” does not prove the client's actual route. Distinguish system proxy, process environment, TUN, bypass rules, DNS and WebSocket routing. Browser access is not a substitute for a client probe.

Verify version-sensitive fields such as respect_system_proxy with a new process. On implementations supporting it, false means not actively following the system proxy; it does not bypass OS TUN or guarantee direct routing. Profiles may differ, but official-on/relay-off is not a policy for every machine.

## Minimal probes and closure

Start with unauthenticated DNS/TLS and URL checks, then authorized minimal auth/model and relevant transport probes in Codex's actual launch environment. Never send official OAuth to an unofficial endpoint or log auth headers, request bodies or secret query parameters.

Restart and retest route corrections; handle auth through re-login; ask before changing unsupported models; disclose unavoidable fallback cost. Retry supplier errors such as 503 within bounds, not by editing history or endlessly switching accounts. When uncertain, retain the last usable profile and report the proven layers and next probe.
