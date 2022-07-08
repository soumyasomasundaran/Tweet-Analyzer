import streamlit as st


st.set_page_config(page_title="Tweet Analyzer", page_icon=":CHIRPBIRDICON:", layout="wide")

def hide_menu():
    """hide the default menu option"""
    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)


def remove_padding():
    """To remove padding between elements"""
    padding = 10
    st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)