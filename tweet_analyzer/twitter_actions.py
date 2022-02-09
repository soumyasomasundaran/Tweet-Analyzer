import tweepy
from . import config
import pandas as pd
from collections import Counter


def get_client():
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                           consumer_key=config.CONSUMER_KEY,
                           consumer_secret=config.CONSUMER_SECRET,
                           access_token=config.ACCESS_TOKEN,
                           access_token_secret=config.ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)
    return client


def get_user_id(username):
    user = client.get_user(username=username)
    return user.data.id
    


def find_hashtags(user_id):
    hashtag_list = []
    responses = pagination(user_id)
    for response in responses:
        if response.data ==None:
            continue
        else:
            for tweets in response.data:
                if tweets['entities'] is not None:
                    for key, value in tweets['entities'].items():
                        if key == 'hashtags':
                            for hashtag in value:
                                hashtag_list.append(hashtag['tag'])
    return pd.DataFrame(top_10_hashtags(hashtag_list), columns=['Hashtags', 'Count'])


def top_10_hashtags(hash_tag_list):
    if hash_tag_list:
        return Counter(hash_tag_list).most_common(10)


def pagination(user_id):
    responses = tweepy.Paginator(client.get_users_tweets, user_id,
                                 exclude='replies,retweets',
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

    df = pd.DataFrame(tweet_list, columns=["Tweet", "Favourites", "Retweets", "Created"])
    return df


def get_lists_owned(user_id):
    owned_list_dictionary = {}
    owned_list_response = client.get_owned_lists(user_id, expansions="owner_id", list_fields=["follower_count"])
    if owned_list_response.data is not None:
        for item in owned_list_response.data:
            owned_list_dictionary[str(item)] = item['follower_count']
        return owned_list_dictionary
    else:
        return False


def get_lists_followed(user_id):
    followed_list_dictionary = {}
    followed_list_response = client.get_followed_lists(user_id, expansions="owner_id", list_fields=["follower_count"])
    if followed_list_response.data is not None:
        for item in followed_list_response.data:
            followed_list_dictionary[str(item)] = item['follower_count']
        return followed_list_dictionary
    else:
        return False

def get_lists_membership(user_id):
    membership_list_dictionary = {}
    membership_list_response = client.get_list_memberships(user_id, expansions="owner_id", list_fields=["follower_count"])
    if membership_list_response.data is not None:
        for item in membership_list_response.data:
            membership_list_dictionary[str(item)] = item['follower_count']
        return membership_list_dictionary
    else:
        return False


def user_details(username):
    user = {}
    user_response = client.get_user(username=username, user_fields=['public_metrics', 'description', 'url'])
    user_metrics = user_response.data['public_metrics']
    user['description'] = user_response.data['description']
    user['followers'] = user_metrics['followers_count']
    user['following'] = user_metrics['following_count']
    return user


client = get_client()