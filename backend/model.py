import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = None
vectorizer = None
model = None
unique_skills = []


def init_ml():
    global data, vectorizer, model, unique_skills
    data = pd.read_csv("data/resumes.csv")
    
    # Store unique skills from database for keyword matching
    all_skills = set()
    for s_list in data["skills"].dropna():
        for s in s_list.split(","):
            all_skills.add(s.strip().lower())
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
    return [s for s in unique_skills if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]


def extract_skills_ml(text):
    if model is None:
        return []
    X = vectorizer.transform([text])
    pred = model.predict(X)

    # convert "python,react" → ["python","react"]
    return [s.strip().lower() for s in pred[0].split(",")]