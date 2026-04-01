from PyPDF2 import PdfReader
import csv
import nltk
import re
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def load_skills():
    """Reads skills from CSV and returns a list."""
    skills = []
    try:
        with open("skills.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["skill"]:
                    skills.append(row["skill"].strip())
    except Exception:
        pass
    return skills

COMMON_SKILLS = load_skills()

SUGGESTIONS = {
    "python": "Master the fundamentals and explore libraries like Flask or FastAPI.",
    "react": "Build interactive UIs and understand hooks and state management.",
    "sql": "Practice complex joins, indexing, and database design on HackerRank.",
    "docker": "Learn containerization, Dockerfiles, and multi-container setups.",
    "aws": "Explore core services like EC2, S3, and Lambda functions.",
    "javascript": "Deep dive into ES6+ features and asynchronous programming.",
    "machine learning": "Study algorithms and practice with Scikit-learn or TensorFlow.",
    "git": "Learn advanced Git workflows: branching, merging, and rebasing.",
    "node.js": "Understand event-driven architecture and asynchronous I/O.",
    "kubernetes": "Learn about orchestration, pods, and service discovery.",
}

def extract_text_from_pdf(file):
    """Extracts text from a PDF file object."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

def extract_skills(text):
    """
    Extracts skills using strict regex matching with word boundaries.
    Handles variations like 'node.js' vs 'nodejs' safely.
    """
    found = set()
    text_lower = text.lower()
    
    # Remove extra whitespace and noise for cleaner matching
    text_clean = " ".join(text_lower.split())

    for skill in COMMON_SKILLS:
        skill_lower = skill.lower().strip()
        if not skill_lower:
            continue
            
        # Create variations for the skill
        variations = [skill_lower]
        if "." in skill_lower:
            variations.append(skill_lower.replace(".", ""))
        if "-" in skill_lower:
            variations.append(skill_lower.replace("-", " "))
            variations.append(skill_lower.replace("-", ""))
            
        for var in variations:
            # \b ensures we match 'git' but NOT 'digital'
            pattern = rf'\b{re.escape(var)}\b'
            if re.search(pattern, text_clean):
                found.add(skill)
                break
                
    return sorted(list(found))

def analyze(resume_text, jd_text):
    """
    Compares resume skills against JD skills and calculates ATS score.
    """
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = sorted(list(resume_skills & jd_skills))
    missing = sorted(list(jd_skills - resume_skills))

    score = 0
    if jd_skills:
        score = int((len(matched) / len(jd_skills)) * 100)

    recommendations = []
    for skill in missing:
        suggestion = SUGGESTIONS.get(skill.lower(), f"Focus on learning and applying {skill} in real-world projects.")
        recommendations.append({
            "skill": skill,
            "suggestion": suggestion
        })

    return {
        "matched": matched,
        "missing": missing,
        "score": min(100, score),
        "recommendations": recommendations,
        "action_plan": generate_action_plan(missing),
        "smart_tips": generate_smart_tips(matched, missing),
        "recruiter_view": generate_recruiter_view(matched, missing, score),
        "checklist": generate_upgrade_checklist(matched, missing),
        "summary": {
            "total_jd_skills": len(jd_skills),
            "matched_count": len(matched),
            "missing_count": len(missing)
        }
    }

def generate_action_plan(missing_skills):
    """
    Generates a sequential weekly learning roadmap based on missing_skills.
    """
    plan = []
    if not missing_skills:
        return ["You're already a great match! Consider deepening your expertise in your core stack."]
        
    for i, skill in enumerate(missing_skills[:4]): 
        start_week = (i * 3) + 1
        plan.append(f"Week {start_week}: Learn {skill} basics")
        plan.append(f"Week {start_week + 1}: Build a small project using {skill}")
        plan.append(f"Week {start_week + 2}: Add {skill} project to resume")
            
    return plan

def generate_smart_tips(matched_skills, missing_skills):
    """
    Generates personalized, actionable resume improvement tips.
    """
    tips = []
    
    SKILL_ADVICE = {
        "react": "Add 1 React project featuring complex state management and API integration.",
        "node.js": "Mention backend experience specifically with Node.js, Express, and RESTful APIs.",
        "javascript": "Focus on ES6+ features and showcase asynchronous programming patterns.",
        "sql": "Highlight experience with database schema design and complex query optimization.",
        "docker": "Include a project where you containerized a multi-service application.",
        "aws": "Mention specific AWS services used, such as EC2, S3, or Lambda.",
        "python": "Showcase Python projects that involve data processing or backend automation.",
        "git": "Explicitly mention experience with Git workflows like rebasing and Pull Request reviews."
    }

    if missing_skills:
        for skill in missing_skills[:2]:
            skill_lower = skill.lower()
            if skill_lower in SKILL_ADVICE:
                tips.append(SKILL_ADVICE[skill_lower])
            else:
                tips.append(f"Build a portfolio project centered around {skill} to demonstrate practical proficiency.")

    if "docker" in missing_skills or "aws" in missing_skills or not any(s in matched_skills for s in ["docker", "aws"]):
        tips.append("Include deployment experience using platforms like Vercel, Netlify, or AWS.")

    if matched_skills:
        primary = matched_skills[0]
        tips.append(f"Add measurable achievements related to {primary} (e.g., 'Reduced latency by 15%').")

    tips.append("Use a clean, single-column resume layout to ensure 100% ATS readability.")
    
    return tips[:5]

def generate_recruiter_view(matched, missing, score):
    """
    Simulates how a recruiter would evaluate the resume.
    """
    strengths = []
    weaknesses = []
    
    # Strengths logic
    if len(matched) > 5:
        strengths.append("Strong technical alignment with the specified job requirements.")
    if score > 70:
        strengths.append(f"High ATS compatibility score ({score}%), indicating a well-optimized resume.")
    
    # Mention specific key technologies if matched
    key_tech = ["react", "python", "javascript", "sql", "node.js"]
    found_key = [s for s in matched if s.lower() in key_tech]
    if found_key:
        strengths.append(f"Demonstrates core proficiency in essential tools: {', '.join(found_key[:3])}.")

    # Weaknesses logic
    if score < 50:
        weaknesses.append("Match score is below the ideal threshold for highly competitive roles.")
    if len(missing) > 5:
        weaknesses.append("Significant gaps identified in several required technical competencies.")
        
    # Mention missing domains
    missing_lower = [s.lower() for s in missing]
    if any(s in missing_lower for s in ["aws", "docker", "kubernetes", "cloud"]):
        weaknesses.append("Limited exposure to cloud architecture or containerization tools.")
    if any(s in missing_lower for s in ["node.js", "python", "sql", "backend"]):
        weaknesses.append("Backend engineering and database management gaps noted.")

    return {
        "strengths": strengths if strengths else ["Showing baseline alignment. Focus on adding more matched skills."],
        "weaknesses": weaknesses if weaknesses else ["Internal evaluation complete. No critical weaknesses identified."]
    }

def generate_upgrade_checklist(matched, missing):
    """
    Generates an actionable checklist for resume improvement.
    """
    checklist = []
    
    # Add items based on missing skills
    for skill in missing[:3]:
        checklist.append(f"Add {skill} to your 'Skills' section with a corresponding project or experience bullet point.")
        
    # Generic high-value improvements
    missing_lower = [s.lower() for s in missing]
    if not any(s in missing_lower for s in ["vercel", "netlify", "aws", "deployment"]):
        # If they haven't mentioned deployment, suggest it
        if not any(s in [m.lower() for m in matched] for s in ["vercel", "netlify", "aws", "deployment"]):
            checklist.append("Include deployment experience using modern platforms like Netlify, Vercel, or GitHub Pages.")
            
    if any(s in missing_lower for s in ["node.js", "express", "backend"]):
        checklist.append("Build and link at least one backend-focused project using Node.js or Python.")
        
    if len(matched) < 5:
        checklist.append("Add 1–2 more technical projects to showcase your practical application of core skills.")
    
    checklist.append("Scan for measurable achievements (metrics, %, saved time) and add them to your experience bullet points.")
    
    return checklist[:6]