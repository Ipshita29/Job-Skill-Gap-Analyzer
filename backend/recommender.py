from sentence_transformers import SentenceTransformer, util
import numpy as np
from model import extract_skills_ml

# Initialise SBERT (MiniLM is small and fast)
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

dataset_embeddings = None
raw_dataset_df = None

def init_recommender(df):
    """
    Precomputes embeddings for the dataset once on startup.
    """
    global dataset_embeddings, raw_dataset_df
    raw_dataset_df = df
    
    if df is not None:
        texts = df["resume_text"].tolist()
        dataset_embeddings = sbert_model.encode(texts, convert_to_tensor=True)
        print("SBERT Embeddings Precomputed.")

def get_ai_recommendations(user_resume_text, jd_text):
    """
    Finds similar profiles and suggests missing skills.
    """
    if dataset_embeddings is None or raw_dataset_df is None:
        return []

    # 1. Detect Role: Find top 5 profiles most similar to the Job Description
    jd_embedding = sbert_model.encode(jd_text, convert_to_tensor=True)
    jd_similarities = util.cos_sim(jd_embedding, dataset_embeddings)[0]
    top_5_indices = np.argsort(-jd_similarities.cpu().numpy())[:5]
    
    # 2. Match Peer: Find top 3 from those 5 most similar to the user's resume
    user_embedding = sbert_model.encode(user_resume_text, convert_to_tensor=True)
    top_5_embeddings = dataset_embeddings[top_5_indices]
    
    user_similarities = util.cos_sim(user_embedding, top_5_embeddings)[0]
    top_3_sub_indices = np.argsort(-user_similarities.cpu().numpy())[:3]
    
    # 3. Dynamic Skills: Get skills from these peers using our ML model
    top_3_final_indices = [top_5_indices[i] for i in top_3_sub_indices]
    user_skills = set(extract_skills_ml(user_resume_text))
    
    suggested_skills = []
    for idx in top_3_final_indices:
        peer_text = raw_dataset_df.iloc[idx]["resume_text"]
        peer_skills = extract_skills_ml(peer_text)
        
        for skill in peer_skills:
            if skill not in user_skills:
                suggested_skills.append(skill)
    
    # Deduplicate and limit
    final_list = list(set(suggested_skills))[:5]
    
    return [{"skill": s, "suggestion": f"Based on top profiles for this role, add {s}."} for s in final_list]

def compute_similarity_score(text1, text2):
    """
    Returns semantic similarity as a percentage.
    """
    emb1 = sbert_model.encode(text1, convert_to_tensor=True)
    emb2 = sbert_model.encode(text2, convert_to_tensor=True)
    similarity = util.cos_sim(emb1, emb2)
    return int(float(similarity.item()) * 100)
