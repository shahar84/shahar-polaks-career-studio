# Shahar Polak’s Career Studio

<p align="center">
  <img src="assets/shahar-career-studio-logo.jpeg" alt="Shahar Polak’s Career Studio yellow duck mascot wearing tortoiseshell glasses" width="360">
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Personal%20Use%201.0-blue.svg"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-public%20beta-orange.svg">
  <a href="#install-in-claude-code"><img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-supported-6e56cf.svg"></a>
  <a href="#install-in-codex"><img alt="Codex" src="https://img.shields.io/badge/Codex-experimental-lightgrey.svg"></a>
</p>

**Career Studio tailors your CV, LinkedIn profile, and interview prep to a specific job — without inventing a single achievement to get there.**

ATS-safe CV tailoring, LinkedIn positioning, job-fit analysis, and interview preparation, in Hebrew or English. Free for personal job-search use.

<p dir="rtl"><strong>אפשר לעבוד עם Career Studio בעברית מהמילה הראשונה ועד המסמך הסופי</strong> — שלחו קורות חיים ומשרת יעד, ותארו מה אתם צריכים במילים שלכם. הכלל היחיד שלא מתגמש: שום הישג, תפקיד או מספר לא מומצאים בשבילכם.</p>

<p align="center">
  <a href="#install-in-claude-code">Install (Claude Code)</a> ·
  <a href="#install-in-codex">Install (Codex)</a> ·
  <a href="#what-you-can-do">What you can do</a> ·
  <a href="#what-the-output-looks-like">Sample output</a> ·
  <a href="#how-to-use-career-studio">Usage examples</a> ·
  <a href="#support">Support</a>
</p>

> **Public beta.** Workflows, templates, and outputs may still change as Career Studio gets tested on real career scenarios. Review every final document before you use it, and send feedback via [shaharpolak.com](https://www.shaharpolak.com/) — please don't include CVs or other personal information when you do.

## Core principle

Career Studio never invents achievements, titles, qualifications, dates, metrics, or experience. It only writes what your evidence actually supports — where evidence is missing, it says so and asks, instead of guessing. Everything else in this README is detail; this is the rule that doesn't bend.

<details>
<summary><strong>What that means in practice</strong></summary>

If your CV shows a reporting job that went from 6 hours to 40 minutes after a migration, Career Studio writes:

> "Migrated a legacy reporting job to an Airflow DAG, cutting run time from 6 hours to 40 minutes."

It will not add "cut cloud costs by 40%" just because that sounds stronger — no such number exists in your evidence, so it doesn't show up in your CV either.

</details>

## What you can do

Describe what you need in plain English or Hebrew — Career Studio figures out the right workflow. If you're not sure where to start, say so and it will suggest a starting path.

**CV & job-fit**

- Tailor your CV for a specific job
- Strengthen an existing CV
- Improve your LinkedIn profile
- Analyze how well you match a job posting — confirmed, transferable, partial, unverified, or a genuine gap
- Prepare for an interview: likely questions, your verified evidence, questions to ask back

**Interview pitches**

- Build or sharpen a spoken "tell me about yourself" pitch, or a STAR-method answer to a behavioral question

## What the output looks like

A job-match analysis builds a requirement matrix from your actual evidence (illustrative example):

| Job requirement | Verdict | Why |
| --- | --- | --- |
| 5+ years backend development | ✅ Confirmed | 7 years across Python and Node.js roles in your CV |
| Kafka in production | 🔄 Transferable | You ran RabbitMQ at scale; the concepts carry over, the tool doesn't |
| Team leadership | ⚠️ Partial | You mentored three engineers, but never held a formal management role |
| Kubernetes | ❓ Unverified | Listed in your skills with no supporting project — Career Studio asks before using it |
| Go | ❌ Gap | Nowhere in your evidence; flagged honestly, not papered over |

CV tailoring works the same way — sharper wording, but only from facts you've confirmed:

> **Before:** "Responsible for data pipelines."
>
> **After:** "Migrated a legacy reporting job to an Airflow DAG, cutting run time from 6 hours to 40 minutes."

## Install in Claude Code

Add the marketplace and install the plugin from your terminal:

```bash
claude plugin marketplace add shahar84/shahar-polaks-career-studio
claude plugin install shahar-polaks-career-studio@shahar-polaks-career-studio
```

Reload Claude Code, then just describe what you need — or invoke a skill directly: `/shahar-polaks-career-studio:shahar-cv-optimizer` for CV and job-fit work, `/shahar-polaks-career-studio:interview-pitch` for interview pitches and STAR answers.

## Install in Codex

```bash
codex plugin marketplace add shahar84/shahar-polaks-career-studio
codex plugin add shahar-polaks-career-studio@shahar-polaks-career-studio
```

Then start a new task with the plugin enabled.

> Career Studio is developed and tested primarily against Claude Code. Codex support works, but document handling (scanned PDFs, generated PDFs) can behave less consistently — if something feels off, try pasting text instead of a scan.

## What to have ready

Send a CV (PDF or text), a target role or job posting, and any achievements you want included. Add your target country if it isn't Israel, and your LinkedIn link if you have one and want it reviewed. That's it — everything else happens in conversation.

## How to use Career Studio

Write naturally in English or Hebrew, and replace the bracketed text with your own details. The two most common flows:

**Tailor a CV for a specific role**

```text
I’m applying for [role] at [company]. Here is my CV and the job description.
Show my strongest matches and gaps, and flag anything that needs confirmation.
```

**Analyze a job match**

```text
Compare my CV with this job posting. Build a requirement matrix showing what is
confirmed, transferable, partial, unverified, or a genuine gap. Recommend
whether and how I should apply.
```

More examples — click to expand:

<details>
<summary><strong>Strengthen an existing CV</strong></summary>

```text
Review my CV for clarity, positioning, and ATS safety.
I’m targeting [role] roles in [country]. Suggest stronger wording.
```

</details>

<details>
<summary><strong>Improve a LinkedIn profile</strong></summary>

```text
Help me improve my LinkedIn profile for [target role].
Here is my current headline, About section, and experience.
```

</details>

<details>
<summary><strong>Prepare for an interview</strong></summary>

```text
I have an interview for [role] at [company]. Based on my CV and this job
description, help me prepare the most likely questions, my verified evidence,
and questions I should ask the interviewer.
```

</details>

<details>
<summary><strong>Interview pitches and STAR answers</strong></summary>

Ask naturally, in English or Hebrew:

- "Help me answer 'Tell me about yourself' for this role."
- "Review and tighten this interview pitch."
- "Help me answer: Tell me about a time you handled a conflict."
- "Build a STAR answer from this real experience."

For a pitch, share the target role plus your verified career highlights. For a STAR answer, share the exact interview question, a real example, your specific responsibility and actions, and the result — if there's no reliable metric, say so; Career Studio will use a truthful qualitative result rather than invent a number.

You'll get a concise, spoken answer in your language. STAR requests also return a Situation–Task–Action–Result outline, items that need your confirmation, and one likely follow-up question to prepare for.

</details>

## Privacy

CVs can contain personal information. Remove unnecessary sensitive details before sharing one. Do not include real CVs, job applications, or other personal data in this repository or its issues.

## Support

Found a bug or have a feature idea? [Open a GitHub issue](https://github.com/shahar84/shahar-polaks-career-studio/issues) — just leave CVs and other personal data out of it. For anything else, reach out via [shaharpolak.com](https://www.shaharpolak.com/).

**Model compatibility.** Career Studio is a set of instructions, not code, so its behavior depends on how the underlying model interprets it. See [`CHANGELOG.md`](plugins/shahar-polaks-career-studio/CHANGELOG.md) for which model each release was validated against, and the [eval harness](plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/eval/README.md) if you want to re-check behavior yourself after a model or CLI upgrade.

## License

Free for individual personal career use under the [Shahar Polak Personal Use License 1.0](LICENSE). It is source-available, not open source: redistribution, modification, commercial use, and competing use require written permission.
