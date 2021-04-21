# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# https://developers.google.com/youtube/v3/docs/commentThreads/list?hl=ko

# pip install --upgrade google-api-python-client

import os

import googleapiclient.discovery
from pyasn1.type.univ import Null


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "YOUR_API_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # example >> part="id, snippet, replies", pageToken="dsdsdd", maxResults=100, videoId="X9IeRJmBL7g"
    request = youtube.commentThreads().list(
        part="id, snippet, replies",
        videoId="49ysegAFDoY",
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
