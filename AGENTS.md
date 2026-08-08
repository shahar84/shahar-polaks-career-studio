# Repository workflow

- Treat `/Users/shahar/dev/shahar-polaks-career-studio` as the canonical local checkout.
- For every new change, start from an up-to-date `main` and create a descriptive feature branch named `agent/<short-description>`.
- Do not make commits directly on `main`.
- Before staging, inspect `git status -sb` and stage only files that belong to the requested change.
- Push feature branches and open a draft pull request for review before merging to `main`.
- This checkout may be used concurrently by Claude Code. Preserve unrelated modified or untracked files, avoid reset/clean/stash operations, and do not switch branches unless the requested work requires it.
