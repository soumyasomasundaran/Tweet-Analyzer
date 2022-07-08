import streamlit as st
from tweet_analyzer import twitter_actions as ta
from tweet_analyzer import display_elements as display
from tweet_analyzer import style



def main():
    """main logic"""
    if "submit" not in st.session_state:
        st.session_state['submit'] = False

    style.remove_padding()
    style.hide_menu()
    st.header("Tweet Analyzer")
    username = st.text_input("Enter a Twitter handle name").lower().replace("@","")     
    submit_button = st.button('Submit')
    if submit_button or st.session_state['submit']:
        st.session_state['submit'] = True 
        if not username:
            st.warning("Please give an input")
            st.stop()
        with st.spinner('Reading Tweets.'):
            user_id = ta.get_user_id(username)
            if not user_id:
                st.error("User Not Found")
                st.stop()
                

            #fetch data
            user = ta.user_details(username)
            tweets = ta.get_original_tweets(user_id)
            list_owned = ta.get_lists_owned(user_id)
            list_followed = ta.get_lists_followed(user_id)
            list_membership  = ta.get_lists_membership(user_id)


            display.draw_divider()

           
            #user profile and Engagment Chart
            c1, c2 = st.columns((1, 3))
            display.display_user_profile(user, c1)
            st.session_state['days'] = display.display_days_selector(c2)
            display.display_engagement_chart(tweets, c2)
            

            display.draw_divider()

            #Lists
            col1, col2, col3 = st.columns((3, 3, 3))
            display.display_user_lists(list_followed, list_owned, list_membership, col1, col2, col3)


            display.draw_divider()
            if not tweets.empty:         
                col9, col10 = st.columns((2, 2))
                with col9:
                    st.header("Top Hashtags")
                    top_hashtags = ta.find_hashtags(user_id)
                    st.table(top_hashtags)
            
                # All Tweets
                
                with col10:
                    st.header("Tweets")
                    tweets_df = tweets.loc[:,tweets.columns != 'Engagement']
                    st.dataframe(tweets_df)
                    @st.cache
                    def convert_df(df):
                        return df.to_csv().encode('utf-8')
                    csv = convert_df(tweets_df)
                    
                    
                    st.download_button( "Download CSV",data = csv,file_name = f"{username}_tweets.csv",mime="text/plain",key='download-csv')             

                    
                   
            else:
                st.warning("No Tweets to display")




if __name__ =='__main__':

    main()
    
