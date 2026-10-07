# Upstream tracking

## Baseline

- upstream repository: https://github.com/Jakeschincariol/instagram-agent-skill
- fork repository: https://github.com/lacartaastral/instagram-agent-skill
- baseline commit: d03c56bb598be770c60b201f94237e5d1a4268a6
- baseline date observed: 2026-10-07
- local branch: openclaw/multiperfil-governed

The baseline was cloned and checked out before any fork-specific edits. The
original MIT license and attribution remain intact.

## Intentional fork seams

- skills/*/SKILL.md: preserve the editorial contracts, replace assistant-
  specific paths with OpenClaw {baseDir} resource resolution and add the
  profile/speaker/approval boundary.
- skills/*/*.py and JSON resources: preserve deterministic behavior; only add
  the smallest resource/configuration changes needed for OpenClaw profile rules.
- shared/: new deterministic storage, rules and model-routing contracts.
- config/: new intent routes, model policy snapshot and mutable platform rules.
- skills/ig-router/: new thin OpenClaw orchestrator; it does not draft or act.
- The upstream-specific plugin manifest is intentionally removed because this
  fork is discovered as native OpenClaw skills.

## Safe update procedure

1. Fetch upstream without changing the current working tree.
2. Inspect the diff against this baseline, especially skill paths, platform
   numbers and any action verbs.
3. Merge with --no-commit into the governed branch.
4. Reapply/update tests and central rule metadata if upstream changed behavior.
5. Run the full deterministic suite, compile checks, git diff --check, and
   OpenClaw discovery validation.
6. Commit the merge as a reviewable change. Never overwrite the fork config or
   state and never accept a change that adds publishing, broad scraping or
   cross-profile reads.
