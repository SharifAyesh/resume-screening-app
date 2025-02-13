import os
import nltk
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure all required NLTK resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("omw-1.4")

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
    try:
        words = word_tokenize(text)  # Tokenize words
        filtered_words = [word for word in words if word.isalnum()]  # Remove punctuation
        filtered_words = [word for word in filtered_words if word.lower() not in stopwords.words("english")]

        st.subheader("Extracted Keywords:")
        st.write(filtered_words)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    os.remove("temp.pdf")  # Cleanup temp file

st.success("Ready to analyze resumes!")
