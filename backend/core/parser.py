import io
import fitz  # PyMuPDF
import pdfplumber

def extract_text_pymupdf(pdf_bytes: bytes) -> str:
    text = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text("text"))
    return "\n".join(text)

def extract_text_pdfplumber(pdf_bytes: bytes) -> str:
    text = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Tries PyMuPDF first for speed; falls back to pdfplumber.
    """
    try:
        t = extract_text_pymupdf(pdf_bytes)
        if t and t.strip():
            return t
    except Exception:
        pass
    try:
        t = extract_text_pdfplumber(pdf_bytes)
        if t and t.strip():
            return t
    except Exception:
        pass
    return ""
