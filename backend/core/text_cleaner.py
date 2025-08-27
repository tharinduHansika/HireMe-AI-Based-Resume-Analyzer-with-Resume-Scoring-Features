# core/text_cleaner.py
from __future__ import annotations
import re
import unicodedata
from unidecode import unidecode

_BULLETS = r"•·●◦■▪▶➤➔►"  # common glyphs from templates
_BUL_CLASS = f"[{_BULLETS}]"

def normalize_unicode(s: str) -> str:
    s = s.replace("\x00", " ")
    s = unicodedata.normalize("NFKC", s)
    s = unidecode(s)  # e.g., “smart quotes”, accents → ascii-ish
    return s

def fix_hyphenation(s: str) -> str:
    # experi-\nence -> experience
    return re.sub(r"(\w)-\n(\w)", r"\1\2", s)

def normalize_bullets(s: str) -> str:
    s = re.sub(_BUL_CLASS, "-", s)
    s = re.sub(r"^\s*[–—-]\s*", "- ", s, flags=re.MULTILINE)
    return s

def strip_noise_icons(s: str) -> str:
    # Drop lines that are only icons/punctuation (common in sidebars)
    return "\n".join([ln for ln in s.splitlines() if re.sub(r"[^\w]+", "", ln).strip()])

def collapse_whitespace(s: str) -> str:
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def drop_repeated_header_footer(pages: list[str]) -> list[str]:
    """Remove a repeating header/footer line (e.g., contact bar) across pages."""
    if len(pages) < 2:
        return pages
    first_lines = []
    for p in pages:
        for ln in p.splitlines():
            if ln.strip():
                first_lines.append(ln.strip())
                break
    if not first_lines:
        return pages
    anchor = first_lines[0]
    repeat = sum(1 for p in pages if anchor in p)
    if repeat < len(pages) // 2:
        return pages
    cleaned = []
    for p in pages:
        cleaned.append("\n".join([ln for ln in p.splitlines() if anchor not in ln]))
    return cleaned

def clean_text(s: str) -> str:
    s = normalize_unicode(s)
    s = fix_hyphenation(s)
    s = normalize_bullets(s)
    s = strip_noise_icons(s)
    s = collapse_whitespace(s)
    return s