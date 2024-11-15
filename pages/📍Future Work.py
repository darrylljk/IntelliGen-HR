import streamlit as st
import openai
from dotenv import load_dotenv
import os
import time

# page config
st.set_page_config(page_title='Future Work', page_icon='📍')
st.header('📍 Future Work')
st.write("""
Additional features for future development:
- **Onboarding Assistant**: Personalize onboarding for new hires including document generation, training schedules, welcome messages
- **Talent Development Partner**: Create personalized learning and career development plans for employees
- **Performance Review Writer**: Generates performance reviews for employees based on manager input and performance data
- **Succession Planning Tool**: Create succession plans for leadership roles
- **Employee Engagement Analyzer**: Analyze employee surveys and feedback to assess engagement, suggesting methods for improvement
- **Exit Interview Analyzer**: Analyze exit interviews to uncover reasons for employee turnover and provide actionable insights
""")

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