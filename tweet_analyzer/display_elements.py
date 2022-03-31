import textwrap
import streamlit as st
from . import visualizations
import pandas as pd
import plotly.express as px
from numerize import numerize 

def display_user_profile(user, c1):
    c1.markdown(f"**About:** {user['description']}")
    c1.markdown(f"### Followers: {(str(numerize.numerize(user['followers'])))}")
    c1.markdown(f"### Following: {(str(numerize.numerize(user['following'])))}")


def display_user_lists(followed, owned, memberof, col1, col2, col3):
    list_followed_container = col1.container()
    list_owned_container = col2.container()
    list_membership_container = col3.container()
    with col1:
        if followed:
            list_followed_container.header("Lists Followed:"+str(len(followed)))
            list_followed_df = pd.DataFrame(list(followed.items()), columns=["ListName", "Followers Count"])
            sorted_df = (list_followed_df.sort_values(by=["Followers Count"],
                                                      ascending=False, ignore_index=True))
            list_followed_container.dataframe(sorted_df)

        else:
            list_followed_container.header("No lists Followed")
    with col2:
        if owned:
            list_owned_container.header("Lists Owned:"+str(len(owned)))
            list_owned_df = pd.DataFrame(list(owned.items()), columns=["List Name", "Followers Count"])
            list_owned_container.dataframe(list_owned_df.sort_values(by=["Followers Count"],
                                                                     ascending=False, ignore_index=True))
        else:
            list_owned_container.header("No lists Owned")

    with col3:
        if memberof:
            list_membership_container.header("Lists Membership:"+str(len(memberof)))
            list_membership_df = pd.DataFrame(list(memberof.items()), columns=["List Name", "Followers Count"])
            list_membership_container.dataframe(list_membership_df.sort_values(by=["Followers Count"],
                                                                     ascending=False, ignore_index=True))
        else:
            list_membership_container.header("Not a member of any list")


def custom_wrap(s, width=30):
    return "<br>".join(textwrap.wrap(s, width=width))


def display_days_selector(c2):
    days_dic = {"Last 30 Days":30, "Today":1, "Last 7 Days":7,"Last 90 Days":90,"Last 12 months":365, }
    days = c2.selectbox("Select Period", days_dic.keys()) 
    time_period = days_dic[days]    
    return time_period


def draw_engagement_chart(tweets, c2):
    barchart_df = visualizations.find_engagement(tweets)
    if barchart_df.empty:
        c2.warning("No Tweets in the Selected Period")
    else:
        fig = px.bar(barchart_df, x=barchart_df['Tweet'], y=barchart_df['Engagement'],
                    title=f"Engagement")
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
    text = '''
    ---
    '''
    st.markdown(text)