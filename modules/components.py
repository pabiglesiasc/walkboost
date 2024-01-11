import streamlit as st
import os
from modules import styles

def get_sidebar():

    styles.hide_sidebar_native_menu()
    st.sidebar.header('Welcome to Boosting Walk', divider='red')

    new_project = st.sidebar.button('New project', use_container_width=True, type='primary', key='new_project')
    load_project = st.sidebar.button('Load project', use_container_width=True, type='secondary', key='load_project')

    if new_project:
        
        st.sidebar.text_input("Please enter the name of your new project:", key='project_name')

    if load_project:

        project_file = st.sidebar.file_uploader('Upload a valid project file (.json):', accept_multiple_files=False)

        if project_file:
            
            st.session_state['project_name'] = project_file['project_name'] 

    st.sidebar.divider()
    default = st.sidebar.button('Default project', use_container_width=True, type='secondary', key='default_project')

    if default:
        st.session_state['project_name'] = 'Default Project'


def get_project_header():

    st.header(st.session_state.project_name, divider='red')
    tab1, tab2, tab3 = st.tabs(['Data Retrieving', 'Data Preprocessing', 'Training Boosting Models'])
