import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import extract_text_from_pdf, analyze

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_files():
    
    resume_file = request.files['resume']
    jd_file = request.files['jd']

    resume_text = extract_text_from_pdf(resume_file)
    jd_text = extract_text_from_pdf(jd_file)

    result = analyze(resume_text, jd_text)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5001)