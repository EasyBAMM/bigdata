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


def get_api_key():
    ''' 
    Youtube API Key
    '''
    config = dotenv_values(".env")
    return config['API_KEY']


def main(count=999999, nextPageToken=""):
    '''
    Change YOUR_API_KEY!!!
    Recursively receive data as much as maxResults through API. 
    Limit API calls to count parameter.
    '''
    # Check count
    if count < 1:
        print("[END] Count")
        return

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = get_api_key()  # "YOUR_API_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Document reference
    # example >> part="id, snippet, replies", pageToken="dsdsdd", maxResults=100, videoId="49ysegAFDoY"
    request = youtube.commentThreads().list(
        part="id, snippet, replies",
        pageToken=nextPageToken,
        maxResults=100,
        videoId="49ysegAFDoY",
    )
    response = request.execute()

    print(f"************** {count} times left. **************")

    with open('samplejson2.json', 'w', encoding="utf-8") as make_file:
        json.dump(response, make_file, indent="\t", ensure_ascii=False)

    print(response)

    # Call recursive when nextPageToken is exist.
    if "nextPageToken" in response:
        main(count-1, response["nextPageToken"])
    else:
        print("[End] No more comments.")


if __name__ == "__main__":
    main()
