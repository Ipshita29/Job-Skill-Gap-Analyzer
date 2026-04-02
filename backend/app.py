import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import extract_text_from_pdf, analyze

# absolute path to frontend (outside backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Serve frontend
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')


# API route
@app.route('/analyze', methods=['POST'])
def analyze_files():
    
    resume_file = request.files['resume']
    jd_file = request.files['jd']

    resume_text = extract_text_from_pdf(resume_file)
    jd_text = extract_text_from_pdf(jd_file)

    result = analyze(resume_text, jd_text)

    return jsonify(result)

# IMPORTANT FOR DEPLOYMENT
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)