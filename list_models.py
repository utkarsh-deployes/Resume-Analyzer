import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

for m in genai.list_models():
    if m.name == "gemini-1.5-flash":
        print(m.name, m.supported_generation_methods)