# Shahar Polak’s Career Studio

A skills-only plugin for Codex and Claude Code that provides truthful CV tailoring, ATS optimization, LinkedIn positioning, job-posting analysis, and interview preparation. It supports Hebrew or English working conversations and produces final professional materials in English by default.

> **Public beta:** This plugin is actively evolving. Workflows, templates, and outputs may change. Review every final document for accuracy before using it, and do not include CVs or other personal information in feedback.

## What it does

- Analyzes uploaded/pasted CVs and accessible job postings
- Matches requirements only to verified candidate evidence
- Creates ATS-safe CV content, LinkedIn recommendations, application strategy, interview preparation, spoken interview pitches, and STAR-method answers
- Uses Israel as the default market, with explicit adjustment for other markets
- Keeps Classic as the default PDF style; Crimson and Warm are late-stage options

## Quick start

Choose one path: tailor a CV for a specific job, strengthen an existing CV, improve a LinkedIn profile, or prepare for an interview. Interview preparation includes a spoken "tell me about yourself" pitch and STAR-method behavioral answers. Send a CV (PDF or text), a target role or job posting, and any achievements that must be included. Your LinkedIn link is optional. If you are unsure where to begin, reply with `1`, `2`, `3`, or `4` after activating the plugin.

## How to use Career Studio

You can write naturally in English or Hebrew. Replace bracketed text with your own details and share only verified information.

### Tailor a CV for a specific role

```text
I’m applying for [role] at [company]. Here is my CV and the job description.
Tailor my CV truthfully for this role, show my strongest matches and gaps,
and flag anything that needs confirmation.
```

### Strengthen an existing CV

```text
Review my CV for clarity, positioning, and ATS safety.
I’m targeting [role] roles in [country]. Suggest stronger wording without
inventing any achievements or metrics.
```

### Improve a LinkedIn profile

```text
Help me improve my LinkedIn profile for [target role].
Here is my current headline, About section, and experience. Keep every claim
grounded in my verified experience.
```

### Analyze a job match

```text
Compare my CV with this job posting. Build a requirement matrix showing what is
confirmed, transferable, partial, unverified, or a genuine gap. Recommend
whether and how I should apply.
```

### Prepare for an interview

```text
I have an interview for [role] at [company]. Based on my CV and this job
description, help me prepare the most likely questions, my verified evidence,
and questions I should ask the interviewer.
```

### Interview pitches and STAR answers

Ask naturally in English or Hebrew:

- “Help me answer ‘Tell me about yourself’ for this role.”
- “Review and tighten this interview pitch.”
- “Help me answer: Tell me about a time you handled a conflict.”
- “Build a STAR answer from this real experience.”

For a pitch, provide the target role and your verified career highlights. For a STAR answer, provide the exact interview question, a real event, your specific responsibility and actions, and the result. If there is no reliable metric, say so. The plugin will return a concise spoken answer, a Situation–Task–Action–Result outline, `Requires confirmation` items, and one likely follow-up question.

## Install and test

In Claude Code:

```bash
claude plugin marketplace add shahar84/shahar-polaks-career-studio
claude plugin install shahar-polaks-career-studio@shahar-polaks-career-studio
```

In Codex:

```bash
codex plugin marketplace add shahar84/shahar-polaks-career-studio
codex plugin add shahar-polaks-career-studio@shahar-polaks-career-studio
```

Then start a new task to test the skill.

## Inputs

Provide a CV (PDF or text), target role/job description or URL, optional LinkedIn link, target country, and verified achievements. Sample PDF content is never candidate evidence.

## Privacy and licence

Read [PRIVACY.md](PRIVACY.md) before use. This plugin is free for individual personal career use under the [Shahar Polak Personal Use License 1.0](LICENSE). It is source-available, not open source: redistribution, modification, commercial use, and competing use require written permission.
