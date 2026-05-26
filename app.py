from flask import Flask, render_template, request, send_file
import pdfplumber
import os
import random

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Global Variables

score = 0
match_score = 0
found_skills = []
matched_skills = []
missing_skills = []
recommended_roles = []
suggestions = []

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
    "flask"
]


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    global score
    global match_score
    global found_skills
    global matched_skills
    global missing_skills
    global recommended_roles
    global suggestions

    # Check Upload

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    # Save Resume

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract Text From PDF

    text = ""

    try:

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted.lower()

    except:

        return "Please upload a valid PDF resume."

    # Job Description

    job_description = request.form.get(
        "job_description",
        ""
    ).lower()

    # Detect Skills

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    # ATS Score

    score = min(len(found_skills) * 10, 100)

    # Match Analysis

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

    # Suggestions

    suggestions = []

    if score < 50:

        suggestions.append(
            "Add more technical skills."
        )

        suggestions.append(
            "Improve project experience."
        )

        suggestions.append(
            "Include certifications."
        )

    elif score < 80:

        suggestions.append(
            "Add more projects."
        )

        suggestions.append(
            "Improve resume formatting."
        )

    else:

        suggestions.append(
            "Excellent resume!"
        )

        suggestions.append(
            "You are ready for internships."
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

    return render_template(

        "index.html",

        skills=found_skills,

        score=score,

        suggestions=suggestions,

        skill_percentages=skill_percentages,

        recommended_roles=recommended_roles,

        filename=file.filename,

        match_score=match_score,

        matched_skills=matched_skills,

        missing_skills=missing_skills
    )


@app.route("/download-report")
def download_report():

    pdf_path = "resume_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    # Title

    title = Paragraph(
        "AI Resume Analysis Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # ATS Score

    ats = Paragraph(
        f"<b>ATS Resume Score:</b> {score}%",
        styles['BodyText']
    )

    elements.append(ats)

    elements.append(Spacer(1, 12))

    # Match Score

    match = Paragraph(
        f"<b>Job Match Score:</b> {match_score}%",
        styles['BodyText']
    )

    elements.append(match)

    elements.append(Spacer(1, 20))

    # Skills

    skills_text = ", ".join(found_skills)

    skills_para = Paragraph(
        f"<b>Detected Skills:</b><br/>{skills_text}",
        styles['BodyText']
    )

    elements.append(skills_para)

    elements.append(Spacer(1, 20))

    # Matched Skills

    matched = ", ".join(matched_skills)

    matched_para = Paragraph(
        f"<b>Matched Skills:</b><br/>{matched}",
        styles['BodyText']
    )

    elements.append(matched_para)

    elements.append(Spacer(1, 20))

    # Missing Skills

    missing = ", ".join(missing_skills)

    missing_para = Paragraph(
        f"<b>Missing Skills:</b><br/>{missing}",
        styles['BodyText']
    )

    elements.append(missing_para)

    elements.append(Spacer(1, 20))

    # Recommended Roles

    roles = ", ".join(recommended_roles)

    roles_para = Paragraph(
        f"<b>Recommended Roles:</b><br/>{roles}",
        styles['BodyText']
    )

    elements.append(roles_para)

    elements.append(Spacer(1, 20))

    # Suggestions

    suggest = "<br/>".join(suggestions)

    suggestion_para = Paragraph(
        f"<b>Suggestions:</b><br/>{suggest}",
        styles['BodyText']
    )

    elements.append(suggestion_para)

    elements.append(Spacer(1, 30))

    # Footer

    footer = Paragraph(
        "Generated by AI Resume Analyzer",
        styles['Italic']
    )

    elements.append(footer)

    # Build PDF

    doc.build(elements)

    # Download PDF

    return send_file(
        pdf_path,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(debug=True)