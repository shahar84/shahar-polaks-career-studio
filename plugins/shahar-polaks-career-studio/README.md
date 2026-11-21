# Shahar Polak Career Studio

**AI CV & Interview Coach**

Build an English CV tailored to a specific job through focused questions about your real experience. Career Studio reads the vacancy, identifies the evidence that matters, asks about the missing details, and turns your answers into the CV. Discuss in Hebrew or English; the finished CV defaults to English.

<p dir="rtl"><strong>מתחילים מהמשרה, מגלים את הניסיון הרלוונטי, ובונים קורות חיים באנגלית.</strong><br>אפשר לענות בעברית ולהתחיל גם בלי קורות חיים מוכנים.</p>

## Start with what you have

Choose a task in your own words:

1. **A tailored English CV:** share the job posting and your CV or rough background. The workflow asks the relevant unanswered questions before writing.
2. **LinkedIn:** paste a headline, About section, or experience. A requested browser review also works when the host and connection support it.
3. **Interview preparation:** share an introduction, career highlights, or a real story for a behavioral question.

Try one of these:

```text
Help me build an English CV for this role. Ask focused questions about the relevant experience missing from my current CV.
```

```text
Improve my LinkedIn headline and About section for my target role.
```

```text
Help me answer "Tell me about yourself" in 90 seconds.
```

For CV creation, the first result may be a short observation about the vacancy and one or two questions about your relevant experience. Each answer shapes the next question or the resulting CV. Once the evidence is sufficient, the workflow produces the complete English draft without an extra approval step. If the supplied material already covers what matters, it drafts directly. It reuses everything already shared and honors requests for a review, formatting only, or a draft without further questions.

An existing CV is optional. If you do not yet have a specific vacancy, start with the role you want; the result is a role-focused baseline that can later be tailored to a posting. Hebrew output remains available when you explicitly request it.

The package contains three skills: a short getting-started workflow, CV and LinkedIn optimization, and interview pitches and STAR answers. It adapts to juniors, career switchers, experienced individual contributors, and senior leaders.

## What you can create

- A clearer, ATS-friendly CV and role-specific job-match assessment.
- A LinkedIn headline, About section, and experience descriptions consistent with your CV.
- A spoken personal introduction in your requested length and STAR answers to behavioral questions.
- An application strategy, focused interview preparation, and mock practice one question at a time when requested.

The package includes [CV content and layout templates](skills/shahar-cv-optimizer/templates/template-index.md), LinkedIn profile sections, application strategy, and interview-preparation guides. The workflow selects and reads the relevant template before drafting, then briefly states what it actually used outside your professional material.

The [bundled document renderer](skills/shahar-cv-optimizer/references/document-export.md) creates editable DOCX files in Classic, Crimson, and Warm from supported candidate content. PDF export uses the same layout when LibreOffice is available. Classic is the default, and you can request Crimson or Warm directly. The assistant prepares the structured input internally, so you can simply ask for your preferred theme and file format.

The PDF design references remain visual examples rather than fillable candidate forms. The renderer uses a single reading column, inline dates, and installed font fallbacks. It is a practical implementation of each theme, not an exact copy of the reference. Final pages and extracted text are checked before delivery when the host supports those checks.

For Hebrew CVs, ask explicitly for Hebrew output. The workflow uses native right-to-left paragraphs and checks mixed English names, technologies, dates, and contact links. A Hebrew conversation alone does not change the English CV default.

Work in Hebrew or English. Final CV and LinkedIn materials default to English unless you request another language; spoken interview pitches follow your language. Israel is the default job market unless your context indicates another country.

## Evidence before polish

Career Studio is instructed to preserve your actual titles, responsibilities, dates, technologies, and achievements. It labels missing evidence, transferable skills, and genuine gaps rather than treating them as wording problems.

**Fictional example:** a sample candidate says they migrated a nightly reporting job to Airflow and measured a change from six hours to 40 minutes.

> Before: Responsible for data pipelines.
>
> After: Migrated a nightly reporting job to an Airflow DAG, reducing runtime from six hours to forty minutes.

The example supplies the metric. It does not imply that another candidate achieved the same result. See the [complete fictional demonstration](skills/shahar-cv-optimizer/references/first-result-demo.md). Questions marked `Requires confirmation` remain outside candidate-ready copy until resolved.

Review final materials for accuracy. The plugin does not guarantee ATS acceptance, interviews, or employment outcomes.

## Setup and availability

The public repository is a source-available beta. The ChatGPT archive installs as a **private plugin**; the package does not provide a verified public directory installation link.

### ChatGPT

From the repository root:

```bash
python3 -m pip install -r scripts/requirements-validation.txt
python3 scripts/package_plugin.py
```

Use the resulting `dist/shahar-polaks-career-studio-<version>.zip` with Plugin Creator. Ask it to create your private plugin, or update your existing Career Studio plugin when upgrading. Open the returned link and start a conversation with Career Studio selected.

The package declares Browser as a dependency and does not configure a separate author-operated server or API key. Host and account capabilities determine access to Plugin Creator, Browser, and document export.

### Claude Code

```bash
claude plugin marketplace add shahar84/shahar-polaks-career-studio
claude plugin install shahar-polaks-career-studio@shahar-polaks-career-studio
```

### Codex

```bash
codex plugin marketplace add shahar84/shahar-polaks-career-studio
codex plugin add shahar-polaks-career-studio@shahar-polaks-career-studio
```

Reload the host or start a new task after installation. Repository changes do not automatically update an installed ChatGPT release.

## Browser-assisted work

Ask for the relevant profile, job posting, or company page. Reading and interacting with pages depends on the tools, connection, and mode available in the host. Career Studio follows their current capabilities and reports what it actually accessed. If access is unavailable, pasted profile or job text can keep the task moving. Complete any necessary sign-in through the host's supported browser flow rather than sharing credentials in chat.

Career Studio states which sources it could access and flags candidate claims that need confirmation. A profile review produces suggestions. Saving edits, sending messages, uploading a CV, or submitting an application requires your specific instruction and the host's applicable approvals.

The existing Browser dependency is intended for compatible private account or workspace use. Public directory submission is a separate release step; a private plugin link alone does not establish public access.

## Support, privacy, and license

Read [PRIVACY.md](PRIVACY.md) before sharing career materials. See [SUPPORT.md](SUPPORT.md) for troubleshooting and redacted feedback instructions. [GitHub issues](https://github.com/shahar84/shahar-polaks-career-studio/issues) are public and should not contain CVs or personal data.

The plugin is free for individual personal career use under the [Shahar Polak Personal Use License 1.0](LICENSE). Host subscriptions and services may have separate requirements. Redistribution, modification, commercial use, and competing use require written permission.
