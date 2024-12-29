import streamlit as st
import pandas as pd

st.set_page_config(page_title='HR IntelliGen', page_icon='💫')
st.header('IntelliGen HR')

st.markdown("""
            Introducing a smarter approach to Human Resources.

            IntelliGen HR is your AI Partner that frees you from mundane HR chores, allowing you to focus on what truly matters.

            ⬅️ Click on the tabs in the sidebar to get started.
""")
st.markdown('---')

st.markdown('#### 🔨 Toolkit')
st.markdown('')

st.markdown('##### 1. AutoJD ')
st.markdown('Craft professional job descriptions. ')
st.markdown('')

st.markdown('##### 2. Smart Interview AI ')
st.markdown('Generate personalized interview questions.')

# Link to profile 
st.write('')
st.write('')
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
        <a href="https://www.linkedin.com/in/darryl-lee-jk/" target="_blank">LinkedIn</a> | 
        <a href="https://github.com/darrylljk" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)
