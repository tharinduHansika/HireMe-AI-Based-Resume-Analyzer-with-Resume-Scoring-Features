def rule_based_feedback(feats: dict, sections: dict) -> list[str]:
    fb = []

    if not feats["has_contact"]:
        fb.append("Add a clearly formatted contact section (name, email, phone, location, LinkedIn).")
    if not feats["has_education"]:
        fb.append("Education section is missing; include degree, institution, and graduation year.")
    if not feats["has_experience"]:
        fb.append("Add a Work Experience section summarizing role, company, dates, and achievements.")

    if feats["num_skills"] < 8:
        fb.append("Include more relevant technical skills; group by category (frontend/backend/devops).")

    if feats["quantified_achievements"] == 0:
        fb.append("Add quantified achievements (e.g., 'reduced load time by 30%').")

    read = feats["readability_flesch"]
    if read < 45:
        fb.append(f"Readability is low (Flesch {read}); simplify sentences and avoid long jargon-heavy lines.")
    elif read > 80:
        fb.append(f"Readability is very high (Flesch {read}); ensure professional tone and concise phrasing.")

    if feats["num_projects"] < 1 and not sections.get("projects","").strip():
        fb.append("Include a Projects section highlighting 1–3 impactful projects with tech stack and outcomes.")

    if feats["num_certifications"] < 1 and not sections.get("certifications","").strip():
        fb.append("Add relevant certifications if available (e.g., AWS, Azure, MongoDB).")

    if len(fb) == 0:
        fb.append("Overall structure looks strong with clear skills and quantified impact. Keep achievements concise.")

    return fb
