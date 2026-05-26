from flask import Flask, render_template, request, send_file
import pdfplumber
import os
import random
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills Database
skills_list = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",
    "artificial intelligence",
    "flask",
    "react",
    "django",
    "mongodb",
    "data analysis"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check Upload
    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    # Save Resume
    filename = "uploaded_resume.pdf"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    # Get Job Description
    job_description = request.form.get(
        "job_description",
        ""
    ).lower()

    # Extract Resume Text
    resume_text = ""

    try:

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    resume_text += text.lower()

    except:
        return "Please upload a valid PDF resume."

    # Detect Skills
    found_skills = []

    for skill in skills_list:

        if skill in resume_text:
            found_skills.append(skill)

    # ATS Score
    ats_score = min(len(found_skills) * 10, 100)

    # Match Skills
    matched_skills = []
    missing_skills = []

    for skill in skills_list:

        if skill in job_description:

            if skill in found_skills:
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

    # Match Score
    if len(matched_skills) + len(missing_skills) > 0:

        match_score = int(

            (
                len(matched_skills)
                /
                (
                    len(matched_skills)
                    + len(missing_skills)
                )
            ) * 100

        )

    else:

        match_score = 0

    # Skill Percentages
    skill_percentages = {}

    for skill in found_skills:

        skill_percentages[skill] = random.randint(70, 95)

    # AI Suggestions
    suggestions = []

    if "python" not in found_skills:
        suggestions.append(
            "Add Python projects to strengthen your resume."
        )

    if "machine learning" not in found_skills:
        suggestions.append(
            "Learn Machine Learning basics and add projects."
        )

    if "flask" not in found_skills:
        suggestions.append(
            "Build Flask web applications for better ATS ranking."
        )

    if "sql" not in found_skills:
        suggestions.append(
            "Add SQL/database skills."
        )

    if len(found_skills) >= 7:
        suggestions.append(
            "Excellent technical skillset!"
        )

    if match_score >= 80:
        suggestions.append(
            "Your resume is highly optimized for this role."
        )

    # Recommended Roles
    recommended_roles = []

    if "python" in found_skills:
        recommended_roles.append(
            "Python Developer"
        )

    if "machine learning" in found_skills:
        recommended_roles.append(
            "Machine Learning Intern"
        )

    if "artificial intelligence" in found_skills:
        recommended_roles.append(
            "AI Engineer Intern"
        )

    if "html" in found_skills or "css" in found_skills:
        recommended_roles.append(
            "Frontend Developer"
        )

    if "sql" in found_skills:
        recommended_roles.append(
            "Data Analyst"
        )

    if "react" in found_skills:
        recommended_roles.append(
            "React Developer"
        )

    # Generate PDF Report
    pdf_path = "resume_report.pdf"

    c = canvas.Canvas(pdf_path)

    c.setFont("Helvetica-Bold", 22)
    c.drawString(160, 800, "AI Resume Report")

    c.setFont("Helvetica", 14)

    c.drawString(
        50,
        760,
        f"ATS Resume Score: {ats_score}%"
    )

    c.drawString(
        50,
        730,
        f"Job Match Score: {match_score}%"
    )

    # Skills
    y = 690

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Detected Skills:")

    y -= 30

    c.setFont("Helvetica", 13)

    for skill in found_skills:

        c.drawString(
            70,
            y,
            f"- {skill}"
        )

        y -= 20

    # Matched Skills
    y -= 20

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Matched Skills:")

    y -= 30

    c.setFont("Helvetica", 13)

    for skill in matched_skills:

        c.drawString(
            70,
            y,
            f"- {skill}"
        )

        y -= 20

    # Missing Skills
    y -= 20

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Missing Skills:")

    y -= 30

    c.setFont("Helvetica", 13)

    for skill in missing_skills:

        c.drawString(
            70,
            y,
            f"- {skill}"
        )

        y -= 20

    # Suggestions
    y -= 20

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI Suggestions:")

    y -= 30

    c.setFont("Helvetica", 13)

    for suggestion in suggestions:

        c.drawString(
            70,
            y,
            f"- {suggestion}"
        )

        y -= 20

    c.save()

    # Render HTML Page
    return render_template(

        "index.html",

        score=ats_score,

        skills=found_skills,

        matched=matched_skills,

        missing=missing_skills,

        roles=recommended_roles,

        suggestions=suggestions,

        skill_percentages=skill_percentages,

        match_score=match_score
    )


@app.route("/download-report")
def download_report():

    return send_file(
        "resume_report.pdf",
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(debug=True)
