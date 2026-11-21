# Career Studio: sharing and discoverability

These notes describe the current distribution boundary and provide draft copy for a future public listing or website page. They do not establish that a listing is public, a landing page is deployed, or search demand has been measured.

## Current distribution

The repository contains a source-available plugin for personal career use. The ChatGPT package is intended for private account or compatible workspace installation and retains its Browser app dependency. Repository changes do not automatically update an installed ChatGPT plugin.

| Route | What can be shared | What still needs verification |
| --- | --- | --- |
| GitHub | The repository and its setup instructions | The recipient has a compatible host and follows the personal-use license |
| Private ChatGPT plugin | A plugin link with access managed through the host's supported sharing controls | The intended recipient can actually open and use it |
| Public directory | A published listing after the separate submission process | Supported integration packaging, review, publication, and a working installation link |
| Shahar's website | A dedicated page with benefits, examples, and an appropriate call to action | The page is built and deployed, and its installation destination works for visitors |

Do not describe a private link as a public install link. Keep the existing audience and permissions unchanged during ordinary plugin updates. Use an authorized sharing or publication workflow when widening access.

For public directory preparation, review the current submission requirements and resolve the existing Browser integration through a supported route. Do not remove a dependency from the public package while continuing to promise its behavior. The private installation archive is not evidence of a successful public submission.

## Positioning

**Name:** Shahar Polak Career Studio

**Short description:** AI CV & Interview Coach

**Core promise:** Build an English CV tailored to the job you want through focused questions about your real experience.

**Hebrew introduction:**

> יש לכם ניסיון. בואו נספר אותו כמו שצריך.
>
> Career Studio של שחר פולק קורא את המשרה שאתם רוצים, שואל את השאלות הנכונות על הניסיון שלכם ובונה קורות חיים מותאמים באנגלית. אפשר לענות בעברית ולהתחיל גם בלי קורות חיים מוכנים.

**What makes the product specific:**

- It connects a target role to evidence from the candidate's actual experience.
- It asks one or two job-specific questions at a time before drafting when important evidence is missing, then writes the CV in English by default.
- It distinguishes missing evidence, transferable experience, and confirmed experience gaps.
- It reads bundled templates before producing the requested material and identifies the template used.
- It generates editable Classic, Crimson, and Warm DOCX files through a shared renderer, with PDF conversion when LibreOffice is available.
- It supports explicitly requested Hebrew documents with native RTL layout, alongside Hebrew or English coaching.
- It carries verified facts from CV work into LinkedIn writing and spoken interview preparation.
- It supports Hebrew conversations with English written career materials by default; users can request another language.
- It treats Browser access, source coverage, and document export as host-dependent capabilities.

## Draft website metadata

Suggested future route: `/career-studio`. This is a proposed route, not a deployed page or an installation URL.

**English title:** Shahar Polak Career Studio | AI CV & Interview Coach

**English description:** Improve your CV, LinkedIn profile, and interview answers with Shahar Polak Career Studio. Practical career coaching in English and Hebrew.

**Hebrew title:** שחר פולק Career Studio | קורות חיים והכנה לראיונות

**Hebrew description:** שיפור קורות חיים, חידוד פרופיל הלינקדאין והכנה לראיונות עם Career Studio של שחר פולק. מתחילים מהניסיון שלכם, בעברית או באנגלית.

The website implementation should set its canonical URL only after choosing the actual published route. The plugin update itself does not publish this metadata to a website.

## Search phrases to validate

These are intent-based content ideas. No search-volume, ranking, competition, or conversion data has been verified for this release.

| Task | English phrase ideas | Hebrew phrase ideas |
| --- | --- | --- |
| CV review | AI resume review; CV review; ATS-friendly CV | שיפור קורות חיים; בדיקת קורות חיים עם AI |
| Role tailoring | tailor resume to job description; CV job match | התאמת קורות חיים למשרה |
| LinkedIn | LinkedIn headline help; LinkedIn About section | שיפור פרופיל לינקדאין; כתיבת אודות בלינקדאין |
| Interview pitch | tell me about yourself answer; interview pitch | ספר לי על עצמך; פיץ׳ לראיון עבודה |
| Behavioral questions | STAR interview answers; behavioral interview preparation | הכנה לראיון עבודה; תשובות בשיטת STAR |

Choose phrases for their relevance to the implemented product. Validate demand with available first-party search data or a suitable keyword tool before treating any phrase as a priority based on traffic. Keep terms natural in the copy; do not promise rankings or repeat keywords to fill space.

## Suggested page structure

1. **A clear first result:** the core promise and one working call to action. Use a verified public installation link when available, or explain the current setup path.
2. **Three ways to start:** CV and job match, LinkedIn profile, and interview pitch or STAR answer. Show one short prompt for each.
3. **One honest before-and-after example:** use the clearly labeled fictional demonstration already in the package. Show the source facts next to the rewrite.
4. **Templates and languages:** explain Classic, Crimson, and Warm, editable DOCX and supported PDF export, English CV defaults, explicit Hebrew RTL output, and spoken-language choice.
5. **Common questions:** inputs, missing job descriptions, Browser access, file export, and who can access the plugin.
6. **Support and privacy:** link to the existing support, privacy, and license documents. Use no invented testimonials, user counts, ratings, hiring outcomes, or endorsements.

Link a future page from relevant existing career articles only after identifying those articles and publishing the route. Do not change unrelated website content as part of a plugin release.

## Release checklist

- Verify the installed release and packaged skills after an update.
- Exercise representative CV, LinkedIn, pitch, and STAR requests; separate observed behavior from untested capabilities.
- Verify the destination and account access before promoting an installation link.
- Keep README claims aligned with the version people can actually install.
- Publish website or directory changes only through the authorized workflow for that destination.
- Record actual feedback with redacted examples. Do not collect candidate CVs through public issues.
