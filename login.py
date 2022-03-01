#!/usr/bin/env python

from tweet_analyzer import config
import webbrowser
import streamlit as st

# From your app settings page
def set_tokens(auth):
    auth.get_access_token(st.session_state['verifier'])
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    config.ACCESS_TOKEN = access_token
    config.ACCESS_TOKEN_SECRET = access_token_secret

def callback_function(auth):
    st.session_state['verifier'] = st.text_input("Enter Pin",key = 2)
    set_tokens(auth)


def login(auth):
    with st.empty():    
        url = auth.get_authorization_url()
        webbrowser.open(url)
        st.session_state['verifier'] = st.text_input("Enter Pin",key = 2)
        set_tokens(auth)
        return st.session_state['verifier']

