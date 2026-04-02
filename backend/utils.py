from PyPDF2 import PdfReader
from model import init_ml, extract_skills_ml, extract_skills_keywords

# Lazy initialization
initialized = False


def ensure_initialized():
    global initialized
    if not initialized:
        print("Initializing ML model...")
        init_ml()
        initialized = True
        print("ML ready.")


# extract text from PDF
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text.lower()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""


# main analysis
def analyze(resume_text, jd_text):

    ensure_initialized()

    resume_skills = extract_skills_keywords(resume_text)
    jd_skills = extract_skills_keywords(jd_text)

    # ML prediction
    resume_ml_skills = extract_skills_ml(resume_text)

    # combine keyword + ML
    resume_all_skills = set(resume_skills + resume_ml_skills)

    matched = sorted(list(resume_all_skills & set(jd_skills)))
    missing = sorted(list(set(jd_skills) - resume_all_skills))

    # score
    score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    # recommendations
    recommendations = [
        {"skill": s, "suggestion": f"Learn {s} through projects"}
        for s in missing[:5]
    ]

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


def generate_action_plan(missing):
    if not missing:
        return ["Your profile is well aligned. Keep improving projects and apply to roles."]

    return [
        f"Master {', '.join(missing[:2])} through practice",
        "Build projects using these skills",
        "Update resume with measurable impact",
        "Apply to relevant roles"
    ]


def generate_smart_tips(matched, missing):
    tips = []

    if missing:
        tips.append(f"Focus on learning {', '.join(missing[:2])}")

    if len(matched) > 3:
        tips.append("You have a strong technical base")

    tips.append("Quantify achievements in your resume")

    return tips


def generate_recruiter_view(matched, missing, score):
    strengths = []
    weaknesses = []

    if matched:
        strengths.append(f"Strong in {', '.join(matched[:3])}")

    if score > 75:
        strengths.append("Good match for the role")

    if missing:
        weaknesses.append(f"Missing {', '.join(missing[:2])}")

    if score < 50:
        weaknesses.append("Needs improvement for this role")

    return {
        "strengths": strengths if strengths else ["Decent profile"],
        "weaknesses": weaknesses if weaknesses else ["Minor gaps"]
    }


def generate_checklist(matched, missing):
    checklist = []

    for skill in missing[:2]:
        checklist.append(f"Build a project using {skill}")

    for skill in matched[:2]:
        checklist.append(f"Improve projects using {skill}")

    return checklist