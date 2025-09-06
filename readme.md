# Resume Analyzer

An intelligent web application designed to evaluate resume alignment with a given job description. This tool provides a quantitative fit score, identifies skill gaps, and suggests tailored improvements to help users optimize their applications for Applicant Tracking Systems (ATS) and human recruiters.

## Features

* **Resume Parsing**: Supports both PDF and DOCX file formats for resume uploads.
* **AI-Powered Analysis**: Leverages the Google Gemini API to perform a deep contextual analysis of the resume against the job description.
* **Fit Scoring**: Generates a numerical score from 1-100 to quantify the match between the resume and the job requirements.
* **Skill Gap Identification**: Highlights key skills and qualifications from the job description that are missing from the resume.
* **Tailored Suggestions**: Auto-generates optimized bullet points that can be integrated into the resume to better reflect the required experience.

## Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML, Tailwind CSS, JavaScript
* **AI & NLP**: Google Gemini API
* **File Processing**: `python-docx`, `PyMuPDF`

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

* Python 3.8 or newer
* `pip` (Python package installer)

### 2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/utkarsh-deployes/Resume-Analyzer.git
cd Resume-Analyzer