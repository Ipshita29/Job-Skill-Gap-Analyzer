from PyPDF2 import PdfReader
import csv
import re
import os

# reads from skills.csv and store them in a list 

def load_skills():
    skills = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "skills.csv"), "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            skills.append(row["skill"].lower())
    return skills

COMMON_SKILLS = load_skills()

# reads pdf file and coverts to plain text

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text.lower()

# tells which skill is present in the resume

def extract_skills(text):
    found = []
    text = text.lower()

    # normalize common variations
    replacements = {
        "css3": "css",
        "html5": "html",
        "reactjs": "react",
        "vuejs": "vue.js",
        "nodejs": "node.js",
        "expressjs": "express",
        "nextjs": "next.js",
        "powerbi": "power bi"
    }

    for key in replacements:
        text = text.replace(key, replacements[key])

    text = " ".join(text.split())

    for skill in COMMON_SKILLS:
        skill = skill.lower()
        skill = replacements.get(skill, skill)

        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)

    return list(set(found))

# ---------------- MAIN ANALYSIS ---------------- #

def analyze(resume_text, jd_text):

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = sorted(list(set(resume_skills) & set(jd_skills)))
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    score = 0
    if len(jd_skills) > 0:
        score = int((len(matched) / len(jd_skills)) * 100)

    # dynamic recommendations
    recommendations = []
    for skill in missing:
        recommendations.append({
            "skill": skill,
            "suggestion": f"Build a project using {skill} and add it to your resume"
        })

    return {
        "matched": matched,
        "missing": missing,
        "score": score,
        "recommendations": recommendations,
        "action_plan": generate_action_plan(missing),
        "smart_tips": generate_smart_tips(matched, missing),
        "recruiter_view": generate_recruiter_view(matched, missing, score),
        "checklist": generate_checklist(matched, missing)
    }

# compares resume and jd and give result

def generate_action_plan(missing):
    if not missing:
        return ["Your profile is well aligned. Keep improving projects and apply to roles."]

    return [
        f"Learn basics of {', '.join(missing[:2])}",
        "Build a real-world project that includes these skills or add in your existing ones",
        "Practice using these skills in real scenarios",
        "Add to resume and apply to relevant job roles"
    ]


# personalised tips
def generate_smart_tips(matched, missing):
    tips = []

    if missing:
        tips.append(f"Focus on adding skills like {', '.join(missing[:2])} through projects")

    if len(matched) > 3:
        tips.append("Highlight your strong skills clearly in your resume")

    tips.append("Use clear and impactful bullet points in your resume")

    return tips


# strengths and weaknesses
def generate_recruiter_view(matched, missing, score):
    strengths = []
    weaknesses = []

    if matched:
        strengths.append(f"Has relevant skills like {', '.join(matched[:3])}")

    if score > 70:
        strengths.append("Good match for this role")

    if missing:
        weaknesses.append(f"Missing key skills like {', '.join(missing[:2])}")

    if score < 60:
        weaknesses.append("Resume needs improvement for this role")

    return {
        "strengths": strengths if strengths else ["Basic alignment found"],
        "weaknesses": weaknesses if weaknesses else ["No major gaps, but can still improve"]
    }


# checklist
def generate_checklist(matched, missing):
    checklist = []
    for skill in missing[:2]:
        checklist.append(f"Add {skill} to your resume for this role")
    for skill in matched[:2]:
        checklist.append(f"Highlight your experience with {skill} in projects")

    return checklist