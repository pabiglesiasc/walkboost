import streamlit as st
from modules import components, styles

st.set_page_config(layout="wide", 
                page_icon="🪙",
                page_title="Boosting Walk",
                initial_sidebar_state='auto')

components.get_sidebar()

if 'project_name' in st.session_state.keys():
    if st.session_state.project_name != '':
        components.get_project_header()