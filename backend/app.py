from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import extract_text_from_pdf, analyze

app = Flask(__name__)
CORS(app) 

@app.route('/analyze', methods=['POST'])
def analyze_files():
    resume_file = request.files['resume']
    jd_file = request.files['jd']

    resume_text = extract_text_from_pdf(resume_file)
    jd_text = extract_text_from_pdf(jd_file)

    result = analyze(resume_text, jd_text)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)