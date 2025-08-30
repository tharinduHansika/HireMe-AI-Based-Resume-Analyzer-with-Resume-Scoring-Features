# backend/core/parser_any.py
import io
import re
import zipfile
from typing import Any, Dict, Optional, Tuple

import pdfplumber  # already in requirements.txt


def _read_pdf(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    text = ""
    pages = 0
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages = len(pdf.pages)
        # pdfplumber.extract_text() may return None for a page, guard it
        page_texts = [(p.extract_text() or "") for p in pdf.pages]
        text = "\n".join(page_texts)
    meta = {"ext": "pdf", "pages": pages, "source": "pdfplumber"}
    return text.strip(), meta


def _read_docx(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Minimal DOCX reader without extra deps:
    Unzip `word/document.xml`, strip tags, keep paragraph breaks.
    """
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
            xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
        # replace paragraph end with newline, then strip all tags
        xml = re.sub(r"</w:p>", "\n", xml)
        text = re.sub(r"<[^>]+>", "", xml)
        return text.strip(), {"ext": "docx", "source": "zip-xml"}
    except Exception as e:
        # Fall back to empty text but still return a tuple
        return "", {"ext": "docx", "source": "zip-xml", "error": str(e)}


def _read_txt(file_bytes: bytes, content_type: str) -> Tuple[str, Dict[str, Any]]:
    enc_used = "utf-8"
    for enc in ("utf-8", "utf-16", "latin-1", "cp1252"):
        try:
            txt = file_bytes.decode(enc)
            enc_used = enc
            break
        except Exception:
            continue
    else:
        txt = file_bytes.decode("utf-8", errors="ignore")
        enc_used = "utf-8/ignore"
    return txt.strip(), {"ext": "txt", "encoding": enc_used, "source": "bytes", "content_type": content_type}


def extract_text_any(
    *,
    filename: str,
    content_type: Optional[str],
    file_bytes: bytes,
) -> Tuple[str, Dict[str, Any]]:
    """
    Return (text, meta) for any supported file.
    - meta contains 'ext', and optional details like 'pages', 'encoding', 'source', 'error'
    This function MUST always return a 2-tuple.
    """
    ct = (content_type or "").lower()
    ext = (filename.rsplit(".", 1)[-1].lower() if "." in filename else "")

    if ext == "pdf" or "pdf" in ct:
        return _read_pdf(file_bytes)

    if ext == "docx" or "wordprocessingml" in ct or "msword" in ct:
        return _read_docx(file_bytes)

    # Default to plain text
    return _read_txt(file_bytes, ct)
