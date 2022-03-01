#!/usr/bin/env python

from tweet_analyzer import config
import webbrowser
import streamlit as st

# From your app settings page
def set_tokens(auth):
    auth.get_access_token()
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    config.ACCESS_TOKEN = access_token
    config.ACCESS_TOKEN_SECRET = access_token_secret


def login(auth):
    with st.empty():    
        url = auth.get_authorization_url()
        webbrowser.open(url)
        set_tokens(auth)
        #return st.session_state['verifier']

