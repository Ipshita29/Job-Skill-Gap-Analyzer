import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# --- SIMPLE ML COMPONENTS ---
# Global variables to store our trained model across the app
vectorizer = TfidfVectorizer(stop_words='english', max_features=1500)
classifier = LogisticRegression(C=5, max_iter=1000)
dataset_df = None

def clean_text(text):
    """
    Cleans text by lowercasing and removing special characters.
    Keeps . # + for technical skills (node.js, c++, c#).
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\.#+]', ' ', text)
    return " ".join(text.split())

def init_ml():
    """
    Trains a simple Logistic Regression model on startup.
    Labels are predicted as entire comma-separated skill strings.
    """
    global dataset_df, vectorizer, classifier
    
    # Path to local CSV dataset
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", "resumes.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset {csv_path} not found!")
        return None

    # 1. Load Dataset
    dataset_df = pd.read_csv(csv_path)
    dataset_df["resume_text"] = dataset_df["resume_text"].apply(clean_text)
    
    # 2. Extract Features (Text -> Numbers)
    X = vectorizer.fit_transform(dataset_df["resume_text"])
    
    # 3. Define Labels (The skills string column)
    # We treat the entire skill list as a single label for simplicity
    y = dataset_df["skills"].fillna("")
    
    # 4. Train Model
    classifier.fit(X, y)
    
    print(f"ML Training Complete. Learned from {len(dataset_df)} profiles.")
    return dataset_df

def extract_skills_ml(text):
    """
    Predicts the skills string and splits it into a list.
    """
    if not text or dataset_df is None:
        return []

    # Clean input and transform to vector
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    
    # Predict the skills matching this text
    # predict() returns the most likely skill string from the training data
    skills_string = classifier.predict(vector)[0]
    
    # Return as a clean list of individual skills
    if not skills_string:
        return []
        
    return [s.strip().lower() for s in str(skills_string).split(',') if s.strip()]
