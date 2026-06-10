# -*- coding: utf-8 -*-
"""Tests for merged PDF page footer renumbering."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

from scripts.build_pdf import apply_continuous_page_footers


def _two_page_pdf(path: Path) -> None:
    writer = PdfWriter()
    for _ in range(2):
        packet = BytesIO()
        page = canvas.Canvas(packet, pagesize=(595, 842))
        page.drawString(72, 800, "body")
        page.save()
        packet.seek(0)
        writer.add_page(PdfReader(packet).pages[0])
    with path.open("wb") as out:
        writer.write(out)


def test_apply_continuous_page_footers(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    _two_page_pdf(pdf_path)
    apply_continuous_page_footers(pdf_path)
    reader = PdfReader(str(pdf_path))
    assert len(reader.pages) == 2
    text = (reader.pages[0].extract_text() or "") + (
        reader.pages[1].extract_text() or ""
    )
    assert "1 / 2" in text
    assert "2 / 2" in text
