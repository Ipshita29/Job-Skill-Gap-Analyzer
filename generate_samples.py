from reportlab.pdfgen import canvas
import os

def create_pdf(filename, content):
    c = canvas.Canvas(filename)
    textobject = c.beginText()
    textobject.setTextOrigin(100, 750)
    textobject.setFont("Helvetica", 12)
    
    for line in content:
        textobject.textLine(line)
        
    c.drawText(textobject)
    c.showPage()
    c.save()
    print(f"Created {filename}")

resume_content = [
    "Ipshita Patel",
    "Full Stack Developer",
    "Skills: Python, JavaScript, React, HTML, CSS, SQL, Git",
    "Experience:",
    "- Developed web applications using React and Python Flask.",
    "- Managed databases with SQL.",
    "- Version control with Git."
]

jd_content = [
    "Senior Software Engineer",
    "Requirements:",
    "- 5+ years of experience with Python and React.",
    "- Expertise in AWS and Docker is a must.",
    "- Strong background in SQL and Node.js.",
    "- Experience with Kubernetes and CI/CD pipelines.",
    "- Good communication and leadership skills."
]

os.makedirs("samples", exist_ok=True)
create_pdf("samples/resume.pdf", resume_content)
create_pdf("samples/jd.pdf", jd_content)
