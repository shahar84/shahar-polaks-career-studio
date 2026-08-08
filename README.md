# Shahar Polak’s Career Studio

Truthful, ATS-safe CV tailoring, LinkedIn positioning, job-fit analysis, and interview preparation for Hebrew- and English-speaking professionals.

> **Public beta:** Career Studio is actively evolving. Workflows, templates, and outputs may change as it is tested with real career scenarios. Review every final document for accuracy before using it, and share feedback through [shaharpolak.com](https://www.shaharpolak.com/). Do not include CVs or other personal information in feedback.

## What it does

- Turns verified experience into clear, credible career materials
- Tailors ATS-safe CV content to specific roles and job descriptions
- Improves LinkedIn positioning, application strategy, and interview preparation
- Supports Hebrew or English working conversations; final professional materials are English by default
- Uses Israel as the default market, with explicit adjustments for other markets

## Core principle

Career Studio never invents achievements, titles, qualifications, dates, metrics, or experience. It matches job requirements only to evidence the candidate has verified.

## Quick start

Start with one of four paths: tailor a CV for a specific job, strengthen an existing CV, improve a LinkedIn profile, or prepare for an interview. Send a CV (PDF or text), a target role or job posting, and any achievements that must be included. Your LinkedIn link is optional. If you are unsure where to begin, activate the plugin and reply with `1`, `2`, `3`, or `4` to choose a path.

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

Reload Claude Code, then use the career workflow with `/shahar-polaks-career-studio:shahar-cv-optimizer`.

## Privacy

CVs can contain personal information. Remove unnecessary sensitive details before sharing one. Do not include real CVs, job applications, or other personal data in this repository or its issues.

## Support

For support, use the contact details at [shaharpolak.com](https://www.shaharpolak.com/).

## License

Free for individual personal career use under the [Shahar Polak Personal Use License 1.0](LICENSE). It is source-available, not open source: redistribution, modification, commercial use, and competing use require written permission.
