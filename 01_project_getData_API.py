# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# https://developers.google.com/youtube/v3/docs/commentThreads/list?hl=ko

# pip install --upgrade google-api-python-client

import json
import pandas as pd
import googleapiclient.discovery
from dotenv import dotenv_values


def get_api_key():
    ''' 
    Youtube API Key
    '''
    config = dotenv_values(".env")
    return config['API_KEY']


def get_data(count=999999, nextPageToken=""):
    '''
    Change YOUR_API_KEY!!!
    Recursively receive data as much as maxResults through API. 
    Limit API calls to count parameter.
    '''
    # Check count
    if count < 1:
        print("[INFO] Count End.")
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
    # example >> part="id, snippet, replies", maxResults=20, order="relevance", pageToken=nextPageToken, videoId="HNObBsbvxOk",
    request = youtube.commentThreads().list(
        part="id, snippet, replies",
        maxResults=100,
        order="relevance",
        pageToken=nextPageToken,
        videoId="wYn8TeTMUL4",
    )
    response = request.execute()

    print(f"************** {count} times left. **************")

    with open('sample.json', 'w', encoding="utf-8") as make_file:
        json.dump(response, make_file, indent="\t", ensure_ascii=False)
        print("[INFO] Saved.")

    # print(response)

    # Call recursive when nextPageToken is exist.
    if "nextPageToken" in response:
        get_data(count-1, response["nextPageToken"])
    else:
        print("[End] No more comments.")


def json_to_pandas(response):

    json_data = response
    items = json_data["items"]

    videoId = []
    item_type = []  # 0: comment, 1: replie
    textDisplay = []
    textOriginal = []
    authorDisplayName = []
    authorChannelUrl = []
    likeCount = []
    # isBad = []

    for item in items:
        comment_videoId = item["snippet"]["videoId"]
        comment_textDisplay = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comment_textOriginal = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        comment_authorDisplayName = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        comment_authorChannelUrl = item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
        comment_likeCount = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        comment_totalReplyCount = item["snippet"]["totalReplyCount"]

        videoId.append(comment_videoId)
        item_type.append(0)
        textDisplay.append(comment_textDisplay)
        textOriginal.append(comment_textOriginal)
        authorDisplayName.append(comment_authorDisplayName)
        authorChannelUrl.append(comment_authorChannelUrl)
        likeCount.append(comment_likeCount)

        if comment_totalReplyCount != 0:
            replies = item["replies"]["comments"]

            for replie in replies:
                replie_videoId = replie["snippet"]["videoId"]
                replie_textDisplay = replie["snippet"]["textDisplay"]
                replie_textOriginal = replie["snippet"]["textOriginal"]
                replie_authorDisplayName = replie["snippet"]["authorDisplayName"]
                replie_authorChannelUrl = replie["snippet"]["authorChannelUrl"]
                replie_likeCount = replie["snippet"]["likeCount"]

                videoId.append(replie_videoId)
                item_type.append(1)
                textDisplay.append(replie_textDisplay)
                textOriginal.append(replie_textOriginal)
                authorDisplayName.append(replie_authorDisplayName)
                authorChannelUrl.append(replie_authorChannelUrl)
                likeCount.append(replie_likeCount)

    data = {'videoId': videoId, 'item_type': item_type, 'authorDisplayName': authorDisplayName,
            'textDisplay': textDisplay, 'textOriginal': textOriginal, 'authorChannelUrl': authorChannelUrl, 'likeCount': likeCount}

    df = pd.DataFrame(data)
    df["isBad"] = 0
    print(df)


if __name__ == "__main__":
    get_data(1)
    print("[INFO] Finished.")
