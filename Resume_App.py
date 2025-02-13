import pandas as pd
import streamlit as st
from textblob import TextBlob
import pdfplumber
import nltk

# Ensure required corpora are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load job skills dataset
csv_path = "Data/job_skills_dataset.csv"  # Adjust the path if needed
try:
    df = pd.read_csv(csv_path)
    job_skills = set(df["Skills"].str.split(",").explode().str.strip().unique())
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
    job_skills = set()

# Streamlit App UI
st.title("Resume Screening App")
st.subheader("Upload resumes and extract key skills using NLP!")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # Process text with TextBlob
    blob = TextBlob(text)
    filtered_words = {word.lower() for word in blob.words if word.isalpha()}

    # Extract matched skills
    matched_skills = sorted(filtered_words & job_skills)

    st.subheader("Extracted Skills:")
    if matched_skills:
        st.write(", ".join(matched_skills))
    else:
        st.write("No matching skills found in the resume.")
