import streamlit as st
from modules import components
st.set_page_config(layout="centered", 
                   page_icon="🪙",
                   page_title="Boosting Walk",
                   initial_sidebar_state='collapsed')

components.get_landing_video()
components.get_landing_buttons()
