from sentence_transformers import SentenceTransformer, util
import numpy as np
from model import extract_skills_ml

model = SentenceTransformer('all-MiniLM-L6-v2')
dataset = None
embeddings = None

def init_recommender(df):
    global dataset, embeddings
    dataset = df
    texts = df["resume_text"].tolist()
    # make embeddings
    embeddings = model.encode(texts, convert_to_tensor=True)

def get_ai_recommendations(user_text, jd_text):
    if embeddings is None:
        return []

    # JD → find similar resumes
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    scores = util.cos_sim(jd_emb, embeddings)[0]
    top5 = np.argsort(-scores.cpu().numpy())[:5]

    # user → compare with those
    user_emb = model.encode(user_text, convert_to_tensor=True)
    scores2 = util.cos_sim(user_emb, embeddings[top5])[0]
    top3 = np.argsort(-scores2.cpu().numpy())[:3]

    # get skills
    user_skills = set(extract_skills_ml(user_text))
    suggestions = []
    for i in top3:
        text = dataset.iloc[top5[i]]["resume_text"]
        skills = extract_skills_ml(text)
        for s in skills:
            if s not in user_skills:
                suggestions.append(s)
    suggestions = list(set(suggestions))[:5]
    return [
        {"skill": s, "suggestion": f"Try adding {s} to your profile"}
        for s in suggestions
    ]

def compute_similarity_score(t1, t2):
    e1 = model.encode(t1, convert_to_tensor=True)
    e2 = model.encode(t2, convert_to_tensor=True)
    score = util.cos_sim(e1, e2).item()
    return int(score * 100)