# Eval harness

Automates the checks in `../tests/*.md` so SKILL.md and reference edits can be
regression-tested instead of manually re-reading four checklists. This
replaces manual QA for most scenarios — it does not replace the manual PDF
visual QA (page breaks, clipping, font size), which still needs an actual
rendered PDF and a human eye.

## Scope

- Targets **Claude Code only**. It shells out to `claude -p`, which requires
  the `claude` CLI installed, authenticated, and the
  `shahar-polaks-career-studio` plugin installed so the skill actually
  triggers (see the repo README's "Install in Claude Code" section).
- Does **not** cover Codex. Codex's non-interactive invocation, PDF/vision
  handling, and skill discovery differ enough that treating them as
  equivalent would give false confidence. Spot-check Codex manually with
  `tests/*.md`.
- Fixtures under `fixtures/` are synthetic — no real CVs or job postings.
  Keep it that way; do not replace them with real candidate data.

## Running it

```bash
cd plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/eval

# everything
python3 run_eval.py

# just one category
python3 run_eval.py --category truth-policy

# just one scenario, useful while iterating on a fix
python3 run_eval.py --id job-4-ambiguous-market

# deterministic checks only — faster and cheaper, skips the LLM-judge calls
python3 run_eval.py --skip-judge

# see what would run without spending any tokens
python3 run_eval.py --list
```

No `pip install` needed — standard library only. Exit code is `1` if
anything failed or errored, `0` otherwise, so it's usable as a pre-release
gate (e.g. run before bumping the plugin version and publishing).

A JSON report is written to `report.json` (path override with `--out`).

## How checks work

Each scenario in `scenarios.json` runs one `claude -p` call and then applies:

- **Deterministic checks** (`contains_all`, `contains_any`, `not_contains_any`,
  `regex_all`) — plain substring/regex checks against the response text. Fast,
  free, no ambiguity, but can only catch what you can phrase as a string
  match.
- **An optional `judge_rubric`** — for anything that needs judgment (tone,
  "did it actually refuse convincingly," persona-appropriate framing), the
  script sends the response plus the rubric to a second `claude -p` call and
  parses a PASS/FAIL verdict. This costs an extra call per scenario and is
  the reason `--skip-judge` exists for quick iteration.

Four `pdf-output` scenarios exist for completeness, but `pdf-2-visual-qa` is
marked `skip_automated: true` — actual page-break/clipping/font QA requires
looking at a rendered PDF, which this harness doesn't generate or inspect.

## A known sharp edge in deterministic checks

`not_contains_any` checks that target a fabricated phrase are risky on
refusal scenarios: a compliant model very naturally quotes the fabricated
claim back while declining it ("I won't add that you led a team of 12
engineers..."), which trips a naive forbidden-string check even though the
response is correct. `truth-1` and `truth-2` were both caught doing this
during a logic dry-run (hand-written compliant/violating sample responses
run through the check functions directly, without calling `claude`) — fix
was to drop the brittle string check and lean on the `judge_rubric`, which
can tell "quoted while refusing" apart from "stated as fact." If you add a
new truth-policy scenario, default to `judge_rubric` for anything involving
a refusal, and only add a `not_contains_any` check for phrases a compliant
response has no legitimate reason to ever produce (see `job-3-israel-tone`
for that safer pattern).

## Keeping this in sync

If you change onboarding copy, the truth policy, market-tone rules, or PDF
ordering behavior in `SKILL.md` or `references/`, update the matching
scenario(s) in `scenarios.json` in the same change — the checklist in
`tests/*.md` and the scenarios here are meant to describe the same behavior
twice, once for humans and once for the harness. If they drift, this harness
stops being trustworthy.
