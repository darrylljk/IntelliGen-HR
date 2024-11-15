import streamlit as st
import openai
from dotenv import load_dotenv
import fitz # pip install PyMuPDF
import os
import time
from docx import Document

# system config
# ----- local (store api key in .env file) ---------
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# ----- --------------------------------------------

# ----- streamlit cloud ---------
api_key = st.secrets["OPENAI_API_KEY"]
# -------------------------------

openai.api_key = api_key
model = "gpt-4o-mini"

# page config
st.set_page_config(page_title='Smart Interview AI', page_icon='📌')
st.header('📌 Smart Interview AI')
st.write("""
Smart Interview AI helps you craft personalized interview questions for each candidate by analyzing their resumes and the job description.
         
Whether you're conducting interviews for a new role or refining your hiring process, Smart Interview AI ensures your questions are relevant, focused, and aligned with the job requirements.
""")
st.markdown('---')

st.write("""
##### ✨ Key Features:
- **AI-Driven**: Generates insightful interview questions based on candidate resumes and job descriptions.
- **Customizable**: Tailor the questions to specific needs or job requirements.
- **Time-Saving**: Receive a fully crafted interview questionnaire in minutes.
""")
st.markdown('')
st.markdown('')

st.write(''' 
##### ⚙️ How it works:
Simply upload the candidate's resume and job description, select question types, click **Generate**, and let Smart Interview AI craft your perfect interview questions! 🚀
''')


# functions
def read_file(file): # reads content of file
    # Determine file type
    if file.type == "application/pdf":
        return read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file)
    else:
        return file.read().decode('utf-8')

def read_pdf(file): # extracts text from pdf file
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_docx(file): # extracts text from docx file
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_requirements(text): # extracts key info from JD
    """
    Extract the key skills, qualifications, and responsibilities from the job description.
    """
    prompt = f"""
    Extract the key skills, qualifications, and responsibilities from the following job description:

    {text}

    Provide a summary of the key requirements.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key skills, qualifications, and responsibilities from the job description"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0
    )

    return response.choices[0].message.content.strip()

def analyze_text(text): # analyzes candidate CV text
    """
    Analyze the text to extract skills, qualifications, and experience from the candidate's CV.
    """
    prompt = f"""
    Analyze the following text from a candidate's CV and extract key skills, qualifications, and experiences:

    {text}

    Provide a summary of the candidate's skills and experiences.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant that analyzes the text to extract skills, qualifications, and experience from the candidate CV'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0
    )

    return response.choices[0].message.content.strip()

def evaluate_candidate_fit(requirements, cv_analysis): # assess candidate fit based on JD and CV
    """
    Evaluate the candidate's fit for the role based on the job requirements and their CV.
    """
    prompt = f"""
    Based on the following job requirements and candidate CV analysis, assess the candidate’s fit for the role:

    Job Requirements:
    {requirements}

    Candidate CV Analysis:
    {cv_analysis}

    Provide a suitability score on a scale of 1 to 10, and explain the assessment.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant that evaluates the candidate fit for the role based on the job requirements and their CV'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0
    )

    return response.choices[0].message.content.strip()

def generate_interview_questions(jd, cv, categories): # generate a list of interview questions
    categories_str = ', '.join(categories)

    prompt = f"""
    Job Description:
    {jd}

    Candidate CV:
    {cv}

    You are a seasoned interviewer with extensive experience creating insightful and relevant interview questions. Your objective is to assess the candidate's suitability for the role, ensuring a thorough evaluation of both their technical expertise and cultural fit.

    Please generate a comprehensive list of interview questions that:
    1. Explore the candidate's professional experience, highlighting their technical skills, project work, and specific achievements listed in the CV.
    2. Assess the candidate's capability to meet the responsibilities outlined in the job description, using job-specific scenarios or challenges.
    3. Evaluate problem-solving abilities, critical thinking, and adaptability, with a focus on past real-world examples.
    4. Gauge cultural fit by exploring the candidate's alignment with the company's values, mission, and workplace environment.
    5. Uncover the candidate's motivations, career goals, and long-term aspirations, ensuring they align with the role and company trajectory.
    6. Examine teamwork and conflict resolution capabilities, asking for examples of how the candidate has managed or participated in team-driven projects or resolved conflicts.
    7. Investigate any potential concerns, such as employment gaps, job-hopping, skill mismatches, or inconsistencies in their CV, and address these directly in your questions.

    The categories you need to focus on are: {categories_str}. Each category should include 4-5 insightful questions. In each category, aim for:
    - At least 1-2 questions directly referencing the candidate’s experience as listed in their CV.
    - A mix of behavioral, situational, and competency-based questions.
    - Questions that explore both soft skills (e.g., cultural fit, teamwork) and technical proficiency.

    The questions should be framed in a way that encourages detailed responses, offering insights into the candidate's capabilities and alignment with the role.

    Output the questions in the following structured format:

    Category A: [e.g., Technical Skills]
    - question 1: [Open-ended, scenario-based question]
    - question 2: [Follow-up question based on CV]
    - question 3: [Problem-solving question]
    - question 4: [Technical knowledge question]

    Category B: [e.g., Business Acumen]
    - question 1: [Scenario-based question]
    - question 2: [Experience-based question]
    - question 3: [Critical thinking question]
    - question 4: [Cultural alignment question]
    - question 5: [Long-term goals question]

    Please ensure each category is covered with thoughtful and varied questions.

    List of Interview Questions:
    """

    response = openai.chat.completions.create(
    model=model,
    messages=[
        {"role":"system", "content":"You are an experienced talent acquisition executive specializing in crafting insightful interview questions."},
        {"role":"user", "content":prompt}
    ],
    max_tokens=2000, n=1, stop=None, temperature=0
    )

    return response.choices[0].message.content.strip()

# form
with st.form(key='settings_form'):
    jd_file = st.file_uploader("Upload Job Description", type=['pdf', 'txt', 'docx'])
    st.markdown('')
    cv_file = st.file_uploader("Upload Candidate CV", type=['pdf', 'txt', 'docx'])
    st.markdown('')
    categories = st.segmented_control(
        "Select Question Types to Focus On",
        ["Technical Skills", "Business Acumen", "Industry Specific", "Cultural Fit", "Problem-Solving", "Career Goals", "Teamwork", "Conflict Management", "CV Anomalies"],
        selection_mode='multi',
        help="Choose the categories you want to focus on during the interview. Each category is designed to evaluate specific aspects of the candidate's profile."
    )
    st.markdown('')
    submit_button = st.form_submit_button(label='📄 Generate Interview Questions', help='Click to generate the job description based on the entered information.')


# Link to profile 
st.markdown("""
    <style>
        .footer {
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 12px;
            color: gray;
            margin-top: 20px;
        }
    </style>
    <div class="footer">
        Author: Darryl Lee | 
        <a href="https://www.linkedin.com/in/your-linkedin-profile" target="_blank">LinkedIn</a> | 
        <a href="https://github.com/darrylljk" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)