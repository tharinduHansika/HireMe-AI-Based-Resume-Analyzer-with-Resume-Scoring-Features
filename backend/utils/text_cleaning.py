import re

BULLET_PREFIX = re.compile(
    r"^\s*([•●○◦▪▫■□◆◇▶►▸▹‣⁃–—\-*·✓✔✦✧➤➣»]+|\d+\.)\s+"
)
DECORATIVE_LINES = re.compile(r"^\s*[=_\-]{6,}\s*$")

def strip_bullet_prefix(line: str) -> str:
    if DECORATIVE_LINES.match(line or ""):
        return ""
    return BULLET_PREFIX.sub("", line or "").rstrip()

def normalize_text_block(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n")
    lines = []
    carry = ""
    for raw in text.splitlines():
        ln = strip_bullet_prefix(raw)
        if ln.endswith("-") and len(ln) > 1 and ln[-2].isalnum():
            carry += ln[:-1]
            continue
        else:
            if carry:
                ln = carry + ln.lstrip()
                carry = ""
        lines.append(ln)

    out = []
    blank = False
    for ln in lines:
        if ln.strip():
            out.append(ln)
            blank = False
        else:
            if not blank:
                out.append("")
            blank = True
    return "\n".join(out).strip()
