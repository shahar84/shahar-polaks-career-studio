# Reusable CV export

Use the bundled [renderer](../scripts/render_cv.py) after reviewing the candidate's evidence and choosing a theme from the [template index](../templates/template-index.md). It turns supplied content into an editable DOCX and can convert the same document to PDF. It does not write career claims, verify facts, fetch URLs, or guarantee ATS acceptance.

## Prepare the content

Read the selected template specification and inspect its reference PDF. This renderer implements the themes with one content column, inline role metadata, A4 pages, 11 pt body text, and installed font fallbacks. It is a practical adaptation, not an exact facsimile of the reference's date gutter. Classic uses wine accents; Crimson uses burgundy; Warm uses brown. Font substitutions are reported outside the CV.

Write a UTF-8 JSON file from the supported evidence. Keep unresolved questions in companion notes, outside the input. Omit unknown information and empty sections. Preserve job titles, dates, attribution, and the candidate's original meaning. Arrange sections for the candidate's persona before rendering; the renderer preserves their order.

The [fictional example](../assets/cv-input-example.json) demonstrates the shape. Do not use its facts for a candidate. It requires `--allow-example` and produces a visible `FICTIONAL EXAMPLE` label. For a real CV, construct a new input from that candidate's evidence rather than removing the example flag and retaining sample content.

| Object | Fields |
| --- | --- |
| Root | Required: `schema_version: 1`, `language: "en"` or `"he"`, `name`, `sections`. Optional: `headline`, `contact`, `example` boolean. |
| `contact` item | Required: `text`. Optional: `url` using HTTP(S) or `mailto:`. Only use candidate-supplied links. |
| `sections` item | Required: `heading`. Include nonempty `paragraphs` and/or `entries`. |
| `paragraphs` | Array of finished text strings, useful for summary or grouped skills. |
| `entries` item | Required: `title`. Optional: `subtitle`, `dates`, `location`, `text`, `bullets` array of strings. Use subtitle for employer, institution, or project context. |

Unknown fields, invalid field types, blank supplied strings, empty sections, selected placeholder patterns, and unsupported URL schemes are rejected. These are structural checks, not a factual audit or a complete detector of editorial residue. Review every input claim and the final text yourself. Do not add JSON comments, HTML, markup, or manually reversed Hebrew.

## Run the renderer

Resolve the installed skill directory first. Use the host's document runtime when available, including `CODEX_PRIMARY_RUNTIME_PYTHON` in ChatGPT. DOCX requires `python-docx`. PDF additionally requires `soffice` or `libreoffice` on PATH. The script never installs dependencies or contacts an external service.

```bash
python3 scripts/render_cv.py /absolute/path/candidate.json --check
python3 scripts/render_cv.py /absolute/path/candidate.json --output /absolute/path/candidate.docx --theme classic --pdf
```

Run from the skill directory, or substitute the renderer's absolute path. `--theme` accepts `classic`, `crimson`, and `warm`; Classic is the default. `--pdf` creates a PDF beside the DOCX. Existing output files are never overwritten: choose a new filename for revisions. Keep candidate input and output outside the installed plugin directory and out of source control. Follow the host's normal artifact-saving workflow after verification.

The success report lists the files actually produced and selected fonts. It does not establish visual quality. When PDF conversion is unavailable or fails, the error identifies the created DOCX separately. Do not say that a PDF exists unless the report and filesystem confirm it. LibreOffice runs with a separate temporary profile and a 60-second timeout.

## Hebrew and mixed text

Set `language` to `he` only for a Hebrew document. This selects right-to-left paragraph properties and a Hebrew-capable font. Latin names, technologies, email addresses, URLs, and numerals receive left-to-right run properties. Contact information and entry metadata use right-aligned, left-to-right paragraphs with Hebrew words marked appropriately. Dates come first in Hebrew metadata so numeric ranges retain their supplied order. The remaining CV follows Hebrew reading direction.

Keep source characters in logical order. Never reverse strings or add invisible directional overrides to make a screenshot look correct. Hebrew names use a sans font because the Latin reference's display font may lack Hebrew glyphs. Inspect dates, punctuation, English technology names, and links after rendering. Different PDF extractors can represent bidi text differently; check a full Hebrew phrase and its mixed-language context, not just the presence of individual letters.

## Verify before delivery

Follow [document design and verification](pdf-design-guidelines.md) and the host's document/PDF skills. Render every page and inspect the images for clipping, overlapping text, orphan headings, broken bullets, missing glyphs, and awkward page breaks. Check hyperlinks and that job dates remain attached to the correct role. Re-extract PDF text and compare all content, including names, employers, dates, and the final bullet, with the source. For Hebrew, also inspect the logical source text in DOCX and the visual reading order in PDF.

Keep summary and skills concise. Allow relevant content to span pages; the renderer does not truncate content or shrink text to force one page. If an entry is too long or a heading is stranded, revise wording or section arrangement using only the same facts, then render again.

Deliver only requested artifacts. Identify the theme and material font substitutions briefly outside the candidate document. The real candidate's files contain no plugin branding, example data, or confirmation notes. Word, Google Docs, other PDF viewers, and individual ATS products may render or parse differently and need separate testing when that matters.
