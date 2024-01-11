import streamlit as st
import pandas as pd
import os
from modules import styles

def get_sidebar():

    styles.hide_sidebar_native_menu()
    styles.get_sidebar_logo()

    new_project = st.sidebar.button('New Project', use_container_width=True, type='primary', key='new_project')
    load_project = st.sidebar.button('Load Project', use_container_width=True, type='secondary', key='load_project')

    if new_project:

        if 'project_name' in st.session_state.keys():
            del st.session_state['project_name']

        st.sidebar.text_input("Please enter the name of your new project:", max_chars=100, key='project_name')
        st.session_state['description'] = 'This is a new project. You can enter a description here.' 
        st.session_state['date_created'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    if load_project:

        project_file = st.sidebar.file_uploader('Upload a valid project file (.json):', accept_multiple_files=False)

        if project_file:
            
            st.session_state['project_name'] = project_file['project_name'] 
            st.session_state['description'] = 'Description here.'
            st.session_state['date_created'] = '%Y-%m-%d %H:%M:%S'

    st.sidebar.divider()
    default = st.sidebar.button('Default Project', use_container_width=True, type='secondary', key='default_project')

    if default:
        st.session_state['project_name'] = 'Default Project'
        st.session_state['description'] = 'This is the default project. This system makes 1-day predictions on stock price movements...'
        st.session_state['date_created'] = '2024-01-11 06:47:22'

def get_project_header():

    st.toast(f'{st.session_state.project_name} :green[successfully] loaded!')

    col1, col2  = st.columns([.9, .1])
            
    with col2:
        st.download_button('Save project', pd.DataFrame([0]).to_csv(), use_container_width=True, key='save_project', disabled=st.session_state.project_name=='Default Project')

    st.title(st.session_state.project_name)
    st.caption(f'Created on {st.session_state.date_created}')
    st.session_state.description = st.text_area('', st.session_state.description, disabled=st.session_state.project_name=='Default Project')
    tab1, tab2, tab3 = st.tabs(['Data Retrieving', 'Data Preprocessing', 'Training Boosting Models'])

    with tab1: 

        st.toggle('Overwrite', value=False, key='overwrite', disabled=st.session_state.project_name=='Default Project', )

        # with st.container(border=True):
            
        #     st.data_editor(
                
        #         pd.DataFrame(

                    
                
        #             ), 
                
        #         use_container_width=True, 
        #         disabled=st.session_state.project_name=='Default Project')

