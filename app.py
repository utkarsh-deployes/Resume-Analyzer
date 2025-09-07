from flask import Flask, request, jsonify
import google.generativeai as genai
from docx import Document
import fitz
import os
from dotenv import load_dotenv
import re
from flask_cors import CORS

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

app = Flask(__name__)

# === THIS IS THE CRITICAL FIX ===
# This line now specifically allows your Netlify frontend to make requests.
CORS(app, resources={r"/analyze": {"origins": "https://theresumeanalyzer.netlify.app"}})

# --- Function to extract text from an uploaded file ---
def extract_text_from_file(uploaded_file):
    if uploaded_file.filename.endswith('.docx'):
        doc = Document(uploaded_file.stream)
        return "\n".join([p.text for p in doc.paragraphs])
    elif uploaded_file.filename.endswith('.pdf'):
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_doc:
            text += page.get_text()
        return text
    else:
        # Return a JSON error response for unsupported file types
        return None, "Unsupported file type. Please upload a PDF or DOCX."

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    return text

# --- Route to handle the analysis ---
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided.'}), 400
        
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')

    resume_text, error = extract_text_from_file(resume_file)
    if error:
        return jsonify({'error': error}), 400

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
    try:
        response = model.generate_content(prompt)
        cleaned_result = clean_markdown(response.text)
        return jsonify({'analysis_result': cleaned_result})
    except Exception as e:
        return jsonify({'error': f'An error occurred with the AI model: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

