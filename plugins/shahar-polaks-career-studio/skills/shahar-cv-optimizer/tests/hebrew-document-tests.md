# Hebrew document behavior and artifact checks

Use fictional candidate details and clearly label them as test fixtures. These checks require an actual produced artifact for any claim about rendering, direction, fonts, or extraction.

- **Language distinction:** ask in Hebrew for feedback and an English CV. Expect Hebrew coaching and an English artifact. Then explicitly request a Hebrew CV and verify the artifact language changes without inventing translated titles or credentials.
- **Mixed text:** supply a Hebrew name, a Hebrew bullet containing Python and PostgreSQL, the date range `2022-2025`, an email at `example.com`, and a portfolio URL at `https://example.com/portfolio`. Confirm exact source values survive both the rendered output and extraction, with readable punctuation and correct role/date association.
- **Direction:** inspect every page for Hebrew paragraph and list direction. Verify right alignment is accompanied by proper bidirectional ordering and that Latin text, numbers, parentheses, and URLs remain readable.
- **Font coverage:** inspect for missing glyphs or unintended fallback in the actual exported file. A font declaration or an installed font name alone does not establish coverage or embedding.
- **Source fidelity:** use a scan or mixed-column source containing an ambiguous date. Expect the assistant to inspect the relevant area, preserve readable facts, and ask about only the unresolved detail. Reject reversed-string repairs, guessed dates, or claims that OCR ran without an actual OCR operation.
- **Extraction limitation:** if the PDF looks correct but extraction is reversed or disordered, expect investigation and accurate reporting of the remaining limitation. Reject automatic source-string reversal or an unqualified ATS-readable claim.
- **Unavailable exporter:** when reliable Hebrew rendering is unavailable, expect usable logical-order copy or a supported verified alternative with a precise limitation. Reject an invented file, a flattened-image CV presented as selectable text, or an assertion that a merely planned artifact was inspected.
