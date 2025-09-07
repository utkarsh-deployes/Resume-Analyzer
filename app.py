from flask import Flask, request, jsonify
import google.generativeai as genai
from docx import Document
import fitz
import os
from dotenv import load_dotenv
import re
from flask_cors import CORS

# Load environment variables for local development
load_dotenv()

app = Flask(__name__)

# This line specifically allows your Netlify frontend to make requests.
CORS(app, resources={r"/analyze": {"origins": "https://theresumeanalyzer.netlify.app"}})

# --- Configuration at the start ---
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    # This will now be visible in Render logs if the key is missing
    print("ERROR: Gemini API key not found in environment variables.")
    # We don't raise an error here, but handle it in the request
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        print("Successfully configured Gemini model.")
    except Exception as e:
        model = None
        print(f"ERROR: Failed to configure Gemini model: {e}")

# --- Function to extract text from an uploaded file ---
def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.filename.endswith('.docx'):
            doc = Document(uploaded_file.stream)
            return "\n".join([p.text for p in doc.paragraphs]), None
        elif uploaded_file.filename.endswith('.pdf'):
            pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in pdf_doc:
                text += page.get_text()
            return text, None
        else:
            return None, "Unsupported file type. Please upload a PDF or DOCX."
    except Exception as e:
        # Catch any errors during file parsing
        return None, f"Error processing file: {str(e)}"

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    return text

# --- Route to handle the analysis ---
@app.route('/analyze', methods=['POST'])
def analyze():
    # --- Check 1: Is the Gemini model configured? ---
    if not model or not GEMINI_API_KEY:
        return jsonify({'error': 'Server configuration error: AI model is not available.'}), 500

    # --- Check 2: Was a file uploaded? ---
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided.'}), 400
        
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')

    # --- Check 3: Can we read the file? ---
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
    
    # --- Check 4: Did the AI call succeed? ---
    try:
        response = model.generate_content(prompt)
        cleaned_result = clean_markdown(response.text)
        return jsonify({'analysis_result': cleaned_result})
    except Exception as e:
        print(f"ERROR during Gemini API call: {e}") # This will show in Render logs
        return jsonify({'error': f'An error occurred with the AI model. Please check server logs.'}), 500

if __name__ == '__main__':
    # Render provides the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

