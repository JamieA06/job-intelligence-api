import cloudscraper
import re
import json
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(os.path.join(basedir, '.env'))
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print("API key loaded successfully.")
    genai.configure(api_key=api_key)
else:
    print("Error: GEMINI_API_KEY not found in environment variables.")
model = genai.GenerativeModel('gemini-2.5-flash')

def ai_extract_skills(text):
    prompt = f"""
    You are a technical recruiter. Extract all programming languages, frameworks, and technical tools 
    from the following job description. 
    Return the result ONLY as a comma-separated list of lowercase words. 
    Do not include any introductory text or explanations.
    Job Description: {text}
    """
    
    try:
        response = model.generate_content(prompt)
        skills_text = response.text.strip()
        #debugging
        print(f"AI Response: {skills_text}")
        if not skills_text:            return []

        skills = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
        return skills
    except Exception as e:
        print(f"AI extraction error: {str(e)}")
        return []

def load_skills():
    try:
        with open('skills.json', 'r') as f:
            data = json.load(f)

        all_skills = set()
        for category in data.values():
            all_skills.update(category)

        return all_skills
    except FileNotFoundError:
        print("Error: 'skills.json' file not found.")
        return set()

def scrape_job_description(url):
    scraper = cloudscraper.create_scraper()
    #pretend to be a real browser to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    try:
        #get page
        response = scraper.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check if the request was successful
        
        #get html data
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #target paragraphs
        paragraphs = soup.find_all('p')
        description_text = " ".join([p.get_text() for p in paragraphs])
        
        return description_text.strip()

    except Exception as e:
        return f"Error: {str(e)}"
    
def extract_skills(text):
    skills_list = load_skills()
    if not skills_list:
        return []

    pattern = r'\b(' + '|'.join(re.escape(skill) for skill in skills_list) + r')\b'
    matches = re.findall(pattern, text, re.IGNORECASE)

    return list(set(m.lower() for m in matches))

app = FastAPI()

class JobRequest(BaseModel):
    url: str

@app.post("/analyze-job")
async def analyze_job(request: JobRequest):
    text = scrape_job_description(request.url)

    if "Error:" in text:
        return {"status": "error", "message": text}
    
    matched_skills = set(extract_skills(text))
    ai_skills = set(ai_extract_skills(text))

    new_suggestions = list(ai_skills - matched_skills)

    return {
        "status": "success",
        "url": request.url,
        "matched_skills_count": len(matched_skills),
        "matched_skills": matched_skills,
        "ai_suggested_skills": new_suggestions
    }

#testing code
if __name__ == "__main__":
    target_url = "https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html"
    raw_text = scrape_job_description(target_url)

    if "Error:" not in raw_text:
        print("--- Skills Found ---")
        print(extract_skills(raw_text))

        print("\n--- Testing AI Extraction ---")
        print(ai_extract_skills(raw_text))
    else:
        print(raw_text)