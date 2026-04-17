# Job Skill Gap Analyzer

A full-stack web application that compares a resume with a job description to identify skill gaps and provide actionable insights for improving job readiness.

---

## Features

* Upload resume and job description (PDF)
* Get a skill match score
* View matched and missing skills
* Receive improvement suggestions and tips

---

## Tech Stack

* **Frontend:** React (Vite), Tailwind CSS
* **Backend:** Flask (Python)
* **ML/NLP:** TF-IDF, Logistic Regression
* **Deployment:** Vercel (Frontend), Railway (Backend)

---

## Project Structure

```
backend/
  app.py
  utils.py
  skills.csv
  requirements.txt

frontend/
  src/
  index.html

samples/
```

---

## Local Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

### Frontend (React)

```bash
cd frontend/react-app
npm install
npm run dev
```

---

## Deployment

* **Frontend:** Deployed on Vercel
* **Backend:** Deployed on Railway

Update API in frontend:

```js
fetch("https://your-railway-url/analyze")
```

---

##  How it Works

* Extracts text from PDFs using PyPDF2
* Applies NLP techniques to identify skills
* Compares with job requirements
* Generates match score and recommendations

---

