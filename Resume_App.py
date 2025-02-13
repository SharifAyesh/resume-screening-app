import pandas as pd
import nltk
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pdfplumber
import tempfile
import os

# Ensure NLTK dependencies are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load job skills dataset
csv_path = "Data/job_skills_dataset.csv"  # Ensure this matches your file path
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

if uploaded_file is not None:
    # Save the uploaded file temporarily to disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Process the PDF with pdfplumber
    try:
        with pdfplumber.open(temp_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

        # Process text using NLTK
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.isalnum()]
        filtered_words = [word for word in filtered_words if word.lower() not in stopwords.words('english')]

        # Extract matched skills
        matched_skills = sorted(set(filtered_words) & job_skills)

        st.subheader("Extracted Skills:")
        if matched_skills:
            st.write(", ".join(matched_skills))
        else:
            st.write("No matching skills found in the resume.")

    except Exception as e:
        st.error(f"Error processing the file: {e}")

    # Clean up the temporary file
    os.remove(temp_path)
