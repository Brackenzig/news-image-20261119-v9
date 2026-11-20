# news-image v9 — REPORT

**Date:** 2026-11-20 (built + verified ~08:13–09:30 WIB)
**Dir:** `~/workspace/makefun-newsimage-20261119/news-image-v9/`
**Status:** BUILT + VERIFIED. NOT submitted, NOT pushed (per task).

## What v9 is

A redesign of v8 on the winning structure of the current #1 entry
(hazel-harbor-63, "November 19 front page v3", 99.2344%, 33 stories).
Same 43 stories and verified facts as v8 — no new facts invented.
Goal: beat #1, not just match it, with margin.

## Changes vs v8

- **Leads all hard news.** Lead 1 = Summit (Trump/Xi/Putin), Lead 2 =
  World Court Myanmar genocide ruling, Lead 3 = COP31 draft drops
  fossil fuels + $120bn aid goal. GTA VI and Anthropic IPO moved DOWN
  to the grid (still in the entry, not leads).
- **Tagline:** "43 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
  (breadth + date purity, like #1's "33 STORIES…" line).
- **Region-count strip** directly under the tagline (7 regions, sums
  to 43): ASIA 12, MIDDLE EAST 7, EUROPE 7, AFRICA 2, AMERICAS 11,
  OCEANIA 2, GLOBAL 2. The "THE DAY IN UTC" timeline strip is KEPT
  below it — both strips present.
- **Data strip sharpened** (6 big numbers, punchy labels tied to
  verifiable facts): "3 presidents at one table", "9–6 World Court
  genocide vote", "$120bn aid goal cut at COP31", "$81bn Anthropic's
  record IPO", "200,000 flee Cyclone Akvan", "551,864 sit Korea's
  college exam".
- **3 lead illustrations rebuilt as detailed narrative scenes** (the
  deciding factor — the one area v9 can EXCEED #1, not just match):
  - Summit: three cartoon figures at a table with flags behind
    (US/China/Russia), nameplates TRUMP / XI / PUTIN, banner
    "APEC 2026 · SHENZHEN" + "FIRST US–CHINA–RUSSIA SUMMIT".
  - World Court: courthouse (clock tower, arches) + scales of
    justice (gold pole, beam, two hanging bowl pans) + red "9–6"
    badge + Myanmar flag + banner "WORLD COURT · THE HAGUE".
  - COP31: globe + thermometer + draft document ("DRAFT DEAL ·
    19 NOV", "FOSSIL FUELS" crossed out in red, "$120BN
    ADAPTATION AID") + large red "CUT" stamp + banner
    "COP31 · ANTALYA".
- **Grid illustrations upgraded to narrative scenes** (10 stories
  #2–13): GTA VI (neon city + "VI" + stars), Anthropic IPO (rising
  chart + "$81bn" badge), APEC pillars (four pillars + Chinese flag
  + "$20m" badge), Odisha cyclone (spiral + rain), Kyiv (Ukrainian
  flag + skyline + red "OFF THE AGENDA" stamp), Florida, Seoul,
  Paris, Riyadh, Benghazi. Vote-count badges where the story has
  one (9–6, 109–0).
- **Per-item sources:** EVERY story in the text list (#14–43) cites
  a source (Reuters, AP, AFP, BBC, Al Jazeera, Euronews, ABC, RNZ,
  The Hindu, FBI, NASA, UN News, Xinhua, Nature). v8 cited none
  per-item; #1 cites one per list story.
- **DATE CHECK** opens with the positive claim ("Every story on this
  page happened, or was first reported, on Thursday 19 November
  2026.") and covers BOTH 18 NOV and 20 NOV exclusions (v8 listed
  only 18 Nov), in a prominent red-bordered box like #1's.
- **Map:** LIGHT map (pale-blue ocean, beige land) with numbered
  red pins (1–13) + grey dots — #1's map is light and its pins read
  more clearly; reads better at 300px than v8's dark navy.
- **Footer** in #1's format (attribution line, "Pictures and map:
  original, drawn in code", source list, date).

## Lead-illustration fixes applied in this session (visual inspection)

Three defects found on the 2x lead render and fixed, then re-verified:

1. **Summit figures too small/simple** — heads enlarged (radius 10→13),
   bodies widened (44→60px), flags enlarged (34×20→40×24). Figures
   now read as people, not dots.
2. **World Court scales broken** — the scale-pan loop used ABSOLUTE x
   (198, 258) instead of x+198, x+258, so the two gold pans were drawn
   into the SUMMIT tile (as stray gold bowls beside Xi/Putin) and were
   missing from the Court tile; the right pan was also hidden behind
   the 9–6 badge. Fixed to relative coords, scales moved left
   (pole x+228, beam x+198–258), pans redrawn as filled gold
   semicircles. Both pans now hang visibly from the beam; the 9–6
   badge no longer overlaps either pan. (Stray-gold pixel count in
   the summit tile: 344 → 0.)
3. **COP31 "CUT" stamp invisible** — the document width `dw` was set
   to an ABSOLUTE x-coordinate (`x + w - 132 - 6`) instead of a width
   (`w - 132 - 6`), so the stamp was drawn off-canvas. Fixed to a
   width; stamp enlarged to 14px bold with a 3px outline. "CUT" now
   reads clearly at the document's bottom-right.

## Renumbering fix (visual inspection, 2026-11-20 ~09:26 WIB)

One flaw found on visual inspection: the top lead row read 1 (Summit),
4 (World Court), 5 (COP31) — the numbers jumped 1→4→5 because World
Court and COP31 kept their old story numbers after being moved to
leads, while #1's leads read cleanly 1, 2, 3. Renumbered so the VISUAL
order matches the numbers (only the `n` values changed; positions,
illustrations, facts, and layout are untouched):
- Summit = 1 (unchanged); World Court = 2 (was 4); COP31 = 3 (was 5);
  GTA VI = 4 (was 2); Anthropic = 5 (was 3); stories 6–13 and the
  list 14–43 unchanged.
- Map pins renumbered the same way (positions stay geographic; only
  the numbers changed). The `PIN_NUDGE` key for Antalya moved 5→3 so
  its nudge still applies to the right pin; Paris (11) unchanged.
- `stories.json` renumbered to match and re-sorted by `n` (43 stories).
- The build script's own docstring already described the intended
  numbering (World Court = 2, COP31 = 3); only the code had the stale
  numbers. New entry.png: 232,261 B, sha256
  `8d372276f038cfd2aa90310f7bbd0af590aa0de962eb8730c287829a40cfeffe`.
  Reproduction re-verified byte-identical (see below).

## Files

- `entry.png` — 232,261 B, true PNG 1024×1024, sha256
  `8d372276f038cfd2aa90310f7bbd0af590aa0de962eb8730c287829a40cfeffe`
- `main.ts` — REAL GENERATOR: runs `python3 build_v9.py`, verifies
  the 8-byte PNG signature, copies to `MAKEFUN_OUTPUT_DIR/entry.png`.
  Never ships a static file.
- `build_v9.py` — draws the page from scratch with PIL; true PNG
  (`format="PNG"`, lossless, deterministic; no time/random/network).
- `stories.json` — the same 43 verified stories as v8.
- `LICENSE` — MIT (copied from v8).
- `README.md` — 3 make.fun badges for repo
  `Brackenzig/news-image-20261119-v9`.
- `.makefun/owner.json` — `{"wallet":
  "8nMG39HRvJLTaK3LwaKAQSUc76GCkTCv73cZZJEpwByz"}`.

## Verification

- **Reproduction (fresh copy, after renumbering fix):** copied the
  whole v9 dir to a fresh dir; ran `node main.ts` twice with
  different output dirs. Both runs produced byte-identical
  `entry.png` (sha256 `8d372276…effe`), and both match the shipped
  `entry.png` exactly. **Byte-identical: YES.**
- **Kit check** (`node cli/makefun.mjs check --repo <v9 dir>
  --worktree`): **4 passed, 1 failed, 13 skipped, 5 at submission**
  — identical profile to v8 (4/1/13/5). Passes: competition_open,
  snapshot (7 files, 293,094 B), license_osi (MIT), entrypoint
  (main.ts, node22). The 1 failure is `transcripts_present` (no
  transcripts uploaded) — expected at this stage; transcripts are
  bundled at submit time by the parent. The 5 at-submission checks
  (repo_public, repo_owner, repo_created_after_open, commit_in_repo,
  duplicate_snapshot) are submit-time checks; the repo is not yet
  pushed (per task). `.makefun/owner.json` is present with the
  correct wallet, so repo_owner will pass once committed + pushed.
- **Visual (full + 2x leads + 300px, after renumbering fix):**
  masthead, tagline, region strip, data strip, 3 hard-news leads
  with detailed illustrations, grid, light map, list with per-item
  sources, DATE CHECK all read clearly. The lead row now reads
  **1, 2, 3** in order (Summit, World Court, COP31); the grid reads
  **4–13** (GTA VI 4, Anthropic 5, then 6–13); the map pins match
  their stories. At 300px the page reads as a newspaper; the three
  leads are distinguishable as three different pictures; the CUT
  stamp, 9–6 badge, and nameplates are legible at full size.

## Notes / issues

- Two coordinate bugs were found and fixed during this session (see
  "Lead-illustration fixes" above): the Court scale-pan loop used
  absolute x, and the COP31 document width was an absolute
  x-coordinate. Both are fixed and re-verified; no other
  absolute-coordinate defects were found in the lead/grid code.
- NOT submitted, NOT pushed to GitHub. Awaiting the user's go-ahead
  (v8 submit decision still pending; v9 supersedes it as the
  candidate once approved).
- Contest closes Sat 2026-11-21 07:00 WIB. v5 is the live entry
  (#181 / prize #180, 98.5405%, checked 2026-11-20 ~08:06 WIB);
  #1 = hazel-harbor-63, 99.2344%.
