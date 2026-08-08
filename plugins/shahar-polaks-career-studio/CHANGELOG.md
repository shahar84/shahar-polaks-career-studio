# Changelog

## 0.5.0 — 2026-08-08

- Added an automated eval harness (`skills/shahar-cv-optimizer/eval/`) that runs the scenarios behind `tests/*.md` against a live `claude -p` call and checks the output deterministically and, where judgment is needed, via an LLM-judge rubric. Not yet run end-to-end against a live model in this environment — run it locally (`python3 eval/run_eval.py`) and note the result here before relying on it as a regression gate.
- Added `references/worked-examples.md`: calibrated before/after examples for CV bullets (with and without a verified metric), gap labeling, and LinkedIn headline/About content, linked from `SKILL.md` and the relevant templates.
- Added `references/document-input-handling.md`: attempt-then-disclose handling for scanned/photographed CVs — attempt to read visually, never claim guaranteed-accurate extraction or "OCR," flag transcribed specifics as needing confirmation, fall back to asking for pasted text.
- Added a "Model compatibility" note to the repo README pointing at the eval harness as the way to re-validate behavior after a model or CLI upgrade.

## 0.4.2 — 2026-08-08

- Added copy-and-paste usage examples for every Career Studio workflow to both READMEs.

## 0.4.1 — 2026-08-08

- Added practical interview-pitch and STAR usage guidance to both READMEs.
- Expanded behavioral-interview test coverage for Hebrew and mixed-outcome stories.

## 0.4.0 — 2026-08-08

- Added the `interview-pitch` skill for truthful spoken interview pitches.
- Added STAR-method behavioral-interview answers with verified Situation, Task, Action, and Result evidence.

## 0.3.2 — 2026-08-08

- Added adaptive English and Hebrew onboarding with four clear starting paths.

## 0.3.1 — 2026-08-08

- Marked the public release as beta across documentation and plugin listings.

## 0.3.0 — 2026-08-08

- Released the plugin publicly under the Shahar Polak Personal Use License 1.0.

## 0.2.1 — 2026-08-06

- Added Claude Code display and license metadata.
- Clarified the plugin README supports both Codex and Claude Code.

## 0.2.0 — 2026-08-06

- Added Claude Code marketplace and plugin packaging.

## Unreleased

- Renamed the plugin to Shahar Polak’s Career Studio.

## 0.1.0 — 2026-08-05

- Initial skills-only release.
