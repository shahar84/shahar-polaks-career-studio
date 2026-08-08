# Shahar Polak’s Career Studio

<p align="center">
  <img src="assets/shahar-career-studio-logo.jpeg" alt="Shahar Polak’s Career Studio yellow duck mascot wearing tortoiseshell glasses" width="360">
</p>

Truthful, ATS-safe CV tailoring, LinkedIn positioning, job-fit analysis, and interview preparation for Hebrew- and English-speaking professionals.

> **Public beta:** Career Studio is actively evolving. Workflows, templates, and outputs may change as it is tested with real career scenarios. Review every final document for accuracy before using it, and share feedback through [shaharpolak.com](https://www.shaharpolak.com/). Do not include CVs or other personal information in feedback.

## What it does

- Turns verified experience into clear, credible career materials
- Tailors ATS-safe CV content to specific roles and job descriptions
- Improves LinkedIn positioning, application strategy, interview pitches, and STAR-method behavioral answers
- Supports Hebrew or English working conversations; final professional materials are English by default
- Uses Israel as the default market, with explicit adjustments for other markets

## Core principle

Career Studio never invents achievements, titles, qualifications, dates, metrics, or experience. It matches job requirements only to evidence the candidate has verified.

## Quick start

Start with one of four paths: tailor a CV for a specific job, strengthen an existing CV, improve a LinkedIn profile, or prepare for an interview. Interview preparation includes a spoken "tell me about yourself" pitch and STAR-method behavioral answers. Send a CV (PDF or text), a target role or job posting, and any achievements that must be included. Your LinkedIn link is optional. If you are unsure where to begin, activate the plugin and reply with `1`, `2`, `3`, or `4` to choose a path.

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

Use the interview-pitch skill naturally in English or Hebrew:

- “Help me answer ‘Tell me about yourself’ for this role.”
- “Review and tighten this interview pitch.”
- “Help me answer: Tell me about a time you handled a conflict.”
- “Build a STAR answer from this real experience.”

For a pitch, share the target role plus your verified career highlights. For a STAR answer, share the exact interview question, a real example, your specific responsibility and actions, and the result. If there is no reliable metric, say so—the plugin will use a truthful qualitative result rather than inventing a number.

You will receive a concise, spoken answer in your language. STAR requests also return a Situation–Task–Action–Result outline, items that require confirmation, and one likely follow-up question to prepare for.

## Install in Codex

Add this repository as a Codex plugin marketplace, install `shahar-polaks-career-studio`, then start a new task with the plugin enabled.

```bash
codex plugin marketplace add shahar84/shahar-polaks-career-studio
```

## Install in Claude Code

Add the marketplace and install the plugin from a terminal where Claude Code is authenticated to GitHub:

```bash
claude plugin marketplace add shahar84/shahar-polaks-career-studio
claude plugin install shahar-polaks-career-studio@shahar-polaks-career-studio
```

Reload Claude Code, then use `/shahar-polaks-career-studio:shahar-cv-optimizer` for CV and job-fit work or `/shahar-polaks-career-studio:interview-pitch` for interview pitches and STAR answers.

## Privacy

CVs can contain personal information. Remove unnecessary sensitive details before sharing one. Do not include real CVs, job applications, or other personal data in this repository or its issues.

## Support

For support, use the contact details at [shaharpolak.com](https://www.shaharpolak.com/).

## License

Free for individual personal career use under the [Shahar Polak Personal Use License 1.0](LICENSE). It is source-available, not open source: redistribution, modification, commercial use, and competing use require written permission.
