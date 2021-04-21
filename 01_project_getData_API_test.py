# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# https://developers.google.com/youtube/v3/docs/commentThreads/list?hl=ko

# pip install --upgrade google-api-python-client

import json
import os

import googleapiclient.discovery
from dotenv import dotenv_values
from pyasn1.type.univ import Null


def get_api_key():
    config = dotenv_values(".env")
    return config['API_KEY']


def hello():
    print("helloworld")


def main(nextPageToken="Null"):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = get_api_key()  # "YOUR_API_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # example >> part="id, snippet, replies", pageToken="dsdsdd", videoId="X9IeRJmBL7g"
    request = youtube.commentThreads().list(
        part="id, snippet, replies",
        pageToken=nextPageToken,
        videoId="7a4OQGyhYeA",
    )
    response = request.execute()

    # JSON to Python
    response = json.loads(response)
    print(response)

    # Call recursive when nextPageToken is exist.
    if response["nextPageToken"]:
        main(response["nextPageToken"])
    else:
        print("[End]")


def sample():
    with open("samplejson.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # print(json_data)
    # print(json.dumps(json_data, indent="\t", ensure_ascii=False))
    print(json_data['nextPageToken'])


if __name__ == "__main__":
    # main()
    sample()
