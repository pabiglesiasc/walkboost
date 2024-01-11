import streamlit as st
from modules import styles
import pandas as pd
import time 

st.set_page_config(layout="wide", 
                page_icon="🪙",
                page_title="Boosting Walk",
                initial_sidebar_state='expanded')

# Sidebar configuration

styles.hide_sidebar_native_menu()
styles.get_sidebar_logo()

new_scheme = st.sidebar.button('New Scheme', use_container_width=True, type='primary')
load_scheme = st.sidebar.button('Load Scheme', use_container_width=True, type='secondary')
default_scheme = st.sidebar.button('Default Scheme', use_container_width=True, type='secondary')
st.sidebar.divider()

if 'scheme_name' not in st.session_state.keys():

    if new_scheme:
        def creating_scheme_callback():
            styles.hide_sidebar_native_menu()
            with st.spinner('Creating new scheme. Please wait...'):
                time.sleep(2)
        st.info('Please provide a name for your new scheme to move on.', icon='ℹ️')
        st.sidebar.text_input("Please enter the name of your new scheme:", max_chars=100, key='scheme_name', on_change=creating_scheme_callback)
        st.session_state['scheme_description'] = 'This is a new scheme. You can enter a description here.' 
        st.session_state['scheme_creation_time'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    if load_scheme:

        if scheme_file: 
            st.session_state['scheme_name'] = scheme_file['scheme_name'] 
            st.session_state['scheme_description'] = 'Scheme description here.'
            st.session_state['scheme_creation_time'] = '%Y-%m-%d %H:%M:%S'

    if default_scheme:
        st.session_state['scheme_name'] = 'Default Scheme'
        st.session_state['scheme_description'] = 'This is the default scheme. This system makes 1-day predictions on stock price movements...'
        st.session_state['scheme_creation_time'] = '2024-01-11 06:47:22'

else:
    
    st.session_state['scheme_name'] = st.session_state['scheme_name']

    if new_scheme or load_scheme or default_scheme:
        st.toast(f'A scheme is currently loaded. Please :orange[close the scheme in use] before opening a new one.', icon='⚠️')

# Body

if 'scheme_name' in st.session_state.keys():
    
    if st.session_state.scheme_name != '':
        
        st.toast(f'{st.session_state.scheme_name} :green[successfully] loaded!', icon='✅')
        st.title(st.session_state.scheme_name)
        st.caption(f'Created on {st.session_state.scheme_creation_time}')
        
        col1, col2  = st.columns([.8, .2])

        with col1:
            st.session_state.scheme_description = st.text_area('', st.session_state.scheme_description, disabled=st.session_state.scheme_name=='Default Scheme')
                
        with col2:
            
            for _ in range(2): 
                st.write("")
            
            saved_scheme = st.download_button('Save Scheme', pd.DataFrame([0]).to_csv(), use_container_width=True, disabled=st.session_state.scheme_name=='Default Scheme')
            
            close_scheme = st.button('Close Scheme', use_container_width=True, type='primary')

            if close_scheme:
                
                for k in st.session_state.keys(): 
                    del st.session_state[k]
                st.rerun()

        tab1, tab2, tab3 = st.tabs(['Data Retrieving', 'Data Preprocessing', 'Training Boosting Models'])

        with tab1: 
            overwrite = st.toggle('Overwrite', value=False, key='overwrite', disabled=st.session_state.scheme_name=='Default Scheme')
            
            # pd.

st.text(dict(st.session_state.items()))