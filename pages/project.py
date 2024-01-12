import streamlit as st
from modules import styles, dataretriever
import os
import json
import pandas as pd
import numpy as np
import time 
from datetime import date, datetime

st.set_page_config(layout="wide", 
                page_icon="🪙",
                page_title="Boosting Walk",
                initial_sidebar_state='expanded')

def get_body():

    if st.session_state.project_name!='':

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

            def created_saved_project_path():
                if not os.path.exists(f"static/projects/{st.session_state.project_name}"):
                    os.makedirs(f"static/projects/{st.session_state.project_name}")
                pd.Series({k:v for k, v in st.session_state.items() if 'new' not in k}).to_json(f"static/projects/{st.session_state.project_name}/{st.session_state.project_name}.json")
            
            st.download_button(
                label='Save Project',
                data=pd.Series({k:v for k, v in st.session_state.items() if 'new' not in k}).to_json(),
                mime='application/json',
                file_name=f'{st.session_state.project_name}.json',
                use_container_width=True, 
                on_click=created_saved_project_path,
                disabled=st.session_state.project_name=='Default Project')      
            
            close_project = st.button('Close Project', use_container_width=True, type='primary')                

            if close_project:
                
                for k in st.session_state.keys(): 
                    del st.session_state[k]
                st.rerun()

        tab1, tab2, tab3 = st.tabs(['Data Retrieving', 'Data Preprocessing', 'Training Boosting Models'])

        with tab1: 

            with st.container(border=True):

                st.markdown('Main parameters:')

                default_retriever_args = pd.DataFrame(
                    [{
                        "start_date": pd.Timestamp(st.session_state.start_date).date(), 
                        "end_date": pd.Timestamp(st.session_state.end_date).date(), 
                        "stocks": st.session_state.stocks, 
                        "macroeconomic": st.session_state.macroeconomic, 
                        "correlated": st.session_state.correlated, 
                        "trading_years": st.session_state.trading_years
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
                            max_value=int((default_retriever_args['end_date'].values[0] - default_retriever_args['start_date'].values[0]).days/252)
                        ),
                    },
                )

            st.session_state['start_date'] = retriever_args['start_date'].values[0].strftime('%Y-%m-%d')
            st.session_state['end_date'] = retriever_args['end_date'].values[0].strftime('%Y-%m-%d')
            st.session_state['stocks'] = retriever_args['stocks'].values[0]
            st.session_state['macroeconomic'] = retriever_args['macroeconomic'].values[0]
            st.session_state['correlated'] = retriever_args['correlated'].values[0]
            st.session_state['trading_years'] = retriever_args['trading_years'].values[0]

            with st.container(border=True):

                st.markdown('Extra parameters:')

                def set_custom_stocks():
                    st.session_state['custom_stocks'] = st.session_state.new_custom_stocks

                with st.expander('Add custom stocks (Ticker Symbols)', expanded=st.session_state.project_name!='Default Project'):
                
                    st.text_area(
                        label=st.session_state.custom_stocks,
                        placeholder="Add ticker symbols, separated by ; (i.e. AAAA;BBBB;...;ZZZZ)",
                        disabled=st.session_state.project_name=='Default Project',
                        key='new_custom_stocks',
                        on_change=set_custom_stocks
                    )

                def set_macroeconomic_indicators():
                    st.session_state['macroeconomic_indicators'] = st.session_state.new_macroeconomic_indicators

                with st.expander('Choose macroeconomic indicators (Ticker Symbols)', expanded=st.session_state.macroeconomic and st.session_state.project_name!='Default Project'):
                
                    st.multiselect(
                        label='',
                        options=['^GSPC', '^990100-USD-STRD', '^VIX', '^FVX', 'GC=F', 'CL=F', 'EUR=X', 'GBP=X', 'CNY=X', 'JPY=X'],
                        default=st.session_state.macroeconomic_indicators,
                        disabled=not st.session_state.macroeconomic or st.session_state.project_name=='Default Project',
                        key='new_macroeconomic_indicators',
                        on_change=set_macroeconomic_indicators
                    )

                def set_number_correlated():
                    st.session_state['number_correlated'] = st.session_state.new_number_correlated

                with st.expander('Number of highest-correlated stocks to retrieve', expanded=st.session_state.correlated and st.session_state.project_name!='Default Project'):

                    st.slider(
                        label='',
                        value=1,
                        min_value=1,
                        max_value=5, 
                        step=1,
                        disabled=not st.session_state.correlated or st.session_state.project_name=='Default Project',
                        key='new_number_correlated',
                        on_change=set_number_correlated
                    )

            generate = st.button('Generate raw dataset', use_container_width=True, type='primary')

            if generate:

                with st.spinner('Downloading requested libraries. Please wait...'):
                    dataretriever.get_yfinance()
                    st.caption('yfinance successfully installed!')

st.text(st.session_state)

styles.hide_sidebar_native_menu()
styles.get_sidebar_logo()

new_project = st.sidebar.button('New Project', use_container_width=True, type='primary')
load_project = st.sidebar.button('Load Project', use_container_width=True, type='secondary')
default_project = st.sidebar.button('Default Project', use_container_width=True, type='secondary')
st.sidebar.divider()

if 'project_name' not in st.session_state.keys():
    
    if new_project:
        
        def get_project_name():
            st.session_state['project_name'] = st.session_state['new_project_name']
            del st.session_state['new_project_name']

        st.info('Please provide a name for your new project to move on.', icon='ℹ️')

        with open('static/projects/Default Project/Default Project.json', 'r') as project_file:
            project_file = json.loads(project_file.read())

        project_file['project_name'] = ''

        for k, v in project_file.items():
            st.session_state[k] = v

        st.sidebar.text_input("Please enter the name of your new project:", max_chars=100, key='new_project_name', on_change=get_project_name)
        
        st.session_state['project_description'] = 'This is a new project. You can enter a description here.'
        st.session_state['project_creation_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if load_project:
        
        project_file = st.sidebar.file_uploader('Upload a valid project file (.json):', accept_multiple_files=False, type='json')
        
        if project_file:

            project_file = json.loads(project_file.read())
            for k, v in project_file.items():
                st.session_state[k] = v

    if default_project:

        with open('static/projects/Default Project/Default Project.json', 'r') as project_file:
            project_file = json.loads(project_file.read())
        
        for k, v in project_file.items():
            st.session_state[k] = v
        st.rerun()
        
else:

    if new_project or load_project or default_project:
        st.toast(f'There is a project in use. Please :orange[close this project] before opening a new one.', icon='⚠️')

    get_body()

st.text(st.session_state)


    
