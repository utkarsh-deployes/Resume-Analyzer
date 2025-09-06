Resume Analyzer
An intelligent web application designed to evaluate resume alignment with a given job description. This tool provides a quantitative fit score, identifies skill gaps, and suggests tailored improvements to help users optimize their applications for Applicant Tracking Systems (ATS) and human recruiters.

Features
Resume Parsing: Supports both PDF and DOCX file formats for resume uploads.

AI-Powered Analysis: Leverages the Google Gemini API to perform a deep contextual analysis of the resume against the job description.

Fit Scoring: Generates a numerical score from 1-100 to quantify the match between the resume and the job requirements.

Skill Gap Identification: Highlights key skills and qualifications from the job description that are missing from the resume.

Tailored Suggestions: Auto-generates optimized bullet points that can be integrated into the resume to better reflect the required experience.

Tech Stack
Backend: Python, Flask

Frontend: HTML, Tailwind CSS, JavaScript

AI & NLP: Google Gemini API

File Processing: python-docx, PyMuPDF

Setup and Installation
Follow these steps to set up and run the project on your local machine.

1. Prerequisites
Python 3.8 or newer

pip (Python package installer)

2. Clone the Repository
Clone this repository to your local machine:

git clone [https://github.com/utkarsh-deployes/Resume-Analyzer.git](https://github.com/utkarsh-deployes/Resume-Analyzer.git)
cd Resume-Analyzer

3. Set Up a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

4. Install Dependencies
Install the required Python packages from the requirements.txt file.

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file containing Flask, google-generativeai, python-dotenv, python-docx, and PyMuPDF)

5. Configure Environment Variables
Create a file named .env in the root directory of the project. This file will store your API key securely.

Add your Google Gemini API key to the .env file:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

Usage
Once the setup is complete, you can run the Flask development server.

flask run

Or

python app.py

The application will be accessible in your web browser at http://127.0.0.1:5000.

Project Structure
Resume-Analyzer/
├── app.py              # Main Flask application logic
├── analyzer.py         # Standalone script for core AI logic testing
├── .env                # Stores environment variables (e.g., API key)
├── requirements.txt    # Lists Python dependencies
├── templates/
│   └── index.html      # Frontend HTML file
└── README.md           # Project documentation

License
This project is licensed under the MIT License. See the LICENSE file for details.