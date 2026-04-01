import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = None
vectorizer = None
model = None


def init_ml():
    global data, vectorizer, model
    data = pd.read_csv("data/resumes.csv")
    texts = data["resume_text"]
    skills = data["skills"]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, skills)
    return data


def extract_skills_ml(text):
    if model is None:
        return []
    X = vectorizer.transform([text])
    pred = model.predict(X)

    # convert "python,react" → ["python","react"]
    return pred[0].split(",")