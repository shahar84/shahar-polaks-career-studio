# Career Studio support

For a bug or feature idea, [open an issue](https://github.com/shahar84/shahar-polaks-career-studio/issues). For other questions, use the contact options on [Shahar Polak's website](https://www.shaharpolak.com/).

GitHub issues are public. Use a fictional or redacted example and omit names, contact details, CV files, private job applications, credentials, and private browser screenshots.

## Useful feedback

Copy this outline into an issue:

```text
Plugin version:
Host and available mode (for example ChatGPT, Codex, Claude Code):
Task (CV, LinkedIn, interview pitch, or another supported task):
What I expected:
What happened:
Short prompt and output with personal details removed:
Relevant error message, if any:
```

Describe the smallest example that reproduces the issue. For a wording problem, a few redacted sentences usually provide more useful evidence than a full document.

## Common questions

### I have only a CV, without a job description

For a review, Career Studio can improve clarity now. For a tailored CV, it will ask for the specific posting or job description. If you do not have a vacancy yet, name the role you want and build a role-focused baseline, then tailor it when you find a posting.

### I do not have a CV yet

Start with the job you want and a few notes about your experience. Career Studio asks one or two relevant questions at a time and uses the answers to build the CV. You do not need to prepare a document or complete a long questionnaire first.

### Why is it asking about my experience before writing?

The questions connect your actual work to the job's requirements. They may clarify what you personally owned, how you used a technology, the scope of a project, or what changed because of your work. If you have no measured result, say so; concrete responsibilities and outcomes can still be useful. When enough material exists, it drafts. You can also ask it to proceed with the facts already provided.

### Can we speak Hebrew while preparing an English CV?

Yes. Questions and explanations follow your conversation language, while the entire CV defaults to English. A Hebrew source CV or job posting does not change that default. Ask explicitly if you want the finished CV in another language.

### My document cannot be read reliably

Try pasting the relevant text or uploading a clearer, text-selectable document. If an image or scan is ambiguous, confirm the extracted dates, names, and metrics before using them.

### LinkedIn or another page is unavailable

Available page access and browser interaction depend on your host, mode, and connection. Follow the host's supported connection and sign-in flow if the requested task is blocked. You can also paste the relevant headline, About section, experience, or job description to continue. A search snippet or partial page should be identified as partial evidence, not described as a complete profile review.

### Did it use a bundled template?

Ask which template was used. The workflow should read the relevant bundled file before drafting and state its choice outside the CV. For a designed document, it should also inspect the matching PDF reference when the tools support that. Classic is the default; you can request Crimson or Warm directly. If a reference cannot be opened, the assistant should say so and describe the layout guidance it could use.

### I do not see a downloadable CV

Ask for an editable Word file, a PDF, or both, and optionally name Classic, Crimson, or Warm. The bundled renderer creates DOCX with Python and `python-docx`; PDF conversion additionally needs LibreOffice. The assistant should run this for you when those tools are available. If PDF conversion is unavailable, an existing successful DOCX should still be delivered with a clear explanation. The renderer's input and dependency details are in the [document export guide](skills/shahar-cv-optimizer/references/document-export.md).

### I want my CV in Hebrew

Ask explicitly for a Hebrew CV. Career Studio keeps its English CV default during Hebrew coaching unless you request otherwise. Hebrew exports use right-to-left paragraphs with appropriate treatment of English terms, dates, email addresses, and links. The final pages and extracted text should both be reviewed. Report any reversed names, unreadable characters, or detached dates with a fictional or redacted example.

### I want to practice an interview interactively

Ask for a mock interview and name the role or share the job description. The workflow asks one question, waits for your answer, gives focused feedback, and continues. You can request feedback only at the end. Hypothetical technical discussion stays separate from claims about your actual work.

### The output added a fact I did not provide

Do not use that claim. Ask Career Studio to remove it and separate confirmed facts from questions. A redacted example of the source text and added claim is useful feedback. The workflow is designed to avoid fabrication, but model output still needs review.

### My installed plugin did not change after a repository update

Rebuild the package and ask Plugin Creator to update the existing ChatGPT plugin. Preserve the plugin identity rather than creating a duplicate. For other hosts, use their plugin update or reload process.

### Can I send a friend my private plugin link?

A private plugin URL does not establish access for another account. Use the host's supported sharing options where available, or point technical users to this repository's personal-use setup instructions. Workspace sharing and public directory publication are separate distribution paths. The current package has no verified public directory installation link.

## Before sharing your final materials

Confirm the facts, contact information, dates, and links. Keep unresolved `Requires confirmation` notes outside the final candidate-ready document. The plugin supports career preparation; it does not guarantee interviews, job offers, or ATS acceptance.
