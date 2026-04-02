import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = None
vectorizer = None
model = None
unique_skills = []

# =
SKILL_MAP = {
    "css3": "css",
    "html5": "html",
    "javascript": "js",
    "reactjs": "react",
    "nodejs": "node",
    "expressjs": "express",
    "mongodb": "mongo"
}


def normalize_skill(skill):
    return SKILL_MAP.get(skill, skill)


def init_ml():
    global data, vectorizer, model, unique_skills

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "resumes.csv")

    data = pd.read_csv(file_path)

    # extract unique skills
    all_skills = set()
    for s_list in data["skills"].dropna():
        for s in s_list.split(","):
            all_skills.add(normalize_skill(s.strip().lower()))

    unique_skills = sorted(list(all_skills), key=len, reverse=True)

    texts = data["resume_text"]
    skills = data["skills"]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=1000)
    model.fit(X, skills)

    return data


def extract_skills_keywords(text):
    text_lower = text.lower()

    found = [
        s for s in unique_skills
        if re.search(r'\b' + re.escape(s) + r'\b', text_lower)
    ]

    return [normalize_skill(s) for s in found]


def extract_skills_ml(text):
    if model is None:
        return []

    X = vectorizer.transform([text])
    pred = model.predict(X)

    skills = [s.strip().lower() for s in pred[0].split(",")]

    return [normalize_skill(s) for s in skills]