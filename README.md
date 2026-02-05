# Job Intelligence API (Scraper + Gemini AI)

A robust backend service that transforms unstructured job descriptions into structured JSON data. It uses a **Hybrid Extraction Engine** that combines traditional keyword matching (Set Theory) with Generative AI (Google Gemini 1.5) for high-accuracy skill discovery.



## Key Features
* **Web Scraping**: Built-in support for extracting text from job URLs using `BeautifulSoup4`.
* **Hybrid Analysis**: 
    * **Verified Matcher**: Fast, regex-based matching against a custom `skills.json` library.
    * **AI Discovery**: Context-aware extraction using **Gemini 1.5 Flash** to find niche skills.
* **RESTful API**: Built with **FastAPI** for high performance and automatic Swagger documentation.
* **Secure**: Implements environment variable management (`python-dotenv`) to protect sensitive API keys.

## Tech Stack
* **Language**: Python 3.10+
* **Framework**: FastAPI
* **AI**: Google Generative AI (Gemini)
* **Scraping**: Requests, BeautifulSoup4
* **Deployment**: Render / Railway (Planned)

## Getting Started

### 1. Prerequisites
* A Google AI Studio API Key (Get it at https://aistudio.google.com/)
* Python installed

### 2. Installation
1. Clone the repo:
   git clone https://github.com/JamieA06/job-intelligence-api.git
2. Install dependencies:
   pip install -r requirements.txt

### 3. Configuration
Create a .env file in the root directory:
GEMINI_API_KEY=your_key_here

### 4. Running the API
uvicorn main:app --reload

Visit http://127.0.0.1:8000/docs to test the endpoints interactively.

## API Example Response
{
  "status": "success",
  "url": "https://example.com/job-post",
  "matched_skills": ["python", "django", "html"],
  "ai_suggested_skills": ["rest api", "unit testing", "git"]
}

## Contact
Jamie - https://github.com/JamieA06