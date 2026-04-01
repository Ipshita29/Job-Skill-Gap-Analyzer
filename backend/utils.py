from PyPDF2 import PdfReader
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ensure nltk is downloaded
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))


def load_skills():
    skills = []
    with open("skills.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            skills.append(row["skill"].lower())
    return skills

COMMON_SKILLS = load_skills()

SUGGESTIONS = {
    "python": "Master the fundamentals and explore libraries like Flask or FastAPI.",
    "react": "Build interactive UIs and understand hooks and state management.",
    "sql": "Practice complex joins, indexing, and database design on HackerRank.",
    "docker": "Learn containerization, Dockerfiles, and multi-container setups.",
    "aws": "Explore core services like EC2, S3, and Lambda functions.",
    "javascript": "Deep dive into ES6+ features and asynchronous programming.",
    "machine learning": "Study algorithms and practice with Scikit-learn or TensorFlow.",
    "git": "Learn advanced Git workflows: branching, merging, and rebasing.",
    "node.js": "Understand event-driven architecture and asynchronous I/O.",
    "kubernetes": "Learn about orchestration, pods, and service discovery.",
}

# text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()

def normalize_text(text):
    return "".join(c for c in text.lower() if c.isalnum())

def extract_skills(text):
    found = set()
    text_lower = text.lower()
    text_normalized = normalize_text(text)

    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()
        skill_normalized = normalize_text(skill)
        if skill_lower in text_lower or skill_normalized in text_normalized:
            found.add(skill)
            
    return list(found)

def analyze(resume_text, jd_text):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = sorted(list(resume_skills & jd_skills))
    missing = sorted(list(jd_skills - resume_skills))

    # ats score logic
    score = 0
    if jd_skills:
        match_rate = len(matched) / len(jd_skills)
        score = int(match_rate * 100)

    # Simple suggestions logic
    recommendations = []
    for skill in missing:
        suggestion = SUGGESTIONS.get(skill.lower(), f"Consider gaining hands-on experience with {skill}")
        recommendations.append({
            "skill": skill,
            "suggestion": suggestion
        })

    return {
        "matched": matched,
        "missing": missing,
        "score": min(100, score),
        "recommendations": recommendations,
        "summary": {
            "total_jd_skills": len(jd_skills),
            "matched_count": len(matched),
            "missing_count": len(missing)
        }
    }