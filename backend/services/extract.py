import io
import pdfplumber
import fitz  # PyMuPDF
from utils.text_cleaning import normalize_text_block

def _extract_with_pdfplumber(data: bytes) -> str:
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        pages = [p.extract_text(x_tolerance=1, y_tolerance=1) or "" for p in pdf.pages]
    return "\n".join(pages)

def _extract_with_pymupdf(data: bytes) -> str:
    text = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text("text"))
    return "\n".join(text)

def extract_text_from_pdf(data: bytes) -> str:
    """
    Robust extractor with fallbacks. Returns normalized, cleaned text:
    - dehyphenation
    - bullet/decorative symbol stripping
    - whitespace normalization
    """
    text = ""
    try:
        text = _extract_with_pdfplumber(data)
    except Exception:
        pass

    if not text or len(text.strip()) < 20:
        try:
            text = _extract_with_pymupdf(data)
        except Exception:
            text = ""

    return normalize_text_block(text)
