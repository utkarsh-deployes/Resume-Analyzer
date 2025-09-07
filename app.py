from flask import Flask, request, jsonify
import google.generativeai as genai
from docx import Document
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import re
from flask_cors import CORS

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Set GEMINI_API_KEY in your .env file.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

app = Flask(__name__)

# --- SECURE CORS CONFIGURATION ---
# This is the critical change: only allow requests from your Netlify app to the /analyze endpoint.
CORS(app, resources={r"/analyze": {"origins": "https://theresumeanalyzer.netlify.app"}})

# --- Function to extract text from an uploaded file ---
def extract_text_from_file(uploaded_file):
    if uploaded_file.filename.endswith('.docx'):
        try:
            doc = Document(uploaded_file.stream)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"Error reading DOCX file: {e}"
    elif uploaded_file.filename.endswith('.pdf'):
        try:
            pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in pdf_doc:
                text += page.get_text()
            return text
        except Exception as e:
            return f"Error reading PDF file: {e}"
    else:
        return "Unsupported file type."

def clean_markdown(text):
    # A simple function to remove basic Markdown for cleaner display
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)    # Italic
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE) # Headers
    return text.strip()

# --- Route to handle the analysis ---
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    if 'job_description' not in request.form:
        return jsonify({'error': 'No job description provided'}), 400

    resume_file = request.files['resume']
    job_description = request.form['job_description']

    resume_text = extract_text_from_file(resume_file)
    if "Error reading" in resume_text or "Unsupported file" in resume_text:
        return jsonify({'error': resume_text}), 400

    prompt = f"""
    Analyze the following RESUME based on the provided JOB DESCRIPTION.

    Your analysis should be structured with the following three sections:
    1.  **Fit Score**: Provide a percentage score from 1 to 100 representing how well the resume matches the job description.
    2.  **Missing Skills**: List exactly 3 key skills or qualifications from the job description that are not present in the resume.
    3.  **Tailored Bullet Points**: Generate 2 improved, action-oriented bullet points for the resume that directly incorporate keywords and responsibilities from the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """

    try:
        response = model.generate_content(prompt)
        cleaned_result = clean_markdown(response.text)
        return jsonify({'analysis_result': cleaned_result})
    except Exception as e:
        return jsonify({'error': f'An error occurred with the AI model: {e}'}), 500

if __name__ == '__main__':
    # This configuration is correct for Render deployment
    app.run(host='0.0.0.0', port=5000, debug=False)

