# Security policy

This repository contains documentation, not a credential service. Even so, examples and issue reports can accidentally expose private material.

## Never publish

- <code>auth.json</code> or any equivalent credential file;
- API keys, OAuth tokens, cookies or signed URLs;
- private relay addresses;
- real usernames, home directories or account IDs;
- conversation bodies or unredacted rollout files;
- encrypted snapshots together with material that weakens their protection.

## Reporting a security issue

Use a GitHub private security advisory for a vulnerability in this guide or its validator. Do not open a public issue containing secrets.

If a secret was posted:

1. revoke or rotate it immediately;
2. remove it from the visible content and Git history;
3. invalidate related sessions where supported;
4. review local and provider access logs;
5. disclose only a redacted timeline.

The repository maintainers cannot recover or secure credentials from a user's machine.
