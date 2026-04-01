import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import extract_text_from_pdf, analyze

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

@app.route('/analyze', methods=['POST'])
def analyze_files():
    """
    Endpoint to receive resume and job description PDFs, 
    extract text, and return skill gap analysis.
    """
    try:
        if 'resume' not in request.files or 'jd' not in request.files:
            return jsonify({"error": "Missing resume or job description file"}), 400

        resume_file = request.files['resume']
        jd_file = request.files['jd']

        logger.info(f"Analyzing resume: {resume_file.filename} and JD: {jd_file.filename}")

        resume_text = extract_text_from_pdf(resume_file)
        jd_text = extract_text_from_pdf(jd_file)

        if not resume_text or not jd_text:
            return jsonify({"error": "Could not extract text from one or both files. Ensure they are valid PDFs."}), 400

        result = analyze(resume_text, jd_text)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({"error": "An internal error occurred during analysis."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)