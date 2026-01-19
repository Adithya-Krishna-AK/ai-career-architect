import streamlit as st
from google import genai
import PyPDF2
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Career Architect", page_icon="🚀", layout="wide")

# --- API KEY ---
GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']

if not GEMINI_API_KEY or "PASTE_YOUR_KEY" in GEMINI_API_KEY:
    st.error("⚠️ Please check your API Key.")
    st.stop()

# --- CLIENT SETUP ---
try:
    client = genai.Client(api_key=st.secrets['GEMINI_API_KEY'])
except:
    st.error("API Key Error")

# --- SESSION STATE ---
if 'planner_result' not in st.session_state: st.session_state['planner_result'] = None
if 'resume_audit' not in st.session_state: st.session_state['resume_audit'] = None
if 'resume_plan' not in st.session_state: st.session_state['resume_plan'] = None
if 'linkedin_result' not in st.session_state: st.session_state['linkedin_result'] = None
if 'chat_history' not in st.session_state: st.session_state['chat_history'] = []

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #4B4BFF; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .ai-box { background-color: #1a1c24; padding: 25px; border-radius: 10px; border: 1px solid #4B4BFF; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_gemini_response(input_content):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=input_content
        )
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def extract_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return None

def process_uploaded_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        return None

def scrape_web_content(url):
    """Scrapes text from a URL (Job Post or LinkedIn)."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Get text and clean it up
            text = soup.get_text(separator=' ', strip=True)
            return text[:5000] 
        else:
            return None
    except Exception as e:
        return None

# --- SIDEBAR: PROFILE ---
st.sidebar.title("👤 Your Profile")

target_role = st.sidebar.text_input("🎯 Target Role / Dream Job", placeholder="e.g. Data Scientist")
interests = st.sidebar.text_input("❤️ Your Interests", placeholder="e.g. Gaming, Art, Math")

# Logic to determine focus
final_goal = None
display_msg = ""

if target_role:
    final_goal = target_role
    display_msg = f"🚀 Planning for: **{target_role}**"
    if interests:
        display_msg += f" *(incorporating {interests})*"
elif interests:
    final_goal = interests
    display_msg = f"✨ Planning for your interest: **{interests}**"
else:
    display_msg = "⚠️ No Goal set yet."

qualifications = st.sidebar.text_input("🎓 Qualifications")
selected_skills = st.sidebar.text_input("🛠️ Your Skills")
location = st.sidebar.text_input("🌍 Location", "Remote")
experience = st.sidebar.selectbox("⏳ Experience", ["Student", "Entry Level", "Mid Level", "Senior"])

st.sidebar.markdown("---")
if final_goal:
    st.sidebar.info(display_msg)
else:
    st.sidebar.warning(display_msg)

# --- MAIN INTERFACE ---
st.markdown('<div class="main-header">📝 AI Career Architect</div>', unsafe_allow_html=True)

# NEW TAB ORDER
tab_planner, tab_resume, tab_chat, tab_linkedin = st.tabs([
    "📅 Career Planner", 
    "📄 Resume & Job Tailor", 
    "💬 AI Coach",
    "🔗 Job Profile Auditor"
])

# --- TAB 1: AI PLANNER (Context Aware) ---
with tab_planner:
    st.markdown(f"### 📅 Custom Roadmap")
    if st.button("🚀 Generate Strategy", key="btn_manual"):
        if not final_goal:
            st.warning("⚠️ Please enter a Target Role or Interest in the sidebar.")
        else:
            with st.spinner("🤖 Drafting strategy..."):
                skills_text = selected_skills if selected_skills else "None listed"
                
                prompt = f"""
                Act as a world-class Senior Career Strategist.
                
                USER CONTEXT:
                - Target Role: {target_role if target_role else "Not specified"}
                - Interests: {interests if interests else "Not specified"}
                - Qualifications: {qualifications if qualifications else "Not specified"}
                - Experience: {experience}
                - Skills: {skills_text}
                - Location: {location if location else "Global/Remote"}
                
                TASK: Create and writea complete Career guide and a strategic roadmap.
                - If "Target Role" is present, focus strictly on that.
                - If only "Interests" are present, suggest career paths matching that interest first, then build a plan for the best one.
                - If BOTH are present, combine them (e.g., "AI Engineer" + "Gaming" = "AI in Game Dev").
                
                IMPORTANT: Detect the language of the user's inputs. Answer STRICTLY in that same language.

                ### Part 1: The Role Intelligence 🧠
                * **Salary Range:** (Estimate for {location if location else "Global"})
                * **The Ladder:** What comes before and after this role?
                * **Key Tech Stack:** The exact tools industry requires.
                * **Hard Truths:** 2 uncommonly known barriers to entry.
                
                ### Part 2: The Action Plan 🚀
                1. 🎯 **The Objective** (Clear goal statement)
                2. 🌟 **The Reality Check** (Honest assessment)
                3. 🎓 **Learning Path** (Certs/Skills)
                4. 💡 **The Strategy:** How to pivot from {experience} to {target_role}.
                5. 🛠️ **Project "Golden Ticket":** One portfolio project idea that combines {final_goal}.
                6. 📅 **Weekly Routine:** A 5-hour/week study schedule.
                """
                st.session_state['planner_result'] = get_gemini_response(prompt)

    if st.session_state['planner_result']:
        st.markdown(f'<div class="ai-box">{st.session_state["planner_result"]}</div>', unsafe_allow_html=True)

# --- TAB 2: RESUME & JOB TAILOR ---
with tab_resume:
    st.markdown("### 📄 Resume Optimizer")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "png", "jpg", "jpeg"])
    
    # Optional Job URL Input
    st.markdown("#### 🎯 Tailor to a Specific Job (Optional)")
    job_url = st.text_input("Paste a Job Posting URL (LinkedIn, Indeed, Company Site):")
    
    final_content = None
    if uploaded_file is not None:
        st.success("✅ File Loaded!")
        if "pdf" in uploaded_file.type:
            final_content = extract_pdf_text(uploaded_file)
        else:
            final_content = process_uploaded_image(uploaded_file)
            if final_content: st.image(final_content, caption="Preview", width=300)
        
        if final_content:
            if st.button("🔍 Analyze & Tailor Resume", key="btn_audit"):
                with st.spinner("🤖 Analyzing resume & job..."):
                    
                    # 1. Scrape Job Description if URL provided
                    job_context = "General Industry Standards"
                    if job_url:
                        scraped_data = scrape_web_content(job_url)
                        if scraped_data:
                            job_context = f"SPECIFIC JOB POSTING:\n{scraped_data[:3000]}"
                            st.success(f"✅ Job Description extracted from URL!")
                        else:
                            st.warning("⚠️ Could not scrape URL (Site might be blocking bots). Using general standards.")
                    
                    # 2. Build Prompt
                    prompt = f"""
                    Act as an Expert ATS Resume Scanner & Recruiter.
                    
                    RESUME CONTENT: Provided below.
                    TARGET CONTEXT: {job_context}
                    USER GOAL: {final_goal}
                    
                    IMPORTANT: Detect the language of the resume. Answer STRICTLY in that language.
                    
                    TASK:
                    1. **Match Score (0-100)**: How well does it fit the Target Context?
                    2. **Missing Keywords**: What specific skills from the Job Description are missing?
                    3. **Formatting Check**: Is it professional?
                    4. **Tailoring Suggestions**: rewrite 2 bullet points to better match the Job Description.
                    """
                    
                    content_payload = [prompt, final_content] if not isinstance(final_content, str) else prompt + f"\n\nRESUME:\n{final_content[:3000]}"
                    st.session_state['resume_audit'] = get_gemini_response(content_payload)

    if st.session_state['resume_audit']:
        st.markdown(f'<div class="ai-box">{st.session_state["resume_audit"]}</div>', unsafe_allow_html=True)


# --- TAB 3: AI COACH ---
with tab_chat:
    st.markdown(f"### 💬 AI Career Coach")
    
    for message in st.session_state['chat_history']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask me anything..."):
        st.session_state['chat_history'].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_instruction = f"""
                You are "Gemini Guide", a supportive Career Coach.
                User Goal: {final_goal}. Skills: {selected_skills}.
                
                IMPORTANT: Detect the user's language. Reply in that language.
                Be human, encouraging, and concise.
                """
                conversation_log = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state['chat_history'][-5:]])
                full_prompt = f"{system_instruction}\n{conversation_log}\n\nUser: {user_query}\nAssistant:"
                
                response = get_gemini_response(full_prompt)
                st.markdown(response)
        
        st.session_state['chat_history'].append({"role": "assistant", "content": response})

# --- TAB 4: PROFILE AUDITOR ---
with tab_linkedin:
    st.markdown("### 🔗 LinkedIn Profile Optimizer")
    st.info("💡 Note: LinkedIn blocks most bots. For best results, paste your text manually below.")
    
    li_text_fallback = st.text_area("Paste your Profile 'About' & 'Experience' text here:")
    li_url = st.text_input("(Optional) Profile URL:")
    
    if st.button("✨ Audit Profile", key="btn_li"):
        profile_data = li_text_fallback
        
        if not profile_data and li_url:
            with st.spinner("Attempts to scrape..."):
                scraped = scrape_web_content(li_url)
                if scraped and len(scraped) > 200:
                    profile_data = scraped
                    st.success("✅ Scrape successful!")
                else:
                    st.error("❌ Could not scrape LinkedIn (Auth Wall). Please paste text above!")
                    st.stop()
                
                if profile_data:
                    prompt = f"""
                    Act as a Personal Branding Expert.
                    Review this LinkedIn Profile data:
                    {profile_data[:4000]}
                    
                    Target Role: {final_goal}
                    
                    IMPORTANT: Detect language. Answer in that language.
                    
                    TASK:
                    1. **Headline Score**: Rewrite it to be punchy and search-optimized.
                    2. **About Section**: Is it a story or a list? Give specific edits.
                    3. **Visibility Hacks**: Suggest 3 changes to appear in more recruiter searches.
                    """
                    st.session_state['linkedin_result'] = get_gemini_response(prompt)
    
    if st.session_state['linkedin_result']:
        st.markdown(f'<div class="ai-box">{st.session_state["linkedin_result"]}</div>', unsafe_allow_html=True)