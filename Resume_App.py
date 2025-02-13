import pandas as pd
import nltk
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK dependencies are downloaded to the correct directory
nltk.data.path.append("/home/adminuser/nltk_data")
nltk.download('punkt', download_dir="/home/adminuser/nltk_data")
nltk.download('stopwords', download_dir="/home/adminuser/nltk_data")

# Load job skills dataset
csv_path = "Data/data_job_skills_dataset.csv"  # Adjust the path if needed
try:
    df = pd.read_csv(csv_path)
    job_skills = set(df["Skills"].str.split(",").explode().str.strip().unique())  # Extract skills
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
    job_skills = set()

# Streamlit App UI
st.title("Resume Screening App")
st.subheader("Upload resumes and extract key skills using NLP!")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
if uploaded_file:
    import pdfplumber

    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # Process text using NLTK with fallback if punkt is missing
    try:
        words = word_tokenize(text)
    except LookupError:
        nltk.download('punkt', download_dir="/home/adminuser/nltk_data")
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
