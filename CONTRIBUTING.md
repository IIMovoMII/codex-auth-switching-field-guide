# Contributing

Contributions should improve the quality of the method, not turn this repository into a machine-specific credential switcher.

## Good contributions

- a reproducible Codex behavior with version and platform context;
- a safer discovery or rollback pattern;
- a synthetic history fixture that exposes a compatibility edge case;
- a clearer first-use decision;
- an additional validation case;
- a correction backed by a minimal probe.

## Please avoid

- API keys, OAuth files, private relay hosts or account identifiers;
- real conversation content;
- absolute local paths or usernames;
- a script that assumes one person's Codex layout;
- claims of universal support without version evidence;
- generated bulk text that has not been technically reviewed.

## Pull request checklist

1. Explain the observed problem and environment.
2. State whether the behavior is documented, measured or inferred.
3. Add a safe way to validate the claim.
4. Update both language pages when their shared meaning changes.
5. Run:

~~~text
python scripts/validate_pack.py
~~~

6. Confirm that no credential or private host appears in the diff.

By contributing, you agree that your contribution is licensed under the MIT License.
