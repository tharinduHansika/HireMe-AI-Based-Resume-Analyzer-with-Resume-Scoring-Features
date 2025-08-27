# core/layout_pdf.py
from __future__ import annotations
import fitz  # PyMuPDF
from typing import List

def extract_pdf_text_layout(pdf_bytes: bytes) -> str:
    """
    Reconstructs reading order for two-column/left-sidebar pages:
    left column (top->bottom) then right column (top->bottom).
    """
    out_pages: List[str] = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            width = page.rect.width
            mid = width * 0.55  # 0.55 works better for narrow sidebars
            blocks = page.get_text("blocks")  # (x0,y0,x1,y1, text, block_no, ...)
            left, right = [], []
            for b in blocks:
                x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
                if not str(txt).strip():
                    continue
                center_x = (x0 + x1) / 2
                (left if center_x < mid else right).append((y0, x0, txt))
            left.sort(key=lambda t: (t[0], t[1]))
            right.sort(key=lambda t: (t[0], t[1]))
            page_txt = "\n".join([t[2] for t in left] + [""] + [t[2] for t in right])
            out_pages.append(page_txt)
    return "\n\n".join(out_pages)
