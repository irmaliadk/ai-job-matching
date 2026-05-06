import streamlit as st
import fitz  # PyMuPDF
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Job Matching")

st.title("🤖 AI Job Matching & Career Coach")

# 🔑 GANTI API KEY DI SINI
client = OpenAI(api_key="OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload CV (PDF)")
job_desc = st.text_area("Paste Job Description")

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if uploaded_file and job_desc:
    with st.spinner("Processing AI..."):
        cv_text = extract_text(uploaded_file)

        prompt = f"""
        You are an AI career assistant.

        Compare this CV and job description.

        CV:
        {cv_text}

        Job:
        {job_desc}

        Give output:
        1. Compatibility Score (0-100)
        2. Missing Skills
        3. 5 Interview Questions
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

    st.subheader("📊 Result")
    st.write(result)