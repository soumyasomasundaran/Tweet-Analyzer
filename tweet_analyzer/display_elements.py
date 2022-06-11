import textwrap
import streamlit as st
import pandas as pd
import plotly.express as px
from numerize import numerize 
from . import find_engagment


def display_user_profile(user, c1):
    """display About, followers and following count of a user"""
    c1.markdown(f"**About:** {user['description']}")
    c1.markdown(f"### Followers: {(str(numerize.numerize(user['followers'])))}")
    c1.markdown(f"### Following: {(str(numerize.numerize(user['following'])))}")

def find_lists(list_name,list_df,list_container):
    """ finds lists of the user given """
    list_container.header(list_name+str(len(list_df)))
    list_df = pd.DataFrame(list(list_df.items()), columns=["ListName", "Followers Count"])
    sorted_df = (list_df.sort_values(by=["Followers Count"], ascending=False, ignore_index=True))
    return sorted_df

    
def display_user_lists(followed, owned, memberof, col1, col2, col3):
    """display lists followed, owned by a user and lists in which they are members"""
    list_followed_container = col1.container()
    list_owned_container = col2.container()
    list_membership_container = col3.container()
    with col1:
        if followed:
            sorted_df = find_lists("Lists Followed: ",followed,list_followed_container)
            list_followed_container.dataframe(sorted_df)
        else:
            list_followed_container.header("No lists Followed")

    with col2:
        if owned:
            sorted_df = find_lists("Lists Owned: ",owned,list_owned_container)
            list_owned_container.dataframe(sorted_df)
        else:
            list_owned_container.header("No lists Owned")

    with col3:
        if memberof:
            sorted_df = find_lists("Lists Membership: ",memberof,list_membership_container)
            list_membership_container.dataframe(sorted_df)
            
        else:
            list_membership_container.header("Not a member of any list")


def custom_wrap(s, width=30):
    """method to wrap text"""
    return "<br>".join(textwrap.wrap(s, width=width))


def display_days_selector(c2):
    """Display selector for the Engagment Chart"""
    days_dic = {"Last 30 Days":30, "Today":1, "Last 7 Days":7,"Last 90 Days":90,"Last 12 months":365}
    days = c2.selectbox("Select Period", days_dic.keys()) 
    time_period = days_dic[days]    
    return time_period


def display_engagement_chart(tweets, c2):
    """Display engagment chart"""
    barchart_df = find_engagment.find_engagement(tweets)
    if barchart_df.empty:
        c2.warning("No Tweets in the Selected Period")
    else:
        fig = px.bar(barchart_df, x=barchart_df['Tweet'], y=barchart_df['Engagement'],
                    title="Engagement")
        fig.update_xaxes(showticklabels=False)
        for ser in fig['data']:
            ser['hovertemplate'] = [str(custom_wrap(d)) for d in barchart_df['Tweet']]

        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
            )
        )
        c2.plotly_chart(fig, use_container_width=True, height=800)



def draw_divider():
    """Draws divider line"""
    text = '''
    ---
    '''
    st.markdown(text)
