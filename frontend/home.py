import streamlit as st
from pathlib import Path
import requests, shutil

st.title("Talent Scout AI")
st.subheader("Where Technology meets Talent")

st.markdown("<h4>Resume Summarizer</h4>", unsafe_allow_html=True)

with st.form(key="Form :", clear_on_submit = True):

    resumes = st.file_uploader(accept_multiple_files=True, label="Upload Resumes (*max 3)")
    
    submit = st.form_submit_button(label='Submit')

if submit:
    url = 'http://127.0.0.1:8080/summarize_resume'

    MAX_LINES = 3

    if len(resumes) > MAX_LINES:
        st.warning(f"Maximum number of files reached. Only the first {MAX_LINES} will be processed.")
        resumes = resumes[:MAX_LINES]

    multiplefiles = [] 
    for resume in resumes:
        save_path = Path("./uploads", resume.name)
        with open(save_path, mode='wb') as f:
            f.write(resume.getvalue())
        multiplefiles.append(("resfiles", open(save_path, 'rb')))
        f.close()
    
    with st.spinner("Working..."):
        response = requests.post(url=url, files=multiplefiles)
    
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.write('Error:', response.status_code)
        