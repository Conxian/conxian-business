# Vendored Run Gemini CLI action

This directory vendors the composite action from
`google-github-actions/run-gemini-cli` at upstream commit
`f77273f4c914e4bf38440cf36a0369cb64a37489`.

## Local changes

The upstream `action.yml` is preserved except for the two nested action refs
that violated this repository's immutable-action policy:

- `google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093`
- `actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f`

The command files and telemetry template are the only additional upstream
files required by the five workflows that invoke this local action. The
upstream Apache-2.0 license is retained in `LICENSE`.

## Maintenance

Treat this directory as a reviewed vendored dependency. Before changing the
upstream commit or refreshing any support file, compare the complete upstream
action tree, re-verify every nested `uses:` ref as a full commit SHA, and
update this provenance record. Do not switch callers back to the upstream
action until its nested refs satisfy the repository policy.
