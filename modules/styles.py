import streamlit as st

def hide_sidebar():

    st.markdown("""

    <style>
        
        [data-testid="stSidebar"]{
            display: none;
        }
                
        [data-testid="collapsedControl"]{
            display: none;
        }
                
    </style>
    
    """, unsafe_allow_html=True)


def hide_sidebar_native_menu():

    st.markdown("""

    <style>
        
        [data-testid="stSidebarNav"]{
            display: none;
        }

    </style>
    
    """, unsafe_allow_html=True)


def get_landing_video_styles():

    st.markdown("""
        
        <style> 
                
            #landing-video {
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%;
                min-height: 100%;
                width: 100%;
                height: 100%;
                background-size: cover;
                object-fit: cover;
                }

            .content {
                position: fixed;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                color: #f1f1f1;
                width: auto;
                padding: 20px;
            }
                
        </style>
    
    """, unsafe_allow_html=True)


def get_button_styles():

    st.markdown("""
        
        <style> 
                
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
                
            .landing-button-container {
                position: fixed;
                bottom: 25%;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                flex-direction: column;
                align-items: center;
            }
                
            .landing-button {
                width: 300px; 
                height: 45px; 
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                cursor: pointer;
                border-radius: 10px;
                opacity: 0;
                background-color: #282D34;
                animation: fadeInUp 1s ease forwards;
                animation-delay: 1s; 
            }
            
            .landing-button:hover {
                opacity: 0.9;
            }
                
            #landing-button-primary {
                background-color: #D84454;
            }
                
            #landing-button-secondary {
                background-color: #282D34;
            }
                                
        </style>
    
    """, unsafe_allow_html=True)
    