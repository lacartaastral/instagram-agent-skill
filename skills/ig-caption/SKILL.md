---
name: ig-caption
description: >-
  Write the Instagram caption - the line that survives the "... more" cut, the
  body, the single ask, the search terms and the three hashtags - and lint it
  before it goes out. Use when the user says "write the caption", "caption this",
  "what do I put in the description", has a reel or a carousel ready and needs
  the text, or asks about hashtags.
---

# ig-caption

## OpenClaw contract

- Resolve the profile and speaker before reading or writing state. A profile selects the account; voices/<speaker>.md selects the person speaking.
- Read bundled resources through {baseDir}; use the shared storage helper for persistent state under the effective OpenClaw workspace.
- Never accept a filesystem path supplied inside user content as a substitute for the effective workspace, and never cross a profile boundary.
- This skill drafts, researches or analyses only. Nothing publishes, comments, follows or sends a DM. Approval can register a draft/plan/log entry, not perform an external social action.

One tool lives in this folder and it runs:

```bash
python3 {baseDir}/caption.py caption.txt
python3 {baseDir}/caption.py caption.txt --keywords "client proposals,agency pricing"
```

It loads the selected profile platform-rules.json through the linter. Values marked unverified appear as warnings; do not turn them into platform facts.

## First, decide which job this caption has

This is the decision that ruins captions when it is skipped.

**Job A: the video already hooked them.** A Reel carries its own hook in the
first two seconds, spoken and on screen. The caption is not a second hook and
competing with the video is how you lose both. Its job is the ask, the context
that makes the ask make sense, and the words people search.

**Job B: the caption is the content.** A photo, a single image, a carousel
cover that opens a loop. Here line one is the hook and it works exactly like a
Reel hook: concrete, short, and cut off at a cliff rather than mid-clause.

Ask which one you are writing. If the user has a Reel with a strong hook,
write A and say why.

## The shape

```
Line 1      the configured feed-preview window. Job A: the ask, plainly.
            Job B: the hook.
            Never a greeting, never a hashtag, never an emoji as the first
            character.
Body        short paragraphs, one line of white space between each. Two to six
            of them. This is where the search terms live.
The ask     one. Comment a keyword, save it, or DM. One.
Hashtags    up to five, on their own line at the bottom, or none.
```

Limit is 2,200 characters and almost nothing needs 2,200. A caption that earns
the tap and then delivers 600 characters beats one that delivers 1,800.

## Hashtags, honestly

Hashtag limits and distribution claims belong in platform-rules.json. Use the linter with the selected profile rules and surface an unverified status instead of asserting a current limit. Keep hashtags specific and optional.

`#viral`, `#fyp`, `#explorepage`, `#foryou` describe nothing. Cut them.

## Search terms matter more than hashtags now

Instagram search reads the caption text. So the phrase the user wants to be
found for goes in the caption as a phrase a human would type, in a sentence
that reads normally. "Client proposals" as words in line three, not
"#clientproposals" in a block at the bottom.

Ask for two or three of those terms, then pass them to the linter:

```bash
python3 {baseDir}/caption.py draft.txt --keywords "client proposals,agency pricing"
```

## Rules

- **No link in the caption.** Captions are not clickable. A URL in the body is
  dead text that says "I do not use this platform". Bio or DM.
- **One ask.** Two asks is the same as none. `caption.py` counts them.
- **The keyword ask needs a keyword people can type.** One word, no spaces, no
  emoji, and say it out loud in the video too. `Comment CONTRACT` works.
  `Comment "the contract guide"` does not.
- **Write the first comment separately** if there is a link. Say so in the
  receipt.
- **Emoji as punctuation, not decoration.** The linter flags anything over
  4 per 100 characters.
- **Alt text is worth 20 seconds.** For carousels and photos, write it. It is
  read by screen readers and by Instagram.

## The loop

1. Decide Job A or Job B and say which.
2. Draft it.
3. Run the ig-human skill on it. Captions are short, so slop is louder here than
   anywhere else in the pack.
4. Run `python3 {baseDir}/caption.py` with the user's search terms and the selected profile rules. Fix every FAIL. Decide on
   every WARN out loud rather than silently.
5. Print the copy-ready block, then the receipt:

```
CAPTION READY
job:        A - the reel carries the hook
visible:    configured preview window used before the cut
ask:        one, comment CONTRACT
hashtags:   3
search:     "client proposals" in line 3, "agency pricing" in line 5
linter:     READY
```

Nothing is posted. The user pastes it.
