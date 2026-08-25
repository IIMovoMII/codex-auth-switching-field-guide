# Network diagnostics

Treat a connection failure as a layered problem. Similar UI messages can come from different layers.

## Diagnostic layers

1. name resolution;
2. TCP reachability;
3. TLS certificate and hostname validation;
4. system and process proxy selection;
5. HTTPS request routing;
6. WebSocket upgrade routing;
7. API path construction;
8. authentication;
9. model availability;
10. application-level response compatibility.

Test one layer at a time with the same environment the Codex process actually inherits.

## Common symptoms

| Symptom | Likely layer | First checks |
| --- | --- | --- |
| Request timeout | proxy, firewall, route or WebSocket handshake | process proxy inheritance, direct HTTPS, upgrade request |
| 404 on a Responses path | base-path duplication or relay feature gap | effective base URL and exact route |
| 401 or 403 | credential type, scope or wrong route | active auth type without printing the token |
| Model not found | profile/model mismatch | provider model catalog and selected ID |
| Reconnect count on first turn, then success | WebSocket attempt followed by HTTPS fallback | upgrade support and timeout duration |
| Every route reaches the relay in official mode | stale endpoint override | effective merged config |
| Browser works but Codex fails | different proxy stack | system proxy and process environment |

## HTTPS and WebSocket are separate capabilities

A provider can implement the Responses HTTPS endpoint without implementing the Responses WebSocket upgrade. A successful HTTPS probe therefore does not prove WebSocket support.

Probe:

- the exact HTTPS request path;
- the exact WebSocket scheme and path;
- whether required headers survive the proxy;
- whether the server returns an upgrade response;
- whether the client times out before falling back.

Do not work around a missing relay capability by mislabeling the provider or mutating conversation history.

## Base URL composition

Clarify whether the configured base URL already contains the API version segment. A client may append a Responses route, while a relay expects a different base convention. A duplicated or omitted segment often produces a clean 404 that looks like a server outage.

Log only the host and normalized path when safe. Strip query parameters, credentials and signed fragments.

## System and process proxy behavior

“VPN enabled” is not enough information. Determine:

- TUN mode versus rule mode;
- operating-system proxy state and whether Codex can inherit it;
- environment proxy variables inherited by Codex;
- bypass rules;
- DNS behavior;
- whether WebSocket upgrades follow the same route as HTTPS;
- whether the current Codex build supports and honors a system-proxy feature flag.

On Windows, also distinguish system proxy, TUN and rule mode; on macOS or Linux, inspect the machine's actual network stack. A feature such as <code>respect_system_proxy</code> may be development-stage or version-sensitive. Test it with a new Codex process after changing configuration. Never describe it as permanent or universally available.

Official and API profiles may need different proxy policies. Make proxy policy an owned profile field only when the target environment actually requires it.

## A minimal probe sequence

1. Resolve the hostname.
2. Establish TLS without sending credentials.
3. Send a minimal authenticated HTTPS request.
4. Attempt the Responses WebSocket upgrade separately.
5. Request or validate the selected model.
6. repeat from the same process environment used to launch Codex.
7. compare official and API profiles.

Record timestamps, status class and sanitized route. Do not record request bodies or authorization headers.

## Interpreting reconnect behavior

If the first turn in each task waits through repeated WebSocket reconnects and later turns are faster, investigate per-task transport initialization and fallback caching. If both official and API modes show timeouts, the shared proxy path is more suspicious than the provider metadata. If only the relay returns 404, inspect relay route support and base URL composition.

The switcher should manage verified profile fields. It should not hide a transport failure by suppressing all diagnostics.
