import os
import nltk
import streamlit as st
import pdfplumber
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure necessary NLTK resources are downloaded
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize NLP tools
tokenizer = RegexpTokenizer(r'\b[a-zA-Z]{3,}\b')  # Extract only words (no numbers/symbols)
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

st.set_page_config(page_title="Resume Screening App", layout="wide")
st.title("Resume Screening App")

st.write("Upload resumes and extract key skills using NLP!")

# Upload and process resumes
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and process PDF
    with pdfplumber.open("temp.pdf") as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # Tokenization, lemmatization, and stopword removal
    words = tokenizer.tokenize(text.lower())  # Convert to lowercase and tokenize
    filtered_words = [
        lemmatizer.lemmatize(word) for word in words if word not in stop_words  # Remove stopwords & lemmatize
    ]

    # Display extracted words
    st.subheader("Extracted Keywords:")
    st.write(list(set(filtered_words)))  # Remove duplicates

    os.remove("temp.pdf")  # Cleanup temp file

st.success("Ready to analyze resumes!")
