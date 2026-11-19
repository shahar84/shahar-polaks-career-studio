# Changelog

## 0.7.1 - 2026-11-19

- Preserved account-provided author metadata in the private release while keeping account contact details out of the public repository.

## 0.7.0 - 2026-11-19

- Declared the verified Browser app dependency for the private ChatGPT plugin.
- Added shared browser guidance for LinkedIn reviews, job postings, and interview research, including mode-aware access, source attribution, and evidence checks.
- Kept profile edits, messages, CV uploads, and applications tied to the user's specific request and existing host approvals.
- Updated package validation and archive generation to preserve and verify the Browser dependency.
- Documented connection requirements and private-package scope. Live LinkedIn navigation has not been exercised as part of this release.

## 0.6.0 - 2026-11-19

- Added an Agent Plugins 1.0 manifest for private ChatGPT installation while preserving the two existing career workflows and their support files.
- Synchronized the portable, Codex, and Claude Code package versions and display name; shortened the listing subtitle to meet ChatGPT's metadata limit.
- Included the existing duck logo inside the plugin package.
- Added a repeatable archive builder and validation for the portable manifest, compatibility metadata, assets, and final ZIP contents.
- Added ChatGPT installation and update instructions and a package-build step in CI.
- Validation covers packaging and metadata. The career instructions are unchanged; live model behavior and document exports have not been newly evaluated in this release.

## 0.5.1 — 2026-08-08

- Restructured the repo README for scannability: badges and a quick-nav bar up top, install instructions moved above the usage examples with Claude Code leading (Codex flagged as less consistent for document handling), the six usage examples collapsed into `<details>` blocks, and a single concrete before/after example replacing the repeated "truthfully" wording throughout. Trimmed "Model compatibility" to a pointer at CHANGELOG/eval docs instead of full detail in the README. Note: `plugins/shahar-polaks-career-studio/README.md` was not updated to match and is now noticeably out of sync with the root README's structure — worth reconciling in a follow-up.

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
