from PyPDF2 import PdfReader
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

# load skills from CSV
def load_skills():
    skills = []
    with open("skills.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            skills.append(row["skill"].lower())
    return skills

COMMON_SKILLS = load_skills()

SUGGESTIONS = {
    "python": "Practice Python and solve coding problems",
    "react": "Build small projects using React",
    "sql": "Practice queries on platforms like HackerRank",
    "docker": "Learn Docker basics and containers",
    "aws": "Start with AWS EC2 and S3"
}

# extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()

# extract skills using NLP + keyword matching
def extract_skills(text):
    words = word_tokenize(text)
    filtered = [w for w in words if w not in stop_words]

    found = []
    text_lower = text.lower()

    for skill in COMMON_SKILLS:
        if skill in text_lower or skill.replace(".", "") in text_lower:
            found.append(skill)

    return list(set(found))

# main analysis logic
def analyze(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = 0
    if len(jd_skills) > 0:
        score = int((len(matched) / len(jd_skills)) * 100)

    recommendations = {}
    for skill in missing:
        if skill in SUGGESTIONS:
            recommendations[skill] = SUGGESTIONS[skill]

    return {
        "matched": matched,
        "missing": missing,
        "score": score,
        "recommendations": recommendations
    }