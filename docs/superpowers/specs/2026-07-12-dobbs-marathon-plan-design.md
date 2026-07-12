# Dobbs training plan — London Marathon 2027 (design)

Date: 2026-07-12
Status: approved (option A)

## Goal

Publish a high-level 32-week marathon training plan page to the flyingkimura
site for Dobbs's first marathon: London Marathon 2027 (the two-day "Double",
Sat 24 / Sun 25 April 2027 — plan assumes Sunday; if she's allocated Saturday
everything shifts one day).

- Baseline: 2h07 half marathon, currently low weekly volume.
- Target: comfortable sub-4:30 (6:24/km race pace).
- Training starts Monday 14 September 2026 → exactly 32 weeks to race day.

## Constraints from user

- 4 run days + 1 strength day + 2 protected rest days (social life) = 7.
- Kilometres throughout.
- No changes to the Jekyll/markdown setup beyond one `exclude:` line.
- Page is a high-level sketch; detailed sections will later become
  interactive HTML pages under `/adhoc/` and be linked from this page.

## Deliverables

1. `_training_plans/dobbs-london-marathon-2027.md` — the plan page
   (auto-appears on the training plans index via the collection).
2. `scripts/generate_plan_charts.py` — matplotlib chart generator, run with
   `uv run`, writes SVGs to `assets/img/`. Committed for reproducibility.
3. 2 charts: (a) weekly volume across 32 weeks coloured by phase,
   (b) long-run progression with milestone annotations.
4. `_config.yml`: add `scripts` to `exclude:`.

## Plan structure (content)

Five phases over 32 weeks, cutback week roughly every 4th week, peak
~50 km/week, longest run 32 km at end of week 29 (3 weeks out):

1. Base rebuild — wks 1–8 (14 Sep – 8 Nov): 15→25 km, all easy.
2. Aerobic build — wks 9–16 (9 Nov – 3 Jan): 25→35 km, long run to ~18 km,
   strides + gentle tempo. Christmas week 15 is the cutback.
3. Marathon build — wks 17–24 (4 Jan – 28 Feb): 35→47 km, long runs 20–28 km,
   gel practice starts (runs ≥ 90 min), tune-up half race end of wk 24.
4. Peak — wks 25–29 (1 Mar – 4 Apr): up to ~50 km, two 30+ km runs,
   full race-fuel rehearsals.
5. Taper — wks 30–32 (5 Apr – 25 Apr): 38→28→race week.

Page sections: goal & paces; the 32-week shape (chart); weekly template
(4+1+2); phase summaries with time commitment; milestones table with dates;
fuelling & gel training; strength & supporting habits; planned adhoc
deep-dive links (placeholders).

## Publishing

Commit and push to main; GitHub Pages workflow deploys. Keep content and
commit messages anonymous per site policy.
