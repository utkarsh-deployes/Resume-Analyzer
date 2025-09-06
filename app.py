from flask import Flask, request, render_template
import google.generativeai as genai
from docx import Document  # Correct import for docx
import fitz  # For .pdf files (PyMuPDF)
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

app = Flask(__name__)

# --- Function to extract text from an uploaded file ---
def extract_text_from_file(uploaded_file):
    if uploaded_file.filename.endswith('.docx'):
        doc = Document(uploaded_file.stream)  # Use stream for Flask uploads
        return "\n".join([p.text for p in doc.paragraphs])
    elif uploaded_file.filename.endswith('.pdf'):
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_doc:
            text += page.get_text()
        return text
    else:
        return "Unsupported file type."

def clean_markdown(text):
    # Remove Markdown bold/italic and headers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove *italic*
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # Remove headers like ## or #
    return text

# --- Route for the main page ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Route to handle the analysis ---
@app.route('/analyze', methods=['POST'])
def analyze():
    resume_file = request.files['resume']
    job_description = request.form['job_description']

    resume_text = extract_text_from_file(resume_file)

    prompt = f"""
    Analyze the RESUME based on the JOB DESCRIPTION.
    Provide a "fit score" from 1 to 100.
    List 3 "missing skills".
    Generate 2 "tailored bullet points".

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """
    response = model.generate_content(prompt)
    cleaned_result = clean_markdown(response.text)  # Clean the output

    return render_template('index.html', analysis_result=cleaned_result)

if __name__ == '__main__':
    app.run(debug=True)

