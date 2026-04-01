from PyPDF2 import PdfReader
import csv
import nltk
import re
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def load_skills():
    """Reads skills from CSV and returns a list."""
    skills = []
    try:
        with open("skills.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["skill"]:
                    skills.append(row["skill"].strip())
    except Exception:
        pass
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

def extract_text_from_pdf(file):
    """Extracts text from a PDF file object."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

def extract_skills(text):
    """
    Extracts skills using strict regex matching with word boundaries.
    Handles variations like 'node.js' vs 'nodejs' safely.
    """
    found = set()
    text_lower = text.lower()
    
    # Remove extra whitespace and noise for cleaner matching
    text_clean = " ".join(text_lower.split())

    for skill in COMMON_SKILLS:
        skill_lower = skill.lower().strip()
        if not skill_lower:
            continue
            
        # Create variations for the skill
        variations = [skill_lower]
        if "." in skill_lower:
            variations.append(skill_lower.replace(".", ""))
        if "-" in skill_lower:
            variations.append(skill_lower.replace("-", " "))
            variations.append(skill_lower.replace("-", ""))
            
        for var in variations:
            # \b ensures we match 'git' but NOT 'digital'
            # re.escape handles special characters like '.' in 'node.js'
            pattern = rf'\b{re.escape(var)}\b'
            if re.search(pattern, text_clean):
                found.add(skill)
                break
                
    return sorted(list(found))

def analyze(resume_text, jd_text):
    """
    Compares resume skills against JD skills and calculates ATS score.
    """
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = sorted(list(resume_skills & jd_skills))
    missing = sorted(list(jd_skills - resume_skills))

    score = 0
    if jd_skills:
        score = int((len(matched) / len(jd_skills)) * 100)

    recommendations = []
    for skill in missing:
        suggestion = SUGGESTIONS.get(skill.lower(), f"Focus on learning and applying {skill} in real-world projects.")
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