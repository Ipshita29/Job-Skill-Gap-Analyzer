import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import extract_text_from_pdf, analyze

app = Flask(__name__, static_folder="frontend", static_url_path="")
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