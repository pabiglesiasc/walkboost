import streamlit as st
from modules import styles
import pandas as pd
import numpy as np
import time 
from datetime import date, datetime

st.set_page_config(layout="wide", 
                page_icon="🪙",
                page_title="Boosting Walk",
                initial_sidebar_state='expanded')

# Sidebar configuration

styles.hide_sidebar_native_menu()
styles.get_sidebar_logo()

new_project = st.sidebar.button('New Project', use_container_width=True, type='primary')
load_project = st.sidebar.button('Load Project', use_container_width=True, type='secondary')
default_project = st.sidebar.button('Default Project', use_container_width=True, type='secondary')
st.sidebar.divider()

if 'project_name' not in st.session_state.keys():

    if new_project:
        def creating_project_callback():
            styles.hide_sidebar_native_menu()
            with st.spinner('Creating new project. Please wait...'):
                time.sleep(1)
        st.info('Please provide a name for your new project to move on.', icon='ℹ️')
        st.sidebar.text_input("Please enter the name of your new project:", max_chars=100, key='project_name', on_change=creating_project_callback)
        st.session_state['project_description'] = 'This is a new project. You can enter a description here.' 
        st.session_state['project_creation_time'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    if load_project:
        project_file = st.sidebar.file_uploader('Upload a valid project file (.json):', accept_multiple_files=False)

        if project_file: 
            st.session_state['project_name'] = project_file['project_name'] 
            st.session_state['project_description'] = 'Project description here.'
            st.session_state['project_creation_time'] = '%Y-%m-%d %H:%M:%S'

        st.rerun()

    if default_project:
        st.session_state['project_name'] = 'Default Project'
        st.session_state['project_description'] = 'This is the default project. This system makes 1-day predictions on stock price movements...'
        st.session_state['project_creation_time'] = '2024-01-11 06:47:22'
        st.rerun()

else:
    
    st.session_state['project_name'] = st.session_state['project_name']

    if new_project or load_project or default_project:
        st.toast(f'A project is currently loaded. Please :orange[close the project in use] before opening a new one.', icon='⚠️')

# Body

if 'project_name' in st.session_state.keys():
    
    if st.session_state.project_name != '':

        if not new_project and not load_project and not default_project:
            st.toast(f'{st.session_state.project_name} :green[successfully] loaded!', icon='✅')
        
        st.title(st.session_state.project_name)
        st.caption(f'Created on {st.session_state.project_creation_time}')
        
        col1, col2  = st.columns([.8, .2])

        with col1:
            st.session_state.project_description = st.text_area('', st.session_state.project_description, disabled=st.session_state.project_name=='Default Project')
                
        with col2:
            
            for _ in range(2): 
                st.write("")
            
            saved_project = st.download_button('Save Project', pd.DataFrame([0]).to_csv(), use_container_width=True, disabled=st.session_state.project_name=='Default Project')      
            close_project = st.button('Close Project', use_container_width=True, type='primary')

            if close_project:
                
                for k in st.session_state.keys(): 
                    del st.session_state[k]
                st.rerun()

        tab1, tab2, tab3 = st.tabs(['Data Retrieving', 'Data Preprocessing', 'Training Boosting Models'])

        with tab1: 

            overwrite = st.toggle('Overwrite', value=False, key='overwrite', disabled=st.session_state.project_name=='Default Project')

            with st.container(border=True):

                st.markdown('Main parameters:')

                default_retriever_args = pd.DataFrame(
                    [{
                        "start_date": date(2000, 1, 1), 
                        "end_date": date(2023, 12, 31), 
                        "stocks": "DJIA30", 
                        "macroeconomic": True, 
                        "correlated": True, 
                        "trading_years": 20
                    }]
                )
                
                retriever_args = st.data_editor(
                    default_retriever_args, 
                    disabled=st.session_state.project_name=='Default Project',
                    num_rows="fixed", 
                    hide_index=True, 
                    use_container_width=True,
                    column_config={
                        "start_date": st.column_config.DateColumn(
                            "Start Date", 
                            help='The start date for the data retrieval.',
                            required=True, 
                            min_value=date(1980, 1, 1), 
                            max_value=date.today()
                        ), 
                        "end_date": st.column_config.DateColumn(
                            "End Date",
                            help='The end date for the data retrieval.',
                            required=True, 
                            min_value=date(1980, 1, 1), 
                            max_value=date.today()
                        ), 
                        "stocks": st.column_config.SelectboxColumn(
                            "Stocks", 
                            help='The stock universe for the data retrieval.',
                            required=True, 
                            options=['DJIA30', 'SP500', 'NASDAQ100']
                        ), 
                        "macroeconomic": st.column_config.CheckboxColumn(
                            "Include macroeconomic assets", 
                            help='Choose whether to retrieve macroeconomic assets or not.',
                            required=True
                        ),
                        "correlated": st.column_config.CheckboxColumn(
                            "Include correlated stocks",
                            help='Choose whether to retrieve close price data of highest-correlated stocks or not.',
                            required=True
                        ),
                        "trading_years": st.column_config.NumberColumn(
                            "Minimum trading years", 
                            help="Choose minimum trading years to keep each stock. Stock with less than 'Minimum trading years'*252 trading days will be discarded.",
                            min_value=0,
                            max_value=int(((default_retriever_args['end_date'] - default_retriever_args['start_date']) / np.timedelta64(1, 'D'))/252)
                        ),
                    },
                )

                st.session_state['retriever_args'] = retriever_args

            with st.container(border=True):
                st.markdown('Extra parameters:')
                extra_stocks = st.text_area(
                    "Add custom stocks (Ticker Symbols)",
                    placeholder="Add ticker symbols, separated by ; (i.e. AAAA;BBBB;...;ZZZZ)",
                )
                macroecnomic_indicators = st.multiselect(
                    'Choose macroeconomic indicators (Ticker Symbols)',
                    options=['^GSPC', '^990100-USD-STRD', '^VIX', '^FVX', 'GC=F', 'CL=F', 'EUR=X', 'GBP=X', 'CNY=X', 'JPY=X'],
                    default=['^GSPC', '^990100-USD-STRD', '^VIX', '^FVX', 'GC=F', 'CL=F', 'EUR=X', 'GBP=X', 'CNY=X', 'JPY=X'],
                    disabled=not st.session_state.retriever_args['macroeconomic'].values[0] or st.session_state.project_name=='Default Project',
                )
                    
