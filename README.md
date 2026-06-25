# AI Resume Analyzer

An AI-powered web application that analyzes resumes and helps students improve them for internship and job applications.

## Live Demo

[Open AI Resume Analyzer](https://ai-resume-analyzer-tjv8.onrender.com)

## Features

- Upload resume in PDF format
- Extract text from uploaded resume
- Detect technical skills from resume
- Calculate ATS resume score
- Match resume skills with job description
- Identify matched and missing skills
- Generate resume improvement suggestions
- Generate interview questions based on detected skills
- Recommend suitable job roles
- Display skill analytics using charts
- Drag-and-drop resume upload
- Dark mode user interface
- Download analysis report as PDF

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Chart.js
- pdfplumber
- ReportLab
- Render
- GitHub

## Project Workflow

1. User uploads a resume PDF.
2. Flask receives and saves the uploaded file.
3. pdfplumber extracts text from the PDF.
4. The system checks the resume text against a predefined skills list.
5. ATS score is calculated based on detected skills.
6. Resume skills are compared with the job description.
7. The application displays matched skills, missing skills, suggestions, interview questions, and recommended roles.
8. ReportLab generates a downloadable PDF report.

## Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── resume_report.pdf
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── uploads/
