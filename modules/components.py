import streamlit as st
import os
from modules import styles

def get_landing_video():

    styles.get_landing_video_styles()
    
    video_link = "./app/static/landing_background_video.mp4"
    
    st.markdown(f"""
        
        <video autoplay muted loop id="landing_video">  
            <source src="{video_link}"> Your browser does not support HTML5 video.
        </video>
    
    """, unsafe_allow_html=True)


def get_landing_buttons():

    styles.get_button_styles()
    
    st.markdown("""

        <div style="position: fixed; bottom: 20%; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center;">
            
            <a href="new_model" target="_self">
                <button id="landing-button-primary" class="landing-button">Get started!</button>
            </a>
            
            <a href="default_model" id="default_model_button_link" target="_self">
                <button id="landing-button-secondary" class="landing-button">Use default model</button>
            </a>
        
        </div>
    """, unsafe_allow_html=True)


def get_sidebar():

    styles.hide_sidebar_native_menu()

    st.sidebar.header('Boosting Walk', divider='red')
    st.sidebar.link_button('New Project', url='new_model', use_container_width=True)
    
    for project in os.listdir('./pages'):
        
        if project!='new_model.py':
            
            st.sidebar.link_button(project.replace('.py', '').replace('_', ' ').title(), url=project.replace('.py', ''), use_container_width=True)

def get_project_header(project_name):

    st.set_page_config(layout="centered", 
                   page_icon="",
                   page_title=project_name,
                   initial_sidebar_state='collapsed')
    
    col1, col2 = st.columns([.6, .4], gap='medium')

    with col1:  
        st.header(project_name, divider='red')
    
    with col2:
        remove_project = st.button('Remove Project', type='primary', key='remove', use_container_width=True)

    if st.session_state.remove:
        
        del st.session_state.remove
        os.remove(f"pages/{project_name}.py")
        st.success(f'The project {project_name} has been successfully removed.')
        
        col1, col2, col3 = st.columns([.3, .3, .4])
        
        with col1:
            st.markdown(
                '''
                <a href="new_model" target="_self">
                    <button class="primary-button">Create custom model</button>
                </a>
                ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(
                '''
                <a href="default_model" target="_self">
                    <button class="secondary-button">Use default model</button>
                </a>
                ''', unsafe_allow_html=True)

    else:
    
        tab1, tab2, tab3 = st.tabs(['Data Retrieving', 'Data Preprocessing', 'Training Boosting Models'])
