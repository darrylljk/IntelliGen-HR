import streamlit as st
import openai
from dotenv import load_dotenv
import os
import time

# system config
# ----- local (store api key in .env file) ---------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# ----- --------------------------------------------

# ----- streamlit cloud ---------
# api_key = st.secrets["OPENAI_API_KEY"]
# -------------------------------

openai.api_key = api_key
model = "gpt-4o-mini"

# page config
st.set_page_config(page_title='AutoJD', page_icon='📌')
st.header('📌 AutoJD')
st.write("""
AutoJD helps you quickly craft professional job descriptions tailored to your needs. 
         
Whether you're hiring for a new role or updating an existing one, AutoJD ensures your job descriptions are clear, comprehensive, and engaging.
""")
st.markdown('---')

st.write("""
##### ✨ Key Features:
- **AI-Powered**: Ensure JD is comprehensive and well-formatted.
- **Customizable**: Personalize the JD to your needs.
- **Time-Saving**: Receive your JD in minutes.
""")
st.markdown('')
st.markdown('')

st.write('''
##### ⚙️ How it works:
Fill out the form, click **Generate**, and let AutoJD craft your perfect job description in minutes! 🚀
''')

# features
def generate_job_description(job_title, company, department, department_info, experience, education, degree, skills, employment_type, work_location, responsibilities, language, travel):

    prompt = f"""
    Create a detailed job description using the following information:
    Company: {company}
    Job Title: {job_title}
    Department: {department}
    Department Info: {department_info}
    Employment Type: {', '.join(employment_type)}
    Work Location: {work_location}
    Work Experience: {experience}
    Education: {education}
    Relevant Degree: {', '.join(degree)}
    Required Skills: {skills}
    Responsibilities: {responsibilities}
    Language Proficiency: {', '.join(language)}
    May be required to travel: {travel}

    Create a professional, engaging job description following best practices. The job description should include the following sections:
    1. About the Company (Provide a brief overview of the company, its culture, and values)
    2. Job Summary (Provide a concise summary of the job, explaining the key purpose of the role and its significance within the organization)
    3. Key Responsibilities (Provide at least 8-10 bullet points outlining the primary duties and tasks expected from the candidate)
    4. Required Skills (List specific technical and soft skills required for the role)
    5. Preferred Qualifications (Include Work Experience, Education, Certifications, and any other qualifications that are advantageous but not mandatory)
    6. Language Proficiency (List the languages required for the position, if any)
    7. Work Environment (Describe the work conditions, including whether the role is remote, hybrid, or on-site)
    8. Travel Requirements (Specify if travel is expected and the extent)
    9. Additional Information (Provide any other important details about the role or company that would attract potential candidates)

    Make sure to expand on each section, ensuring the job description is thorough, attractive, and clearly communicates the expectations for the role. Incorporate any relevant company culture, expectations, and job specifics that would help candidates understand the full scope of the position.

    Job Description:
    """

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role":"system", "content":"You are an experienced talent acquisition executive specializing in crafting compelling and detailed job descriptions that attract top talent across various industries."},
            {"role":"user", "content":prompt}
        ],
        max_tokens=2000, n=1, stop=None, temperature=0
    )
    return response.choices[0].message.content.strip()

# form
with st.form(key='job_description_form'): # form
    company = st.text_input('Company', 'Meta', help='Enter the company name where the position is offered.')
    job_title = st.text_input('Job Title', "Data Scientist", help='Specify the title of the job being offered.')
    department = st.text_input('Department', 'Product Analytics', help='Enter the department that the role belongs to.')
    department_info = st.text_area('Department Info', "Meta's Product Analytics department leverages data to evaluate product performance, identify user behavior trends, and collaborate with product teams to optimize features and enhance user engagement for products like Facebook, Instagram, and WhatsApp.", help='Provide more details about the department (e.g., key functions, team size, projects)')
    employment_type = st.segmented_control('Employment Type', ['Full-time', 'Part-time', 'Contract', 'Internship'], selection_mode='multi', help='Select the type of employment for the role.')
    work_location = st.segmented_control('Work Location', ['On-site', 'Hybrid', 'Remote'], selection_mode='single', help='Specify where the role will be based (e.g., On-site, Hybrid, or Remote).')
    experience = st.segmented_control('Min. Related Work Experience', ['0-2 years', '3-5 years', '5-10 years', 'More than 10 years'], selection_mode='single', help='Indicate the minimum required years of work experience for the role.')
    education = st.segmented_control('Min. Education Qualification', ['Diploma', "Bachelor's Degree", "Master's' Degree", 'PhD'], selection_mode='single', help='Select the minimum education qualification required for the position.')
    language = st.segmented_control('Language requirements', ['English', 'Chinese', 'Malay', 'Tamil', 'Spanish'], selection_mode='multi', help='Select the languages required for the role.')
    travel = st.segmented_control('May be required to travel', ['Yes', 'No'], selection_mode='single', help='Specify whether the role requires travel.')
    degree = st.multiselect('Preferred Degree Majors', sorted(['Any', 'Engineering', 'Mathematics', 'Business', 'Finance', 'Computer Science', 'Economics', 'Data Science', 'Marketing', 'Arts and Social Science', 'Physics', 'Psychology', 'Communications', 'Information Systems', 'Statistics', 'Political Science', 'Linguistics', 'Literature', 'Philosophy', 'Sociology']), default=sorted(['Data Science', 'Statistics', 'Mathematics', 'Engineering']), help="Select the degree majors relevant to the job. You can select multiple options.")
    skills = st.text_area('Skills Required', 'Experience with data querying languages (e.g. SQL), scripting languages (e.g. Python), and/or statistical/mathematical software (e.g. R).', help='List the skills required for the position.')
    responsibilities = st.text_area('Responsibilities', 'Analyze large-scale data to derive actionable insights, drive business decisions, and collaborate with cross-functional teams to enhance tools, processes, and user value.', help='List the responsibilities required for this position.')
    submit_button = st.form_submit_button(label='🔥 Generate the Perfect JD', help='Click to generate the job description based on the entered information.')

if submit_button:
    with st.spinner('Generating job description...'):
        progress_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.05)
            progress_bar.progress(percent_complete+1)
        
        job_description = generate_job_description(
            job_title=job_title, 
            company=company, 
            experience=experience, 
            education=education, 
            degree=degree, 
            skills=skills, 
            department=department, 
            department_info=department_info, 
            employment_type=employment_type, 
            work_location=work_location,
            responsibilities=responsibilities,
            language=language,
            travel=travel
        )

    st.subheader("Generated Job Description:")
    st.write(job_description)
    st.balloons()
    st.download_button(label="Download Job Description as TXT", data=job_description, file_name="job_description.txt", mime="text/plain")

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
