import numpy as np
from model import extract_skills_ml

model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


data = None
emb = None

def init_recommender(df):
    global data, emb
    data = df

    model = get_model()  
    emb = model.encode(df["resume_text"].tolist(), convert_to_tensor=True)


def get_ai_recommendations(user, jd):
    from sentence_transformers import util  

    if emb is None:
        return []

    model = get_model()  

    # step 1
    jd_scores = util.cos_sim(model.encode(jd, convert_to_tensor=True), emb)[0]
    top5 = np.argsort(-jd_scores.cpu().numpy())[:5]

    # step 2
    user_scores = util.cos_sim(model.encode(user, convert_to_tensor=True), emb[top5])[0]
    top3 = np.argsort(-user_scores.cpu().numpy())[:3]

    # step 3
    user_skills = set(extract_skills_ml(user))
    suggestions = []

    for i in top3:
        text = data.iloc[top5[i]]["resume_text"]
        for skill in extract_skills_ml(text):
            if skill not in user_skills:
                suggestions.append(skill)

    suggestions = list(set(suggestions))[:5]

    return [{"skill": s, "suggestion": f"Add {s} to improve your profile"} for s in suggestions]


def compute_similarity_score(a, b):
    from sentence_transformers import util  

    model = get_model() 

    score = util.cos_sim(
        model.encode(a, convert_to_tensor=True),
        model.encode(b, convert_to_tensor=True)
    ).item()

    return int(score * 100)