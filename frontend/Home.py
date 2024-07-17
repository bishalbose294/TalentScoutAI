import streamlit as st
from streamlit_navigation_bar import st_navbar


st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.title("Talent Scout AI")
st.subheader("Where Technology meets Talent")

st.sidebar.success("Select a Page Above")


# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
# https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app