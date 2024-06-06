import streamlit as st
from pathlib import Path
import requests, os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from streamlit_agraph import agraph, Node, Edge, Config
import random


def deletePdfs(folderName):
    for parent, dirnames, filenames in os.walk(folderName):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                try:
                    os.remove(os.path.join(parent, fn))
                    print("Deleted", fn)
                except:
                    print("Skipped: ",fn)
    pass


deletePdfs("./uploads")
if not os.path.exists("./uploads"):
    os.makedirs("./uploads")
    print("Created Directory for Upload")

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Talent Scout AI")
st.subheader("Where Technology meets Talent")

st.markdown("<h4>JD Matcher</h4>", unsafe_allow_html=True)

with st.form(key="Form :", clear_on_submit = True):

    jd = st.file_uploader(accept_multiple_files=False, label="Upload JD (*max 1)")
    resumes = st.file_uploader(accept_multiple_files=True, label="Upload Resumes (*max 3)")
    
    submit = st.form_submit_button(label='Submit')

if submit:
    url = 'http://127.0.0.1:8080/calculate_scores'

    MAX_LINES = 3

    if len(resumes) > MAX_LINES:
        st.warning(f"Maximum number of files reached. Only the first {MAX_LINES} will be processed.")
        resumes = resumes[:MAX_LINES]

    save_path = Path("./uploads", jd.name)
    with open(save_path, mode='wb') as f:
        f.write(jd.getvalue())
    
    multiplefiles = [("jdfiles", open(save_path, 'rb'))] 

    for resume in resumes:
        save_path = Path("./uploads", resume.name)
        with open(save_path, mode='wb') as f:
            f.write(resume.getvalue())
        multiplefiles.append(("resfiles", open(save_path, 'rb')))
        f.close()
    
    with st.spinner("Working..."):
        response = requests.post(url=url, files=multiplefiles)


    jd_res_match = response.json()
    resumes_info = jd_res_match[jd.name]
    

    for resumename, value in resumes_info.items():
        st.subheader(resumename)
        st.write("Points : ",value['points'])
        keys = ", ".join(value['keywords']['resume_keywords'])
        
        col1, col2, = st.columns(2)

        
        wordcloud = WordCloud(max_font_size=25, max_words=100, background_color="white", prefer_horizontal=1, height=250, width=250).generate(keys)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        col1.write("Extracted Keywords: ")
        col1.pyplot()

        nodes = []
        edges = []

        resumeNodeColor = "blue"
        jdNodeColor = "green"
        edgeColor = "red"

        mainNode = Node(id=jd.name, 
                label=jd.name, 
                size=25, 
                shape="dot",
                color=jdNodeColor)
        
        exitNode = Node(id=resumename, 
                label=resumename, 
                size=25, 
                shape="dot",
                color=resumeNodeColor)
        
        nodes.append(mainNode)
        
        for jdkeys, reskeys in value["keywords"].items():
            if jdkeys == "resume_keywords":
                continue
            
            jdNodeId = jdkeys+"_"+str(random.randint(0,999))
            nodes.append(Node(id=jdNodeId, 
                label=jdkeys, 
                size=25, 
                shape="dot",
                color=jdNodeColor))
            
            edges.append(Edge(source=jd.name, 
                    label="",
                    color=edgeColor,
                    target=jdNodeId,
                ) 
            )
            
            for keys in reskeys:
                resNodeId = keys+"_"+str(random.randint(0,999))
                nodes.append(Node(id=resNodeId, 
                label=keys, 
                size=25, 
                shape="dot",
                color=resumeNodeColor))
                edges.append(Edge(source=jdNodeId, 
                    label="", 
                    color=edgeColor,
                    target=resNodeId,
                    ) 
                )
            
        config = Config(width=350,
            height=350,
            directed=True, 
            physics=True, 
            hierarchical=False,
            # **kwargs
            )
        

        col2.write("JD/Resume Keyword Graph: ")
        with col2:
            agraph(nodes=nodes, 
                edges=edges, 
                config=config,
                )

deletePdfs("./uploads")