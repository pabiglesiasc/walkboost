import streamlit as st
from modules import styles

st.set_page_config(layout="wide", 
                   page_icon="🪙",
                   page_title="Boosting Walk",
                   initial_sidebar_state='collapsed')

styles.hide_sidebar()
styles.get_landing_video_styles()
styles.get_button_styles()

video_link = "./app/static/landing_background_video.mp4"

st.markdown(f"""
    
    <video autoplay muted loop id="landing-video">  
        <source src="{video_link}"> Your browser does not support HTML5 video.
    </video>

""", unsafe_allow_html=True)

st.markdown("""
        
    <div class="landing-button-container">
        <a href="project" target="_self">
            <button id="landing-button-primary" class="landing-button">Get started!</button>
        </a>
    </div>

""", unsafe_allow_html=True)