# Document input handling

Covers CVs or other materials supplied as images, scanned PDFs, or photos —
anything without a reliable text layer. Applies on top of, not instead of,
the truth policy.

Attempt-then-disclose: try to read the document visually first. Current
Claude Code environments generally view rendered pages as images even
without a text layer; Codex's support for this is less consistent across
setups. Don't assume either platform will read a given scan reliably — if it
plainly can't, say so and ask for pasted text instead of proceeding.

Treat anything recovered from a scan or photo as an unverified transcription,
not a confirmed fact, no matter how clean it looks. Ask the candidate to
confirm names, dates, numbers, employers, and titles pulled from a scan
before using them in a requirement match or a final deliverable. This is the
same `Requires confirmation` handling used for any other unverified detail,
applied here to transcription accuracy itself rather than to the underlying
claim.

Never claim guaranteed-accurate extraction, describe it as "running OCR," or
state an accuracy rate — that promises a capability that isn't consistently
available and isn't something to assert either way.

If the scan is low quality, rotated, multi-column, or handwritten, say
plainly which parts were unreadable or uncertain instead of guessing and
presenting the guess as fact. If visual reading is unavailable or clearly
unreliable for a given file, ask for the CV as pasted text or a text-based
PDF rather than continuing on a guess.
