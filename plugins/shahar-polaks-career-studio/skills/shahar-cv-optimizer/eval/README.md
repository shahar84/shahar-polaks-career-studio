# Eval harness

Automates the checks in `../tests/*.md` so SKILL.md and reference edits can be
regression-tested instead of manually re-reading four checklists. This
checks configured behavioral criteria. It does not replace the manual PDF
visual QA (page breaks, clipping, font size), which still needs an actual
rendered PDF and a human eye.

## Scope

- Targets **Claude Code only**. It runs `claude -p --plugin-dir <source>`
  with `--output-format stream-json --verbose`. The CLI must be installed and
  authenticated; a marketplace installation is not needed. By default,
  `<source>` is the plugin containing this harness, not an installed copy.
- Every scenario checks the CLI's `system/init` event for the expected plugin
  name, exact resolved source path, and registered plugin skills. Missing,
  disabled, blocked, stale, or unverifiable loading is an error before any
  response can be counted as a pass. The harness never falls back to a bare
  model or a different plugin version.
- Does **not** cover Codex. Codex's non-interactive invocation, PDF/vision
  handling, and skill discovery differ enough that treating them as
  equivalent would give false confidence. Spot-check Codex manually with
  `tests/*.md`.
- Fixtures under `fixtures/` are synthetic - no real CVs or job postings.
  Keep it that way; do not replace them with real candidate data.

## Running it

```bash
cd plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/eval

# everything, using this checkout's source
python3 run_eval.py

# explicitly test another checkout of the same plugin
python3 run_eval.py --plugin-dir /absolute/path/to/shahar-polaks-career-studio

# just one category
python3 run_eval.py --category truth-policy

# just one scenario, useful while iterating on a fix
python3 run_eval.py --id job-4-ambiguous-market

# still generates model responses; skips the additional LLM-judge calls
python3 run_eval.py --skip-judge

# see what would run without spending any tokens
python3 run_eval.py --list
```

No `pip install` is needed for this harness; it uses the standard library.
Normal runs use your authenticated Claude environment and consume model usage.
Exit code is `1` for failures or errors, `2` when required judge checks were
skipped, and `0` when all automated checks completed successfully. Manual
scenarios remain listed as skipped and require separate verification.

A JSON report is written to `report.json` (path override with `--out`). It
records the local plugin name, version, resolved source path, runtime SHA-256,
file count, timestamps, scenario-file digest, requested models, and the CLI
version and actual response model reported in each initialization event. The
runtime digest includes plugin files and excludes evaluation/test data, caches,
and generated build directories. The source is hashed again after the run;
if it changed, the run exits with an error and the report is not a valid result
for either version. Do not edit the source while an evaluation is running.

The report retains the complete synthetic scenario and response for review.
It also records observed calls to the plugin's `Skill` commands and `Read`
calls for files inside its source directory. These are tool-call observations,
not proof that a read succeeded, a reference was visually inspected, or a file
was exported correctly. A loaded plugin can still fail to activate; inspect
these fields for activation scenarios instead of treating good prose alone as
proof. Other locally configured skills, plugins, and settings can still affect
a run; this harness does not create a hermetic Claude profile.

Do not replace fixtures with real candidate data or upload private evaluation
reports. The `--list` command validates source identity, scenario IDs, fixture
references, check types, and regex syntax without starting the CLI or a model.
Its successful exit means definition validation only. Automated response
checks, skill activation evidence, and rendered artifact verification are
separate results; the harness does not perform document quality checks.

## How checks work

Each automated scenario in `scenarios.json` runs one Claude call with the
explicit local source, verifies its initialization metadata, and then applies:

- **Deterministic checks** (`contains_all`, `contains_any`, `not_contains_any`,
  `regex_all`) - plain substring/regex checks against the response text. The check operation itself uses no model call, but can only catch what you
  express as a string match. The preceding response generation still uses a model.
- **An optional `judge_rubric`** - for anything that needs judgment (tone,
  "did it actually refuse convincingly," persona-appropriate framing), the
  script sends the original request and evidence, response, and rubric to a
  second `claude -p` call and
  parses a PASS/FAIL verdict. This costs an extra call per scenario and is
  the reason `--skip-judge` exists for quick iteration.

PDF scenarios exist for completeness, but `pdf-2-visual-qa` is
marked `skip_automated: true` - actual page-break/clipping/font QA requires
looking at a rendered PDF, which this harness doesn't generate or inspect.

## A known sharp edge in deterministic checks

`not_contains_any` checks that target a fabricated phrase are risky on
refusal scenarios: a compliant model very naturally quotes the fabricated
claim back while declining it ("I won't add that you led a team of 12
engineers..."), which trips a naive forbidden-string check even though the
response is correct. `truth-1` and `truth-2` were both caught doing this
during a logic dry-run (hand-written compliant/violating sample responses
run through the check functions directly, without calling `claude`) - fix
was to drop the brittle string check and lean on the `judge_rubric`, which
can tell "quoted while refusing" apart from "stated as fact." If you add a
new truth-policy scenario, default to `judge_rubric` for anything involving
a refusal, and only add a `not_contains_any` check for phrases a compliant
response has no legitimate reason to ever produce (see `job-3-israel-tone`
for that safer pattern).

## Keeping this in sync

If you change onboarding copy, the truth policy, market-tone rules, or PDF
ordering behavior in `SKILL.md` or `references/`, update the matching
scenario(s) in `scenarios.json` in the same change - the checklist in
`tests/*.md` and the scenarios here are meant to describe the same behavior
twice, once for humans and once for the harness. If they drift, this harness
stops being trustworthy.

## Harness protocol tests

Run `python3 -m unittest discover -s plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/eval -p 'test_run_eval.py'` from the repository root.
These tests use synthetic source directories and mocked CLI events. They verify
loading rejection, response parsing, invocation flags, and source fingerprints.
They do not run a model, prove plugin behavior, or validate generated documents.

## CLI compatibility references

The local source flag and JSON output format follow the official [Claude Code
CLI reference](https://code.claude.com/docs/en/cli-reference). The exact loaded
name/path and skill checks follow the [SDK plugin verification
guidance](https://code.claude.com/docs/en/agent-sdk/plugins#verifying-plugin-installation).

A session-only plugin normally takes precedence over a same-named installed
plugin, but managed settings or a disabled `@inline` entry can prevent it from
loading. See [plugin name conflicts](https://code.claude.com/docs/en/plugins/loading#name-conflicts).
The initialization check catches this rather than overriding account policy.
An older CLI that omits the required initialization fields must be updated or
tested manually; the harness will not call that result a verified evaluation.
