import streamlit as st
import pandas as pd
import pdfplumber
import spacy
import os
import re
from collections import Counter

# ✅ Ensure this is the FIRST Streamlit command
st.set_page_config(page_title="Resume Screening App", layout="wide")

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Load Job Skills Dataset
dataset_path = "data/job_skills_dataset.csv"
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
    st.sidebar.success("✅ Job Skills Dataset Loaded!")
else:
    st.sidebar.warning("⚠️ Dataset Not Found! Please upload job_skills_dataset.csv")


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


# Function to extract key skills from resume
def extract_skills(text):
    doc = nlp(text)
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    return set(words)


# Function to predict job title
def predict_job(skills):
    if df is None:
        return "⚠️ No Job Dataset Loaded"

    skill_counts = Counter()
    for _, row in df.iterrows():
        job_title = row["Job Title"]
        job_skills = set(re.split(r",|\s+", row["Skills"].lower()))
        match_score = len(skills.intersection(job_skills))
        skill_counts[job_title] += match_score

    return skill_counts.most_common(1)[0][0] if skill_counts else "❌ No Job Match Found"


# UI Header
st.markdown("<h1 style='text-align: center; color: #2C3E50;'>📄 Resume Screening App</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #2980B9;'>Upload a Resume PDF to Extract Skills and Predict Jobs</h3>",
    unsafe_allow_html=True)

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload a Resume (PDF)", type=["pdf"])
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    # Extract Skills
    skills = extract_skills(resume_text)
    st.markdown("### 🎯 Extracted Key Skills")
    st.write(", ".join(skills))

    # Predict Job
    job_prediction = predict_job(skills)
    st.markdown("### 🚀 Predicted Job Title")
    st.success(job_prediction)
