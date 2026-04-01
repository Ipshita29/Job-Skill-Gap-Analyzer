# Job Skill Gap Analyzer

This project helps you compare your resume with a job description. It shows you which skills you already have and which ones you need to learn. It also gives you a plan to improve your resume to match the job better.

## Features
- Upload your resume and job description as PDF files.
- See a score that shows how well your skills match the job.
- See a list of skills that you already have.
- See a list of skills that are missing.
- Get advice and a step-by-step plan to improve your skills.
- Get smart tips to help highlight your strengths to recruiters.

## Project Structure
- **backend/**: This folder has the Python code for the server and the skill analysis logic.
  - `app.py`: The main server file.
  - `utils.py`: Contains the logic to read PDFs and find skills.
  - `skills.csv`: A list of common skills used for matching.
  - `requirements.txt`: A list of tools needed for the backend.
- **frontend/**: This folder has the user interface.
  - `index.html`: The main web page for the project.
- **samples/**: This folder contains example files you can use to test the project.

## How to setup the project

### Backend Setup
1. Open a terminal or command prompt.
2. Go to the `backend` folder.
3. Install the required tools by running this command: 
   `pip install -r requirements.txt`
4. Start the backend server by running this command: 
   `python app.py`
   The backend will start running on http://127.0.0.1:5000.

### Frontend Setup
1. Go to the `frontend` folder.
2. Open the `index.html` file in any web browser like Chrome or Firefox.
3. You can now start using the analyzer by uploading your files.

## Technical Details
- The backend is built using Flask and Python.
- It uses the PyPDF2 library to read text from PDF files.
- Skills are identified by matching words from the PDF against the list in `skills.csv`.
- The frontend is built with HTML, CSS, and Tailwind CSS for a modern design.
- Communication between the frontend and backend happens through a REST API.