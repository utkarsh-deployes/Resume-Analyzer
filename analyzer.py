# Import necessary libraries to load the secret key
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the environment variables from the .env file
load_dotenv()

# Securely get the API key from the environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if the key was found
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Make sure you have a .env file with GEMINI_API_KEY set.")

# Configure the Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# The rest of your code is unchanged
resume_text = """
John Doe
Software Engineer
- Developed a web application using Python and Flask.
- Managed databases with SQL.
"""

job_description_text = """
Looking for a Backend Developer with experience in Python and databases.
Experience with cloud services like AWS is a plus.
Must be a team player.
"""

prompt = f"""
Analyze the RESUME based on the JOB DESCRIPTION.
Provide a "fit score" from 1 to 100.
List 3 "missing skills" from the job description not found in the resume.
Generate 2 "tailored bullet points" for the resume to better match the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description_text}
"""

# Send the prompt to Gemini and print the result
response = model.generate_content(prompt)
print(response.text)