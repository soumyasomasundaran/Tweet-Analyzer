from collections import Counter
from http.client import BAD_REQUEST
from traceback import print_tb
import tweepy
from . import config
import pandas as pd


def get_client():
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                            wait_on_rate_limit=True)
    return client


def get_user_id(username):
    """returns user_id from username"""
    try:
        user = client.get_user(username=username)
    except:
        return False
    if user.data:
        return user.data.id
    

def find_hashtags(user_id):
    hashtag_list = []
    responses = pagination(user_id)
    for response in responses:
        if response.data is None:
            continue
        else:
            for tweets in response.data:
                if tweets['entities'] is not None:
                    for key, value in tweets['entities'].items():
                        if key == 'hashtags':
                            for hashtag in value:
                                hashtag_list.append(hashtag['tag'])
    return pd.DataFrame(find_top_10_hashtags(hashtag_list), columns=['Hashtags', 'Count'])


def find_top_10_hashtags(hash_tag_list):
    if hash_tag_list:
        return Counter(hash_tag_list).most_common(10)


def pagination(user_id):
    """get paginated reponse from Twitter"""
    responses = tweepy.Paginator(client.get_users_tweets, user_id,
                                 max_results=100,
                                 expansions='referenced_tweets.id',
                                 tweet_fields=['created_at', 'public_metrics', 'entities'])
    return responses


def get_original_tweets(user_id):
    tweet_list = []
    responses = pagination(user_id)
    for response in responses:
        if response.data ==None:
            continue
        else:
            for tweets in response.data:
                tweet_list.append([tweets.text,
                                tweets['public_metrics']['like_count'],
                                tweets['public_metrics']['retweet_count'],
                                tweets['created_at'].date()])

    tweets_dataframe = pd.DataFrame(tweet_list, columns=["Tweet", "Favourites", "Retweets", "Created"])
    return tweets_dataframe


def get_lists_owned(user_id):
    """returns lists owned by a user and follower_count of each list  as dataframe"""
    
    owned_list_dictionary = {}
    owned_list_response = client.get_owned_lists(user_id, expansions="owner_id", list_fields=["follower_count"])
    if owned_list_response.data is not None:
        for item in owned_list_response.data:
            owned_list_dictionary[str(item)] = item['follower_count']
        return owned_list_dictionary
    else:
        return False


def get_lists_followed(user_id):
    """returns lists followed by a user and follower_count of each list  as dataframe"""
    followed_list_dictionary = {}
    followed_list_response = client.get_followed_lists(user_id, expansions="owner_id", list_fields=["follower_count"])
    if followed_list_response.data is not None:
        for item in followed_list_response.data:
            followed_list_dictionary[str(item)] = item['follower_count']
        return followed_list_dictionary
    else:
        return False

def get_lists_membership(user_id):
    """returns lists a user is a member of and follower_count of each list as dataframe"""

    membership_list_dictionary = {}
    membership_list_response = client.get_list_memberships(user_id, expansions="owner_id", list_fields=["follower_count"])
    if membership_list_response.data is not None:
        for item in membership_list_response.data:
            membership_list_dictionary[str(item)] = item['follower_count']
        return membership_list_dictionary
    else:
        return False


def user_details(username):
    """returns public metrics of a user as a dictionary"""
    user = {}
    user_response = client.get_user(username=username, user_fields=['public_metrics', 'description', 'url'])
    user_metrics = user_response.data['public_metrics']
    user['description'] = user_response.data['description']
    user['followers'] = user_metrics['followers_count']
    user['following'] = user_metrics['following_count']
    return user


client = get_client()
