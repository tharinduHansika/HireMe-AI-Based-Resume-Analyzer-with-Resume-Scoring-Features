import re
from datetime import datetime

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January","February","March","April","May","June","July","August","September","October","November","December"], start=1
)}

DATE_RX = re.compile(
    r"(?P<m1>Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t)?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*"
    r"(?P<y1>\d{4})\s*[-–—]\s*(?:(?P<m2>Present|Current|Now|Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t)?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*(?P<y2>\d{4})?)",
    re.I
)
YEAR_RANGE = re.compile(r"(?P<y1>\d{4})\s*[-–—]\s*(?P<y2>\d{4}|Present|Current|Now)", re.I)

def _to_month(m: str) -> int:
    if not m: return 1
    m = m.lower()
    if m in ("present","current","now"): return datetime.now().month
    for full, idx in MONTHS.items():
        if full.startswith(m):
            return idx
    return 1

def estimate_years_experience(text: str) -> int:
    spans_months = 0
    now = datetime.now()
    for m in DATE_RX.finditer(text or ""):
        m1, y1, m2, y2 = m.group("m1","y1","m2","y2")
        start = datetime(int(y1), _to_month(m1), 1)
        if not m2:
            end = now
        else:
            if m2.lower() in ("present","current","now"):
                end = now
            else:
                end = datetime(int(y2), _to_month(m2), 1)
        spans_months += max(0, (end.year - start.year) * 12 + (end.month - start.month))

    for m in YEAR_RANGE.finditer(text or ""):
        y1, y2 = m.group("y1","y2")
        start = datetime(int(y1),1,1)
        end = now if y2.lower() in ("present","current","now") else datetime(int(y2),1,1)
        spans_months += max(0, (end.year - start.year) * 12)

    return max(0, round(spans_months / 12))
