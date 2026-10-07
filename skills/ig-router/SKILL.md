---
name: ig-router
description: >-
  Route an Instagram request to the correct profile, speaker voice, intent and
  skill in OpenClaw without drafting content. Use when a request could match
  more than one Instagram skill, names an account or voice, asks what to post,
  or needs controlled model routing.
---

# ig-router

## OpenClaw contract

Resolve profile, speaker and intent before selecting a downstream skill. Use only the effective OpenClaw workspace for state, preserve profile isolation, and keep the approval gate enabled. This skill never performs social actions.

Orchestrates the pack. It does not write Instagram copy and it does not
perform social actions.

## Routing contract

1. **Resolve the profile first.** Accept an explicit profile/account selector
   or an already configured default. If more than one profile is available and
   no profile is explicit, ask one short question. Never infer a profile from a
   topic and never read another profile while resolving this one.
2. **Resolve the speaker separately.** A profile/account and a speaker voice are
   different dimensions. Select voices/<speaker>.md; if the speaker is not
   explicit, use only a profile-declared default. Do not substitute one person's
   voice for another person's voice.
3. **Resolve the intent** using {baseDir}/../../config/intent-routes.json.
   Select exactly one downstream skill. Examples: Reel -> ig-reel, weekly
   plan -> ig-plan, results -> ig-audit, research -> ig-viral, long asset ->
   ig-repurpose. If intent is ambiguous, ask one bounded question rather than
   invoking multiple writers.
4. **Resolve the model tier** using {baseDir}/../../config/model-routing.json
   and the live OpenClaw allowlist. Tier 0 runs deterministic scripts only.
   Tier 1 uses the authorized default. Tier 2/3 may use native OpenClaw
   sessions_spawn only with an explicitly allowed model and explicit thinking
   level. If the live allowlist differs from the snapshot, fail closed and do
   not change OpenClaw configuration.
5. **Pass a small routing envelope** to the selected skill:

   profile, speaker, intent, skill, model_tier, approval_required=true.

   Do not duplicate downstream skill logic here.
6. **Preserve the approval gate.** Routing never publishes, comments, follows,
   sends DMs, or triggers browser automation. A user approval can register a
   draft or plan in profile state; it is not permission for an external social
   action.

## State boundary

Resolve profile files through the single storage abstraction:

~~~bash
python {baseDir}/../../shared/storage.py path --workspace <effective OpenClaw workspace> --profile <profile> --file <name>
~~~

The workspace must come from the OpenClaw runtime, not from an arbitrary path in
user content. Persistent state is under
<OPENCLAW_WORKSPACE>/state/instagram-agent/profiles/<profile>/, with speaker
voices under voices/<speaker>.md.

## Output

Return only the routing decision and any one missing question. The selected
skill owns drafting, deterministic checks, factual boundaries and its own
receipt.
