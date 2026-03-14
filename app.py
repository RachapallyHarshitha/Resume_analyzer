from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os

app = Flask(__name__)
CORS(app)

skills = [
    "python","java","sql","machine learning",
    "react","angular","html","css"
]

def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    return text.lower()


@app.route("/")
def home():
    return "Resume Analyzer Backend Running"


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]
    job_desc = request.form["job_description"].lower()

    file_path = "data/" + file.filename
    file.save(file_path)

    resume_text = extract_text(file_path)

    resume_skills = [s for s in skills if s in resume_text]
    job_skills = [s for s in skills if s in job_desc]

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = (len(matched)/len(job_skills))*100 if job_skills else 0

    # detect strengths
    strengths = []
    if "hardworking" in resume_text:
        strengths.append("Hardworking")
    if "positive attitude" in resume_text:
        strengths.append("Positive Attitude")

    # detect experience
    experience = "No Experience Found"
    if "experience" in resume_text or "workshop" in resume_text:
        experience = "Some training/workshop experience found"

    return jsonify({

        "resume_skills": resume_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": round(score,2),
        "strengths": strengths,
        "experience": experience

    })


if __name__ == "__main__":
    app.run(debug=True)