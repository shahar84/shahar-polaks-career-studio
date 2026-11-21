"""Focused artifact tests. Run with --with-pdf for actual LibreOffice exports."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/shahar-polaks-career-studio/skills/shahar-cv-optimizer/scripts/render_cv.py"
spec = importlib.util.spec_from_file_location("career_cv_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
WITH_PDF = "--with-pdf" in sys.argv
if WITH_PDF:
    sys.argv.remove("--with-pdf")
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

DATA = {
    "schema_version": 1,
    "language": "en",
    "name": "Taylor Fixture",
    "headline": "Software Developer",
    "contact": [{"text": "taylor@example.com", "url": "mailto:taylor@example.com"}],
    "sections": [
        {"heading": "Experience", "entries": [
            {"title": "Developer", "subtitle": "Fixture Systems", "dates": "2022 - Present",
             "bullets": ["Built Python services and automated tests.", "Maintained API documentation."]}
        ]},
        {"heading": "Skills", "paragraphs": ["Python, SQL, Git"]}
    ]
}
HEBREW_DATA = {
    "schema_version": 1,
    "language": "he",
    "name": "דנה דוגמה",
    "headline": "מפתחת תוכנה",
    "contact": [{"text": "חיפה, ישראל"}, {"text": "dana@example.com", "url": "mailto:dana@example.com"},
                {"text": "example.com/dana", "url": "https://example.com/dana"}],
    "sections": [
        {"heading": "ניסיון מקצועי", "entries": [
            {"title": "מפתחת Backend", "subtitle": "חברת דוגמה", "dates": "2022 - 2026",
             "bullets": ["פיתחתי שירותים ב-Python על AWS עם בדיקות אוטומטיות.",
                         "עבדתי עם צוות המוצר על API ושיפור תהליכי עבודה."]}
        ]},
        {"heading": "מיומנויות", "paragraphs": ["Python, SQL, Git", "פיתוח תוכנה ועבודה בצוות"]}
    ]
}


def document_xml(path: Path):
    with zipfile.ZipFile(path) as archive:
        return ET.fromstring(archive.read("word/document.xml"))


def paragraph_text(xml):
    return ["".join(p.itertext()) for p in xml.findall(".//w:body/w:p", NS)]


class RendererTests(unittest.TestCase):
    def test_validation_rejects_missing_name_and_unknown_fields(self):
        for change in ({"name": ""}, {"new_fact": "Invented"}, {"schema_version": True},
                       {"language": "fr"}, {"sections": []}):
            data = copy.deepcopy(DATA)
            data.update(change)
            with self.assertRaises(renderer.CVError):
                renderer.validate(data)
        data = copy.deepcopy(DATA)
        del data["name"]
        with self.assertRaises(renderer.CVError):
            renderer.validate(data)

    def test_validation_rejects_bad_nested_types_and_placeholders(self):
        changes = [
            {"heading": "Experience", "entries": [{"title": "Developer", "bullets": "not an array"}]},
            {"heading": "Experience", "entries": [{"title": "Developer", "achievement": "invented"}]},
            {"heading": "Skills", "paragraphs": ["Requires confirmation: team size"]},
            {"heading": "Skills", "paragraphs": ["{{insert metrics}}"]},
            {"heading": "Skills", "paragraphs": ["Python\u202e"]},
            {"heading": "Skills"},
        ]
        for section in changes:
            data = copy.deepcopy(DATA)
            data["sections"] = [section]
            with self.subTest(section=section), self.assertRaises(renderer.CVError):
                renderer.validate(data)

    def test_links_cannot_be_commands_files_or_credential_urls(self):
        for url in ["javascript:alert(1)", "file:///etc/passwd", "https://name:secret@example.com", "https://", "https://a b"]:
            data = copy.deepcopy(DATA)
            data["contact"][0]["url"] = url
            with self.subTest(url=url), self.assertRaises(renderer.CVError):
                renderer.validate(data)

    def test_all_themes_preserve_text_and_use_a4_single_column(self):
        original = copy.deepcopy(DATA)
        with tempfile.TemporaryDirectory() as tmp:
            for theme in renderer.THEMES:
                document, report = renderer.build_document(renderer.validate(DATA), theme)
                path = Path(tmp) / f"{theme}.docx"
                document.save(path)
                xml = document_xml(path)
                paragraphs = paragraph_text(xml)
                text = "\n".join(paragraphs)
                self.assertLess(text.index("Taylor Fixture"), text.index("taylor@example.com"))
                self.assertLess(text.index("Developer\nFixture Systems"), text.index("Built Python"))
                self.assertLess(text.index("Maintained API"), text.index("SKILLS"))
                self.assertIn("Python, SQL, Git", text)
                self.assertNotIn("Jane Doe", text)
                self.assertNotIn("Shahar", text)
                self.assertFalse(xml.findall(".//w:tbl", NS))
                size = xml.find(".//w:sectPr/w:pgSz", NS)
                self.assertEqual(size.get(f"{{{NS['w']}}}w"), "11906")
                self.assertEqual(report["theme"], theme)
                with zipfile.ZipFile(path) as archive:
                    rels = archive.read("word/_rels/document.xml.rels").decode()
                    self.assertIn("mailto:taylor@example.com", rels)
        self.assertEqual(DATA, original)

    def test_hebrew_keeps_logical_source_and_native_direction(self):
        document, report = renderer.build_document(renderer.validate(HEBREW_DATA), "warm")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hebrew.docx"
            document.save(path)
            xml = document_xml(path)
            text = "\n".join(paragraph_text(xml))
            self.assertIn("דנה דוגמה", text)
            self.assertIn("פיתחתי שירותים ב-Python על AWS עם בדיקות אוטומטיות.", text)
            self.assertIn("2022 - 2026", text)
            self.assertIn("dana@example.com", text)
            self.assertTrue(xml.findall('.//w:bidi[@w:val="1"]', NS))
            self.assertTrue(xml.findall('.//w:rtl[@w:val="0"]', NS))
            self.assertTrue(xml.findall('.//w:rtl', NS))
            self.assertEqual(report["language"], "he")

    def test_cli_check_example_gate_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest = Path(tmp) / "input.json", Path(tmp) / "out.docx"
            src.write_text(json.dumps(DATA))
            def call(*args):
                return subprocess.run([sys.executable, str(SCRIPT), str(src), *args], capture_output=True, text=True, timeout=30)
            self.assertEqual(call("--check").returncode, 0)
            self.assertFalse(dest.exists())
            dest.write_text("DO NOT REPLACE")
            result = call("--output", str(dest))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(dest.read_text(), "DO NOT REPLACE")
            example = copy.deepcopy(DATA)
            example["example"] = True
            src.write_text(json.dumps(example))
            self.assertEqual(call("--check").returncode, 2)
            self.assertEqual(call("--check", "--allow-example").returncode, 0)
            dest2 = Path(tmp) / "example.docx"
            self.assertEqual(call("--output", str(dest2), "--allow-example").returncode, 0)
            self.assertIn("FICTIONAL EXAMPLE", "\n".join(paragraph_text(document_xml(dest2))))

    def test_duplicate_json_and_pdf_collision_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "input.json"
            src.write_text('{"name":"One","name":"Two"}')
            with self.assertRaisesRegex(renderer.CVError, "duplicate"):
                renderer.read_input(src)
            src.write_text(json.dumps(DATA))
            pdf = Path(tmp) / "out.pdf"
            pdf.write_text("DO NOT REPLACE")
            result = subprocess.run([sys.executable, str(SCRIPT), str(src), "--output", str(pdf.with_suffix(".docx")), "--pdf"],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(pdf.read_text(), "DO NOT REPLACE")
            self.assertFalse(pdf.with_suffix(".docx").exists())

    def test_missing_pdf_tool_preserves_and_reports_docx(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dest = Path(tmp) / "input.json", Path(tmp) / "out.docx"
            src.write_text(json.dumps(DATA))
            environment = dict(os.environ, PATH=tmp)
            result = subprocess.run([sys.executable, str(SCRIPT), str(src), "--output", str(dest), "--pdf"],
                                    env=environment, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertTrue(dest.is_file())
            self.assertFalse(dest.with_suffix(".pdf").exists())
            self.assertEqual(json.loads(result.stderr)["docx"], str(dest))

    @unittest.skipUnless(WITH_PDF, "use --with-pdf to exercise installed LibreOffice")
    def test_actual_pdf_all_themes_hebrew_and_multiple_pages(self):
        import fitz
        with tempfile.TemporaryDirectory() as tmp:
            for theme in renderer.THEMES:
                docx, pdf = Path(tmp) / f"{theme}.docx", Path(tmp) / f"{theme}.pdf"
                document, _ = renderer.build_document(DATA, theme)
                document.save(docx)
                renderer.export_pdf(docx, pdf)
                with fitz.open(pdf) as rendered:
                    text = "\n".join(page.get_text() for page in rendered)
                    self.assertIn("Taylor Fixture", text)
                    self.assertIn("2022 - Present", text)
                    self.assertIn("Maintained API documentation.", text)
                    self.assertLess(text.index("Fixture Systems"), text.index("Built Python"))
                    self.assertLess(text.index("Maintained API"), text.index("SKILLS"))
                    self.assertAlmostEqual(rendered[0].rect.width, 595.3, delta=1)
                    self.assertTrue(rendered[0].get_links())
            long_data = copy.deepcopy(HEBREW_DATA)
            for i in range(14):
                entry = copy.deepcopy(long_data["sections"][0]["entries"][0])
                entry["title"] = f"תפקיד לדוגמה {i + 1}"
                long_data["sections"][0]["entries"].append(entry)
            docx, pdf = Path(tmp) / "hebrew.docx", Path(tmp) / "hebrew.pdf"
            document, _ = renderer.build_document(long_data, "warm")
            document.save(docx)
            renderer.export_pdf(docx, pdf)
            with fitz.open(pdf) as rendered:
                self.assertGreater(len(rendered), 1)
                text = "\n".join(page.get_text() for page in rendered)
                self.assertIn("dana@example.com", text)
                self.assertIn("Python", text)
                self.assertIn("AWS", text)
                self.assertIn("2022 - 2026", text)
                # Extractor-specific bidi ordering is checked separately during
                # visual QA; DOCX source text is tested in logical order above.
                self.assertEqual(text.count("Python"), 16)
                for page in list(rendered)[1:]:
                    self.assertFalse(page.get_text().lstrip().startswith("•"), "short entry continued as an orphan bullet")


if __name__ == "__main__":
    unittest.main()
