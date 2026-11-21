#!/usr/bin/env python3
"""Render supplied CV content to editable DOCX and, optionally, PDF.

No network access or content generation. See references/document-export.md for
the input contract, factual review requirements, and visual verification steps.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit


THEMES = {
    "classic": {"ink": "1A1614", "body": "1A1614", "accent": "6D2D3F", "muted": "57504C", "name_size": 27,
                "name_fonts": ("Newsreader", "Georgia", "Liberation Serif", "DejaVu Serif"),
                "body_fonts": ("Public Sans", "Arial", "Liberation Sans", "DejaVu Sans")},
    "crimson": {"ink": "10151F", "body": "3F4753", "accent": "B3213C", "muted": "596371", "name_size": 30,
                "name_fonts": ("Bodoni Moda", "Georgia", "Liberation Serif", "DejaVu Serif"),
                "body_fonts": ("Jost", "Arial", "Liberation Sans", "DejaVu Sans")},
    "warm": {"ink": "2F2823", "body": "5B5049", "accent": "8A5F4E", "muted": "6E6158", "name_size": 30,
             "name_fonts": ("Bodoni Moda", "Georgia", "Liberation Serif", "DejaVu Serif"),
             "body_fonts": ("Jost", "Arial", "Liberation Sans", "DejaVu Sans")},
}
PLACEHOLDERS = re.compile(
    r"\b(?:TODO|TBD|Requires confirmation)\b|\{\{[^{}]*\}\}|"
    r"\[(?:name|candidate[^\]]*|insert[^\]]*|your[^\]]*|employer|dates?|metric|confirm[^\]]*)\]",
    re.IGNORECASE,
)
FORBIDDEN_CONTROLS = {chr(i) for i in range(32)} - {"\t", "\n", "\r"}
# Direction belongs in document properties, not invisible overrides in source text.
FORBIDDEN_CONTROLS |= {chr(i) for i in range(0x202A, 0x202F)} | {chr(i) for i in range(0x2066, 0x206A)}


class CVError(ValueError):
    """A useful, non-traceback input or export error."""


def object_fields(value: object, allowed: set[str], required: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise CVError(f"{label} must be an object")
    unknown = value.keys() - allowed
    missing = required - value.keys()
    if unknown:
        raise CVError(f"{label}: unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        raise CVError(f"{label}: missing fields: {', '.join(sorted(missing))}")
    return value


def text_value(value: object, label: str, limit: int = 10000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CVError(f"{label} must be nonempty text; omit unused fields")
    if len(value) > limit:
        raise CVError(f"{label} exceeds {limit} characters")
    if any(c in FORBIDDEN_CONTROLS for c in value) or any(unicodedata.category(c) == "Cs" for c in value):
        raise CVError(f"{label} contains invalid controls; supply ordinary logical text")
    if PLACEHOLDERS.search(value):
        raise CVError(f"{label} contains an unresolved placeholder or confirmation note")
    return value


def list_value(value: object, label: str, *, maximum: int = 100, nonempty: bool = False) -> list:
    if not isinstance(value, list) or len(value) > maximum or (nonempty and not value):
        raise CVError(f"{label} must be {'a nonempty' if nonempty else 'an'} array of at most {maximum} items")
    return value


def validate(data: object) -> dict:
    data = object_fields(data, {"schema_version", "language", "name", "headline", "contact", "sections", "example"},
                         {"schema_version", "language", "name", "sections"}, "CV")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise CVError("schema_version must be the integer 1")
    if data["language"] not in ("en", "he"):
        raise CVError("language must be en or he")
    if "example" in data and type(data["example"]) is not bool:
        raise CVError("example must be true or false")
    text_value(data["name"], "name", 200)
    if "headline" in data:
        text_value(data["headline"], "headline", 300)
    for i, item in enumerate(list_value(data.get("contact", []), "contact", maximum=12)):
        label = f"contact[{i}]"
        item = object_fields(item, {"text", "url"}, {"text"}, label)
        text_value(item["text"], f"{label}.text", 300)
        if "url" in item:
            text_value(item["url"], f"{label}.url", 2000)
            try:
                url = urlsplit(item["url"])
            except ValueError as exc:
                raise CVError(f"{label}.url is invalid") from exc
            if (url.scheme not in {"https", "http", "mailto"}
                    or (url.scheme in {"https", "http"} and (not url.hostname or url.username or url.password))
                    or (url.scheme == "mailto" and (not url.path or "@" not in url.path))
                    or any(c.isspace() for c in item["url"])):
                raise CVError(f"{label}.url must be an HTTP(S) or mailto URL without credentials or spaces")
    for i, section in enumerate(list_value(data["sections"], "sections", maximum=30, nonempty=True)):
        label = f"sections[{i}]"
        section = object_fields(section, {"heading", "paragraphs", "entries"}, {"heading"}, label)
        text_value(section["heading"], f"{label}.heading", 150)
        paragraphs = list_value(section.get("paragraphs", []), f"{label}.paragraphs")
        entries = list_value(section.get("entries", []), f"{label}.entries")
        if not paragraphs and not entries:
            raise CVError(f"{label} has no content; remove empty sections")
        for j, paragraph in enumerate(paragraphs):
            text_value(paragraph, f"{label}.paragraphs[{j}]")
        for j, entry in enumerate(entries):
            entry_label = f"{label}.entries[{j}]"
            entry = object_fields(entry, {"title", "subtitle", "dates", "location", "text", "bullets"}, {"title"}, entry_label)
            for field in ("title", "subtitle", "dates", "location", "text"):
                if field in entry:
                    text_value(entry[field], f"{entry_label}.{field}")
            for k, bullet in enumerate(list_value(entry.get("bullets", []), f"{entry_label}.bullets")):
                text_value(bullet, f"{entry_label}.bullets[{k}]")
    return data


def read_input(path: Path) -> dict:
    if path.stat().st_size > 1024 * 1024:
        raise CVError("Input is larger than 1 MiB")
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise CVError(f"Input contains duplicate JSON field: {key}")
            result[key] = value
        return result
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CVError(f"Input must be valid UTF-8 JSON: {exc}") from exc
    return validate(data)


def font_choices(theme: dict, language: str) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    installed: set[str] = set()
    if shutil.which("fc-list"):
        try:
            result = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True, timeout=10, check=True)
            installed = {name.strip().casefold() for line in result.stdout.splitlines() for name in line.split(",")}
        except (OSError, subprocess.SubprocessError):
            pass
    def choose(preferred: tuple[str, ...], fallback: str) -> str:
        selected = next((font for font in preferred if font.casefold() in installed), fallback)
        if selected != preferred[0]:
            warnings.append(f"Font substitution: {preferred[0]} -> {selected}.")
        return selected
    if language == "he":
        # Latin-only display fonts cannot be the Hebrew name font.
        body = choose(("DejaVu Sans", "Arial", "Liberation Sans"), "Arial")
        name = body
        warnings.append("Hebrew uses a Hebrew-capable sans font for name and body; the Latin display-font reference differs.")
    else:
        body = choose(theme["body_fonts"], "Arial")
        name = choose(theme["name_fonts"], "Georgia")
    if not installed:
        warnings.append("Installed fonts could not be checked; inspect the rendered output for substitution and glyph coverage.")
    return name, body, warnings


def directional_segments(text: str, rtl: bool) -> list[tuple[str, bool]]:
    """Keep logical character order; give strong Latin/numeric runs LTR metadata."""
    parts: list[tuple[str, bool]] = []
    current_direction = rtl
    for char in text:
        direction = unicodedata.bidirectional(char)
        char_rtl = True if direction in {"R", "AL"} else False if direction in {"L", "EN", "AN"} else current_direction
        if not parts or parts[-1][1] != char_rtl:
            parts.append((char, char_rtl))
        else:
            previous, _ = parts[-1]
            parts[-1] = (previous + char, char_rtl)
        current_direction = char_rtl
    return parts


def build_document(data: dict, theme_name: str):
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Mm, Pt, RGBColor
        from docx.opc.constants import RELATIONSHIP_TYPE
    except ImportError as exc:
        raise CVError("DOCX export requires python-docx in the active Python environment") from exc

    theme = THEMES[theme_name]
    rtl = data["language"] == "he"
    name_font, body_font, warnings = font_choices(theme, data["language"])
    doc = Document()
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.title = data["name"]
    doc.core_properties.subject = ""
    doc.core_properties.comments = ""
    section = doc.sections[0]
    section.page_width, section.page_height = Mm(210), Mm(297)
    section.top_margin = section.bottom_margin = Pt(44)
    section.left_margin = section.right_margin = Pt(48)

    def set_fonts(properties, font: str):
        fonts = properties.find(qn("w:rFonts"))
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            properties.insert(0, fonts)
        for name in ("ascii", "hAnsi", "cs", "eastAsia"):
            fonts.set(qn(f"w:{name}"), font)
        for name in ("asciiTheme", "hAnsiTheme", "csTheme", "cstheme", "eastAsiaTheme"):
            fonts.attrib.pop(qn(f"w:{name}"), None)

    for name in ("Normal", "Title", "Subtitle", "Heading 1", "Heading 2"):
        style = doc.styles[name]
        style.font.name = body_font
        style.font.size = Pt(11)
        style.font.color.rgb = RGBColor.from_string(theme["body"])
        set_fonts(style.element.get_or_add_rPr(), body_font)
        style.paragraph_format.space_after = Pt(5)
        style.paragraph_format.line_spacing = 1.12
        style.paragraph_format.widow_control = True
        # Some python-docx distributions include a blue rule in Title. Remove
        # inherited template decoration before applying the selected CV theme.
        pr = style.element.find(qn("w:pPr"))
        if pr is not None:
            for border in list(pr.findall(qn("w:pBdr"))):
                pr.remove(border)
    doc.styles["Title"].font.name = name_font
    doc.styles["Title"].font.size = Pt(26 if rtl else theme["name_size"])
    doc.styles["Title"].font.bold = True
    doc.styles["Title"].font.color.rgb = RGBColor.from_string(theme["ink"])
    set_fonts(doc.styles["Title"].element.get_or_add_rPr(), name_font)
    doc.styles["Heading 1"].font.size = Pt(10)
    doc.styles["Heading 1"].font.bold = True
    doc.styles["Heading 1"].font.color.rgb = RGBColor.from_string(theme["accent"])
    doc.styles["Heading 1"].paragraph_format.space_before = Pt(13)
    doc.styles["Heading 1"].paragraph_format.space_after = Pt(6)
    doc.styles["Heading 1"].paragraph_format.keep_with_next = True
    doc.styles["Heading 2"].font.bold = True
    doc.styles["Heading 2"].font.color.rgb = RGBColor.from_string(theme["ink"])
    doc.styles["Heading 2"].paragraph_format.space_before = Pt(7)
    doc.styles["Heading 2"].paragraph_format.space_after = Pt(3)

    def paragraph(style="Normal", *, direction: bool | None = None, keep=False):
        p = doc.add_paragraph(style=style)
        is_rtl = rtl if direction is None else direction
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next = keep
        p.paragraph_format.widow_control = True
        pr = p._p.get_or_add_pPr()
        bidi = OxmlElement("w:bidi")
        bidi.set(qn("w:val"), "1" if is_rtl else "0")
        pr.insert_element_before(bidi, "w:spacing", "w:ind", "w:jc", "w:textDirection")
        # start is direction-aware. A physical 'right' value is mirrored by
        # LibreOffice for bidi paragraphs and would place Hebrew at the left.
        if is_rtl:
            pr.find(qn("w:jc")).set(qn("w:val"), "start")
        return p

    def add_text(p, value: str, *, bold=False, color: str | None = None, size=None, font=None, direction=None):
        runs = []
        for part, part_rtl in directional_segments(value, rtl if direction is None else direction):
            run = p.add_run(part)
            run.font.rtl = part_rtl
            if bold:
                run.bold = True
                run.font.cs_bold = True
            if font:
                run.font.name = font
                set_fonts(run._r.get_or_add_rPr(), font)
            if color:
                run.font.color.rgb = RGBColor.from_string(color)
            if size:
                run.font.size = Pt(size)
                sz_cs = OxmlElement("w:szCs")
                sz_cs.set(qn("w:val"), str(int(size * 2)))
                run._r.get_or_add_rPr().append(sz_cs)
            lang = OxmlElement("w:lang")
            lang.set(qn("w:val"), "he-IL" if part_rtl else "en-US")
            lang.set(qn("w:bidi"), "he-IL")
            run._r.get_or_add_rPr().append(lang)
            runs.append(run)
        return runs

    if data.get("example"):
        p = paragraph(direction=False, keep=True)
        if rtl:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        add_text(p, "FICTIONAL EXAMPLE", bold=True, color=theme["accent"], size=9, direction=False)
    p = paragraph("Title", keep=True)
    add_text(p, data["name"], bold=True, font=name_font, size=26 if rtl else theme["name_size"], color=theme["ink"])
    if "headline" in data:
        p = paragraph(keep=True)
        add_text(p, data["headline"], color=theme["accent"], size=11)
    if data.get("contact"):
        # Contact information is intentionally one LTR body paragraph. The Hebrew
        # city/name runs retain their own direction, and links stay copyable.
        p = paragraph(direction=False, keep=True)
        if rtl:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_after = Pt(8)
        for i, item in enumerate(data["contact"]):
            if i:
                add_text(p, "  |  ", color=theme["muted"], size=9.5, direction=False)
            runs = add_text(p, item["text"], color=theme["muted"], size=9.5, direction=False)
            if "url" in item:
                link = OxmlElement("w:hyperlink")
                link.set(qn("r:id"), p.part.relate_to(item["url"], RELATIONSHIP_TYPE.HYPERLINK, is_external=True))
                for run in runs:
                    link.append(run._r)
                p._p.append(link)
        borders = OxmlElement("w:pBdr")
        border = OxmlElement("w:bottom")
        for key, value in {"val": "single", "sz": "8", "space": "8", "color": theme["accent"]}.items():
            border.set(qn(f"w:{key}"), value)
        borders.append(border)
        p._p.get_or_add_pPr().append(borders)

    for content in data["sections"]:
        p = paragraph("Heading 1", keep=True)
        heading = content["heading"] if rtl else content["heading"].upper()
        add_text(p, heading, bold=True, color=theme["accent"], size=10)
        for value in content.get("paragraphs", []):
            add_text(paragraph(), value, size=11)
        for entry in content.get("entries", []):
            has_details = any(entry.get(key) for key in ("subtitle", "dates", "location", "text", "bullets"))
            p = paragraph("Heading 2", keep=has_details)
            add_text(p, entry["title"], bold=True, color=theme["ink"], size=11)
            metadata_order = ("dates", "subtitle", "location") if rtl else ("subtitle", "dates", "location")
            metadata = [entry[key] for key in metadata_order if entry.get(key)]
            if metadata:
                # Keep the metadata paragraph LTR so numeric date ranges stay
                # in their supplied order. Hebrew words retain run direction.
                p = paragraph(direction=False, keep=bool(entry.get("text") or entry.get("bullets")))
                if rtl:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                p.paragraph_format.space_after = Pt(4)
                add_text(p, " | ".join(metadata), color=theme["muted"], size=10, direction=False)
            if entry.get("text"):
                add_text(paragraph(keep=bool(entry.get("bullets"))), entry["text"], size=11)
            bullets = entry.get("bullets", [])
            keep_short_entry = len(bullets) <= 5 and sum(len(value) for value in bullets) + len(entry.get("text", "")) < 900
            for index, bullet in enumerate(bullets):
                p = paragraph(keep=keep_short_entry and index < len(bullets) - 1)
                p.paragraph_format.keep_together = True
                p.paragraph_format.space_after = Pt(4)
                # A normal Unicode bullet keeps extraction simple and uses the
                # body font, avoiding a Wingdings/symbol-font dependency.
                p.paragraph_format.left_indent = Pt(11)
                p.paragraph_format.first_line_indent = Pt(-11)
                add_text(p, "• ", color=theme["accent"], size=11)
                add_text(p, bullet, size=11)
    return doc, {"theme": theme_name, "language": data["language"], "name_font": name_font,
                 "body_font": body_font, "warnings": warnings}


def export_pdf(docx_path: Path, pdf_path: Path) -> None:
    executable = shutil.which("soffice") or shutil.which("libreoffice")
    if not executable:
        raise CVError("PDF export requires LibreOffice (soffice). The DOCX was created successfully.")
    with tempfile.TemporaryDirectory(prefix="career-studio-export-") as temp:
        root = Path(temp)
        profile = (root / "profile").as_uri()
        result = subprocess.run(
            [executable, f"-env:UserInstallation={profile}", "--headless", "--convert-to", "pdf:writer_pdf_Export",
             "--outdir", str(root), str(docx_path)], capture_output=True, text=True, timeout=60,
        )
        produced = root / f"{docx_path.stem}.pdf"
        if not produced.is_file() or not produced.read_bytes().startswith(b"%PDF-"):
            detail = (result.stderr or result.stdout).strip()[-1000:]
            raise CVError(f"LibreOffice did not produce a PDF. The DOCX was created successfully. {detail}")
        # The exclusive target was preflighted before creating any artifact.
        with pdf_path.open("xb") as target:
            target.write(produced.read_bytes())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 JSON containing reviewed candidate facts")
    parser.add_argument("--output", type=Path, help="New .docx path; existing files are never overwritten")
    parser.add_argument("--theme", choices=THEMES, default="classic")
    parser.add_argument("--pdf", action="store_true", help="Also create a PDF beside the DOCX using LibreOffice")
    parser.add_argument("--check", action="store_true", help="Validate JSON without writing files")
    parser.add_argument("--allow-example", action="store_true", help="Render labeled fictional example data")
    args = parser.parse_args(argv)
    report = {}
    try:
        data = read_input(args.input)
        if data.get("example") and not args.allow_example:
            raise CVError("This is fictional example data. Use --allow-example for a visibly labeled sample, never as a candidate CV.")
        if args.check:
            print(json.dumps({"valid": True, "theme": args.theme, "language": data["language"]}))
            return 0
        if not args.output:
            raise CVError("--output is required unless --check is used")
        target = args.output.absolute()
        if target.suffix.lower() != ".docx":
            raise CVError("--output must end in .docx")
        pdf_target = target.with_suffix(".pdf")
        for output in [target] + ([pdf_target] if args.pdf else []):
            if output.exists() or output.is_symlink():
                raise CVError(f"Output already exists: {output}. Choose a new filename.")
            if output.resolve() == args.input.resolve():
                raise CVError("Output cannot replace the input")
        document, report = build_document(data, args.theme)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            document.save(stream)
        report["docx"] = str(target)
        if args.pdf:
            export_pdf(target, pdf_target)
            report["pdf"] = str(pdf_target)
        report["verification_required"] = "Render and inspect every page, then check extracted text and hyperlinks before delivery."
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (CVError, OSError, subprocess.TimeoutExpired) as exc:
        if report.get("docx"):
            print(json.dumps({"docx": report["docx"], "pdf": None, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"CV export failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
