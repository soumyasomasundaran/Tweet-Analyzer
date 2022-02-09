import os
from urllib.parse import urlsplit
import pandas as pd

subscription_key = "d9e7b105d4934ffea5a4b760ad05ad7b"
endpoint = "https://text-imorph.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    return TextAnalyticsClient(
        endpoint=endpoint, credential=ta_credential
    )

client = authenticate_client()


def split_text(text: str) -> list:
    final_text = []
    if len(text) > 4500:
        while len(text) > 4500:
            final_text.append(text[:4500])
            text = text[4500:]
    final_text.append(text)
    return final_text


def text_array_to_documents(text_list):
    documents = {"documents": []}
    for num, text in enumerate(text_list):
        documents["documents"].append(
            {"id": str(num + 1), "language": "en", "text": text}
        )
    return documents


def get_azure_keyphrases(documents):
    response = client.extract_key_phrases(documents=documents)[0]
    return response.key_phrases


def get_filename(website_or_path):
    if website_or_path.startswith("http"):
        split_url = urlsplit(website_or_path)
        if len(split_url.path) > 3:
            return split_url.path.replace("/", "") + ".csv"
        else:
            return split_url.netloc + ".csv"
    else:
        return os.path.basename(website_or_path).split(".")[0] + ".csv"


def get_local_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_text(source):
    return get_filename(source), get_local_text(source)


def get_azure_keywords(text):
    text_list = split_text(text)
    print("Getting keywords...")
    keywords = get_azure_keyphrases(text_list)
    
    return keywords
   