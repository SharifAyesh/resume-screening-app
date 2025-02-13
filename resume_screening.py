import os
import csv
import pdfplumber
import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# List of skills to match
SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data analysis", "sql", "nlp", "artificial intelligence",
    "cloud computing", "flask", "django", "tensorflow",
    "pytorch", "react", "html", "css", "javascript", "git",
    "network security", "firewall", "ethical hacking"
]

# Job role categories
JOB_CATEGORIES = {
    "Data Scientist": ["python", "machine learning", "data analysis", "tensorflow", "sql", "nlp"],
    "Software Engineer": ["java", "c++", "git", "django", "flask", "cloud computing"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Cybersecurity Analyst": ["network security", "firewall", "ethical hacking"],
}

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills(text):
    """Identify skills mentioned in the resume"""
    doc = nlp(text.lower())  # Convert text to lowercase for matching
    found_skills = [token.text for token in doc if token.text in SKILLS]
    return list(set(found_skills))  # Remove duplicates

def classify_resume(skills):
    """Classify the resume into a job category"""
    job_match_count = {job: len(set(skills) & set(required_skills)) for job, required_skills in JOB_CATEGORIES.items()}
    best_match = max(job_match_count, key=job_match_count.get)  # Find the job with the most skill matches
    return best_match if job_match_count[best_match] > 0 else "Unknown"

def save_results_to_csv(filename, resume_name, skills, job_category):
    """Save resume results to a CSV file"""
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Resume Name", "Predicted Job Role", "Extracted Skills"])  # Write header only once
        writer.writerow([resume_name, job_category, ", ".join(skills)])

    print(f"\n✅ Results saved for {resume_name} in {filename}")

def process_all_resumes():
    """Process all resumes in the Data folder"""
    RESUME_FOLDER = "Data/"
    CSV_FILENAME = "resume_results.csv"

    print("\n📂 Processing all resumes in 'Data' folder...")

    for filename in os.listdir(RESUME_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(RESUME_FOLDER, filename)
            resume_text = extract_text_from_pdf(pdf_path)
            skills_found = extract_skills(resume_text)
            job_category = classify_resume(skills_found)

            print(f"\n📄 {filename} - 🎯 Predicted Job Role: {job_category}")
            print(f"🔍 Extracted Skills: {', '.join(skills_found)}")

            # Save results to CSV
            save_results_to_csv(CSV_FILENAME, filename, skills_found, job_category)

# Run the batch processing function
process_all_resumes()

