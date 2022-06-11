import datetime
import streamlit as st

def find_time_period():
    """find the startdate for selected number of Days
     end date is always today
    """
    end_date = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(days=st.session_state['days'])
    return start_date,end_date

def find_tweets_in_period(df):
    """ Select tweets in the specific time period"""
    start_date,end_date = find_time_period()
    mask = (start_date.date() <= df['Created']) & (df['Created'] <= end_date.date())
    return df[mask]


def find_engagement(original_tweets_df):
    """Engagment of each tweet is calculated in dataframe"""
    original_tweets_df['Engagement'] = original_tweets_df['Favourites']*0.2 + original_tweets_df['Retweets']*0.8
    last_period_tweets = find_tweets_in_period(original_tweets_df)[['Tweet','Engagement']]
    return last_period_tweets
