import streamlit as st
from pathlib import Path
import requests
import json

st.title("Talent Scout AI")
st.subheader("Where Technology meets Talent")

with st.form(key="Form :", clear_on_submit = True):
    jd = st.file_uploader(accept_multiple_files=False, label="Upload JD")
    resume = st.file_uploader(accept_multiple_files=False, label="Upload Resumes")
    submit = st.form_submit_button(label='Submit')

if submit:
    url = 'http://127.0.0.1:8080/summarize_resume'
    headers={
            "content-type":"application/json",
            "application-type":"REST" 
    }
    print(resume.getvalue())
    save_path = Path("./uploads", resume.name)
    with open(save_path, mode='wb') as f:
        f.write(resume.getvalue())
    print(resume.getvalue())
    files = {'resfiles': resume} 
    print(resume)
    response = requests.post(url=url, files=files, headers=headers)
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.write('Error:', response.status_code)
        