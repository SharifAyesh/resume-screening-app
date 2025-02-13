import os
import spacy
import streamlit as st


# Function to install spaCy model if missing
def ensure_spacy_model(model_name):
    try:
        nlp = spacy.load(model_name)
    except OSError:
        st.warning(f"spaCy model '{model_name}' not found. Installing now...")
        os.system(f"python -m spacy download {model_name}")
        nlp = spacy.load(model_name)
    return nlp


# Ensure model is installed
model_name = "en_core_web_sm"
nlp = ensure_spacy_model(model_name)

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

    # Process text using spaCy NLP
    doc = nlp(text)
    extracted_skills = [ent.text for ent in doc.ents]

    st.subheader("Extracted Skills:")
    st.write(extracted_skills)

    os.remove("temp.pdf")  # Cleanup temp file

st.success("Ready to analyze resumes!")
