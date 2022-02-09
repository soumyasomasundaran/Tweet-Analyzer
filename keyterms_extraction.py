from get_azure_keywords import get_azure_keywords
import re
import pandas as pd


def remove_links(text):
    text = re.sub(r'http\S+', '', text)
    return text

def remove_hashtags(text):
    text = re.sub(r'#\S+','', text)
    return text

def clean_text(text):
    link_removed = remove_links(text)
    clean_text = remove_hashtags(link_removed)
    return clean_text

def remove_words_with_numbers(keywords):
    for word in keywords:
        if any(map(str.isdigit, word)):
            keywords.remove(word)
    return keywords

def keyterm_extraction(tweets):
    text = ""
    keyword_list = []
    final_text = []        
    for tweet in tweets['Tweet']:
        text = text+tweet
    text = clean_text(text)
    if len(text)>45000:
        while len(text) > 45000:
            final_text.append(text[:45000])
            text = text[45000:]
    final_text.append(text)

    for text in final_text:
        keywords = get_azure_keywords(text)
        keyword_list.extend(keywords)
    keyword_list = remove_words_with_numbers(keyword_list)

    df = pd.DataFrame(keyword_list, columns=["keywords"])
    return df
