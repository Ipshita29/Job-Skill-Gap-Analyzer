from PyPDF2 import PdfReader
import csv
import re

# ---------------- LOAD SKILLS ---------------- #

def load_skills():
    skills = []
    with open("skills.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            skills.append(row["skill"].lower())
    return skills

COMMON_SKILLS = load_skills()

# ---------------- SUGGESTIONS ---------------- #

SUGGESTIONS = {
    "python": "Practice Python and build projects",
    "react": "Build React apps with API integration",
    "sql": "Practice queries and database design",
    "docker": "Learn Docker basics",
    "aws": "Learn EC2 and deployment",
}

# ---------------- PDF TEXT ---------------- #

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text.lower()

# ---------------- SKILL EXTRACTION ---------------- #

def extract_skills(text):
    found = []
    text = text.lower()

    # 🔥 normalize variations
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

    # recommendations
    recommendations = []
    for skill in missing:
        recommendations.append({
            "skill": skill,
            "suggestion": SUGGESTIONS.get(skill, f"Learn {skill} and build a project")
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

# ---------------- FEATURES ---------------- #

def generate_action_plan(missing):
    plan = []

    for i, skill in enumerate(missing[:3]):
        plan.append(f"Week {i*3+1}: Learn {skill}")
        plan.append(f"Week {i*3+2}: Build project using {skill}")
        plan.append(f"Week {i*3+3}: Add {skill} to resume")

    return plan


def generate_smart_tips(matched, missing):
    tips = []

    for skill in missing[:2]:
        tips.append(f"Add a project using {skill}")

    if "react" in matched:
        tips.append("Improve your React project with API integration")

    tips.append("Add deployment (Vercel / Netlify)")

    return tips


def generate_recruiter_view(matched, missing, score):
    strengths = []
    weaknesses = []

    if matched:
        strengths.append(f"Has relevant skills like {', '.join(matched[:3])}")

    if score > 70:
        strengths.append("Good match for this role")

    if missing:
        weaknesses.append(f"Missing key skills like {', '.join(missing[:3])}")

    if score < 60:
        weaknesses.append("ATS score is low, resume needs improvement")

    return {
        "strengths": strengths if strengths else ["Basic alignment found"],
        "weaknesses": weaknesses if weaknesses else ["No major gaps, but can still improve"]
    }


def generate_checklist(matched, missing):
    checklist = []

    for skill in missing[:3]:
        checklist.append(f"Add {skill} to resume")

    checklist.append("Add 1–2 strong projects")
    checklist.append("Include measurable achievements")

    return checklist