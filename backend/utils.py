from PyPDF2 import PdfReader
import os
from model import init_ml, extract_skills_ml, extract_skills_keywords
from recommender import init_recommender, compute_similarity_score, get_ai_recommendations

# --- STARTUP INITIALIZATION ---
# This ensures the model is trained in-memory when the backend is loaded.
try:
    print("Pre-training ML model in-memory...")
    df = init_ml()
    init_recommender(df)
    print("Backend AI ready.")
except Exception as e:
    print(f"Error during ML initialization: {e}")

# reads pdf file and coverts to plain text

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

#analysis part 

def analyze(resume_text, jd_text):
    # Minimal accuracy fix: Use keyword matching for precise results
    resume_skills = extract_skills_keywords(resume_text)
    jd_skills = extract_skills_keywords(jd_text)

    matched = sorted(list(set(resume_skills) & set(jd_skills)))
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    # IA Scoring (Semantic SBERT Similarity)
    score = int(compute_similarity_score(resume_text, jd_text))
    recommendations = get_ai_recommendations(resume_text, jd_text)

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
        f"Master the {', '.join(missing[:2])} skills through hands-on practice",
        "Build complex projects incorporating these missing technologies",
        "Update your resume with specific achievements in these areas",
        "Apply to roles demonstrating your advanced skill set"
    ]


# personalised tips
def generate_smart_tips(matched, missing):
    tips = []

    if missing:
        tips.append(f"Focus on bridging the gap in {', '.join(missing[:2])}")

    if len(matched) > 3:
        tips.append("Your technical foundation is strong in several areas")

    tips.append("Quantify your project impact in your resume bullet points")

    return tips


# strengths and weaknesses
def generate_recruiter_view(matched, missing, score):
    strengths = []
    weaknesses = []

    if matched:
        strengths.append(f"Exhibits proficiency in {', '.join(matched[:3])}")

    if score > 75:
        strengths.append("Exceptional alignment with role requirements")

    if missing:
        weaknesses.append(f"Gaps identified in {', '.join(missing[:2])}")

    if score < 50:
        weaknesses.append("Significant skill gaps for this specific JD")

    return {
        "strengths": strengths if strengths else ["Potential talent alignment"],
        "weaknesses": weaknesses if weaknesses else ["High-performing profile with minor gaps"]
    }


# checklist
def generate_checklist(matched, missing):
    checklist = []
    for skill in missing[:2]:
        checklist.append(f"Gain certification or build a project for {skill}")
    for skill in matched[:2]:
        checklist.append(f"Peer-review your projects involving {skill}")

    return checklist