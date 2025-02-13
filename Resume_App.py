import os
import nltk
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK dependencies are downloaded
nltk.download("punkt")
nltk.download("stopwords")

st.set_page_config(page_title="Resume Screening App", layout="wide")
st.title("Resume Screening App")

st.write("Upload resumes and extract key skills using NLP!")

# Upload and process resumes
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and process PDF
    import pdfplumber

    with pdfplumber.open("temp.pdf") as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # Process text using NLTK
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.isalnum()]  # Remove punctuation
    filtered_words = [word for word in filtered_words if word.lower() not in stopwords.words("english")]

    st.subheader("Extracted Keywords:")
    st.write(filtered_words)

    os.remove("temp.pdf")  # Cleanup temp file

st.success("Ready to analyze resumes!")
