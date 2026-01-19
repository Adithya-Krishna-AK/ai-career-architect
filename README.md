# 📝 AI Career Architect

**Your All-in-One AI Career Strategist, Resume Expert, and Interview Coach.**

The **AI Career Architect** is a Streamlit-based application powered by **Google Gemini 1.5 Flash**. This is an AI powered project built with Streamlit that uses Gemini for helping generate career roadmaps, audit resumes, providing career advice in the form of a chatbot and can also help make your LinkedIn profile better.

---

## 🌟 Features

### 1. 📅 AI Career Planner
- Generates a **custom 6-month roadmap** based on your target role, current skills, and location.
- Provides salary estimates, industry "hard truths," and a weekly study schedule.
- Identifies the "Golden Ticket" portfolio project to boost your profile.

### 2. 📄 Resume & Job Tailor (ATS Scanner)
- **Multimodal Analysis:** Upload a PDF or Image of your resume.
- **Gap Analysis:** Compares your resume against a specific Job Description (URL or Text).
- **Output:** Returns a match score (0-100), missing keywords, and specific bullet point rewrites.

### 3. 💬 AI Career Coach
- A 24/7 Chatbot interface for instant advice.
- Ask questions like *"How do I negotiate my salary?"* or *"What are the best certifications for Data Science?"*.

### 4. 🔗 LinkedIn Profile Auditor
- Analyzes your LinkedIn headline, about section, and experience.
- Provides actionable "Visibility Hacks" to appear in more recruiter searches.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Model:** Google Gemini 1.5 Flash (via `google-genai` SDK)
- **PDF Processing:** PyPDF2
- **Image Processing:** Pillow (PIL)
- **Web Scraping:** BeautifulSoup4, Requests

---

## 🚀 Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/Adithya-Krishna-AK/ai-career-architect.git](https://github.com/Adithya-Krishna-AK/ai-career-architect.git)
cd ai-career-architect
```


### 2. Create & Activate Virtual Environment

**For Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```
For Mac / Linux:


```Bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```Bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

1. Get your free API Key from Google AI Studio.
2. Create a folder named .streamlit in the root directory.
3. Inside that folder, create a file named secrets.toml.
4. Paste your key inside secrets.toml like this:

`GEMINI_API_KEY = "your_actual_api_key_here"
`
### 5. Run the App

```Bash
streamlit run app.py
```