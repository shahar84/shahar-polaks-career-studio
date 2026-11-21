# Shahar Polak Career Studio

<p align="center">
  <img src="plugins/shahar-polaks-career-studio/assets/career-studio-icon.png" alt="Career Studio's yellow duck mascot wearing tortoiseshell glasses" width="180" height="180">
</p>

**Turn your real experience into stronger CVs, LinkedIn profiles, and interview answers.**

An AI career coach for CV and resume review, LinkedIn profile improvement, and interview preparation. Career Studio helps you see what matters for a target role, explain your experience clearly, and prepare a personal pitch. Start with what you have, in Hebrew or English.

<p dir="rtl"><strong>יש לכם ניסיון. בואו נספר אותו כמו שצריך.</strong><br>שיפור קורות חיים, חידוד פרופיל הלינקדאין והכנה לראיונות עבודה, על בסיס הניסיון שלכם. אפשר להתחיל בעברית, גם אם קורות החיים באנגלית.</p>

[Start here](#start-with-one-task) · [See an example](#what-a-useful-result-looks-like) · [ChatGPT setup](#set-up-in-chatgpt) · [Claude Code](#install-in-claude-code) · [Codex](#install-in-codex) · [Support](#support)

**Availability:** this repository is a source-available beta for personal career use. Follow the setup instructions below to use it in a supported host. ChatGPT setup creates a private plugin; a public directory installation link is not currently provided here.

## Who this helps

Use Career Studio for a first professional CV, a career change, an experienced individual-contributor role, or an engineering leadership application. The review adapts to your target and the evidence you provide. For example, a Head of Engineering review should examine actual leadership scope, delivery, and business partnership; a junior review can draw on coursework and projects.

## Start with one task

Choose a task in your own words. There is no need to complete a questionnaire first.

### 1. CV and resume review

Share a CV or paste a section. Add a job description if you want a role-specific review.

```text
Review my CV for this role and show the three most important improvements.
```

Expect a clear assessment, practical rewrites, and a distinction between confirmed experience, transferable skills, partial matches, missing evidence, and genuine gaps. A CV without a target job can still receive a useful clarity review.

Ask for a review to get a focused assessment, or ask for a tailored CV to get a complete draft. Add a job description when you want the result aligned to a specific vacancy.

### 2. LinkedIn profile improvement

Paste your headline, About section, or experience. Include the target role when you know it.

```text
Improve my LinkedIn headline and About section for my target role.
```

Expect a more focused headline, an About section grounded in your experience, and consistent positioning across LinkedIn and your CV. Browser review is available when the host and connection support it.

### 3. Interview preparation and STAR answers

Share an existing introduction or a few career highlights. For a behavioral question, start with a real event.

```text
Help me answer "Tell me about yourself" in 90 seconds.
```

Expect a spoken introduction, a useful rehearsal prompt, or a Situation, Task, Action, Result answer. Details already shared during CV work carry forward into interview preparation.

<details>
<summary><strong>אפשר להתחיל גם ככה, בעברית</strong></summary>

```text
אלה קורות החיים שלי. מה שלושת הדברים שהכי כדאי לשפר?
```

```text
אני מכוון לתפקיד פיתוח בקאנד. תעזור לי לחדד את הכותרת וה-About בלינקדאין.
```

```text
יש לי ראיון. איך אני עונה על "ספר לי על עצמך" בלי לספר את כל קורות החיים?
```

</details>

## What a useful result looks like

**Fictional demonstration, not a customer result.** The sample candidate, Alex, says they replaced a nightly reporting cron job with an Airflow DAG. Their measured run time changed from six hours to 40 minutes.

> **Before:** Responsible for data pipelines.
>
> **After:** Migrated a nightly reporting job to an Airflow DAG, reducing runtime from six hours to forty minutes.

The stronger version uses facts supplied in the example. It does not add a cost saving, team size, or revenue claim. If the target role prefers Kafka and Alex has only used RabbitMQ, the review labels that experience as transferable rather than claiming production Kafka experience.

See the [complete fictional CV-to-pitch demonstration](plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/references/first-result-demo.md) for the source facts, job match, LinkedIn headline, and interview introduction.

Career Studio is designed to flag details that need confirmation and keep them outside candidate-ready copy. Review the final wording before using it. AI output and third-party information can contain errors; the plugin does not guarantee ATS acceptance, interviews, or job offers.

## What is included

- **Three skills:** a short getting-started workflow, CV and LinkedIn optimization, and interview pitches and STAR answers.
- **Role-specific analysis:** evidence inventory, job-match review, career narrative, and practical next steps.
- **Reusable templates:** [CV content and layout guides](plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/templates/template-index.md), LinkedIn profile sections, application strategy, and interview preparation. The workflow selects and reads the relevant template before creating the requested material.
- **Editable CV files:** a shared renderer creates Classic, Crimson, and Warm DOCX files from supported candidate content, with PDF conversion when LibreOffice is available. Classic is the default; you can request another style directly. The assistant identifies the template it used outside your CV and checks the finished pages. The reference PDFs remain visual examples, never candidate evidence.
- **Hebrew documents:** native right-to-left layout when requested, with mixed Hebrew/English contact details, dates, and technology names checked in the final output.
- **Interview practice:** role-specific preparation, evidence-based stories, questions for the employer, and mock interviews one question at a time.
- **Browser guidance:** requested LinkedIn profiles, job pages, and company research, with source and access limitations made explicit.

The working conversation can be Hebrew or English. Final CV and LinkedIn materials default to English unless you request another language. Interview pitches follow your language. Israel is the default job market unless your context indicates another country.

### Ask for a finished document

```text
Create my CV in the Classic template and give me an editable Word file and a PDF.
```

```text
תכין לי קורות חיים בעברית בתבנית Warm, בקובץ Word וב-PDF.
```

The assistant prepares the content and runs the [document export workflow](plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/references/document-export.md) when the host provides Python and document tools. DOCX creation uses `python-docx`; PDF conversion uses LibreOffice. If a requested exporter is unavailable, it delivers the supported format and identifies what remains. Fonts can differ from the design references, and each finished file still needs visual and text review.

## Set up in ChatGPT

From a local copy of this repository, build the package:

```bash
python3 -m pip install -r scripts/requirements-validation.txt
python3 scripts/package_plugin.py
```

The builder writes `dist/shahar-polaks-career-studio-<version>.zip`. Give that archive to ChatGPT's Plugin Creator and ask it to create your private Career Studio plugin. Open the returned plugin link, enable it if prompted, and start with one of the tasks above.

The package does not require a separate author-operated server or API key. It declares Browser as a dependency. Access to Plugin Creator, Browser, and document tools depends on your host and account. Pasted text also works when a page or document cannot be read.

Repository updates do not automatically update an installed ChatGPT plugin. Rebuild the archive and ask Plugin Creator to update your existing plugin, preserving its identity.

### Browser-assisted reviews

For example:

```text
Review my LinkedIn profile in the browser for this target role. Suggest changes
to my headline, About section, and experience, and flag facts to confirm.
```

Available access depends on the host, mode, connection, and tools in your conversation. Career Studio follows those tools' current capabilities, reports the sections it actually read, and keeps profile claims separate from confirmed candidate evidence. If the requested page cannot be accessed, paste the relevant text to continue. Complete any necessary sign-in through the host's supported browser flow.

A review produces suggested edits. Saving profile changes, sending messages, uploading a CV, or submitting an application requires a specific user request and the host's applicable approvals.

The Browser dependency is preserved for compatible private account or workspace installations. Public directory submission requires separate preparation. See the [launch preparation notes](docs/career-studio-launch.md) for sharing options, public listing copy, and the remaining publication steps.

## Install in Claude Code

```bash
claude plugin marketplace add shahar84/shahar-polaks-career-studio
claude plugin install shahar-polaks-career-studio@shahar-polaks-career-studio
```

Use the host's current plugin activation or reload flow, then describe the task. The package includes `career-studio-start`, `shahar-cv-optimizer`, and `interview-pitch` skills.

## Install in Codex

```bash
codex plugin marketplace add shahar84/shahar-polaks-career-studio
codex plugin add shahar-polaks-career-studio@shahar-polaks-career-studio
```

Start a new task with the plugin enabled. Browser access and document export vary by host, mode, and connected tools. Check the [changelog](plugins/shahar-polaks-career-studio/CHANGELOG.md) for the validation actually performed for each release.

## Support

For a bug or feature idea, [open a GitHub issue](https://github.com/shahar84/shahar-polaks-career-studio/issues). Include the plugin version, host, task, expected behavior, and a short redacted example. GitHub issues are public: leave out CVs, contact details, application records, and credentials.

Read the [support guide](plugins/shahar-polaks-career-studio/SUPPORT.md) for troubleshooting and feedback instructions, and the [privacy information](plugins/shahar-polaks-career-studio/PRIVACY.md) before sharing career materials. General contact is available through [Shahar's website](https://www.shaharpolak.com/).

## Development and license

The [evaluation harness](plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/eval/README.md) documents how to check model behavior against the local plugin source, with source/version evidence recorded for each run. Package validation, renderer checks, and model evaluation are separate checks; passing one does not establish the others.

Free for individual personal career use under the [Shahar Polak Personal Use License 1.0](LICENSE). Host subscriptions or services may have their own requirements. This is source-available software, not an open-source license: redistribution, modification, commercial use, and competing use require written permission.
