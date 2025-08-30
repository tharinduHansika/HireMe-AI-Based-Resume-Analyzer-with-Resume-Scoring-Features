# backend/core/extractor.py
# Keep it simple: this module should ONLY parse structure, not scoring.
import re
from typing import Dict

def extract_structured_fields(text: str) -> Dict:
    """
    Very lightweight extractor that tries to populate fields; validator.py will refine.
    """
    fields: Dict = {}

    # naive job role: first line with 'developer|engineer|designer|analyst'
    first_lines = [l.strip() for l in text.splitlines() if l.strip()]
    for ln in first_lines[:10]:
        if re.search(r"\b(developer|engineer|designer|analyst|manager)\b", ln, re.I):
            fields["job_role"] = ln.strip()
            break

    # capture explicit "X years" if present
    m = re.search(r"(\d+)\s*\+?\s*(?:years?|yrs)\b", text, re.I)
    if m:
        try:
            fields["experience_years"] = float(m.group(1))
        except:
            pass

    # crude projects count
    fields["projects_count"] = None  # let validator compute

    # try to keep education lines near the word "Education"
    edu = []
    chunks = text.splitlines()
    for i, ln in enumerate(chunks):
        if re.search(r"\beducation\b", ln, re.I):
            for j in range(i+1, min(i+8, len(chunks))):
                s = chunks[j].strip()
                if not s:
                    break
                edu.append(s)
            break
    if edu:
        fields["education"] = edu

    # certifications near "Certification"
    certs = []
    for i, ln in enumerate(chunks):
        if re.search(r"\b(certification|certifications|certificates)\b", ln, re.I):
            for j in range(i+1, min(i+8, len(chunks))):
                s = chunks[j].strip()
                if not s:
                    break
                certs.append(s)
            break
    if certs:
        fields["certifications"] = certs

    return fields
