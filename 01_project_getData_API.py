# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# https://developers.google.com/youtube/v3/docs/commentThreads/list?hl=ko

# Provides YouTube comments in json file and csv file.
# Before Run!!!
# 1. erase Line 19, if you don't use dotenv.
#   If not leave it and pip install python-dotenv. Create an .env file and write down the API_KEY=yourapikey
# 2. check Line 51, your Google YouTube API KEY!
# 3. pip install --upgrade google-api-python-client
# 4. Change Line 58 ~ 64 whatever you want.

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


# total comments
total_data = []


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
        videoId="49ysegAFDoY",
    )
    response = request.execute()

    print(f"************** {count} times left. **************")

    # print(response)

    # append response to total_data
    total_data.append(response)

    # Call recursive when nextPageToken is exist.
    if "nextPageToken" in response:
        get_data(count-1, response["nextPageToken"])
    else:
        print("[End] No more comments.")


def save_response_to_json_file(filepath):
    # save response to JSON file.
    json_data = {"responses": total_data}
    with open(filepath, 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t", ensure_ascii=False)
        print("[INFO] JSON file Saved.")


def open_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        json_file = json.load(f)
    return json_file


def json_file_to_pandas_csv(json_file, filepath):
    print("[INFO] JSON to Pandas Started.")
    json_responses = json_file["responses"]

    id = []
    videoId = []
    item_type = []  # 0: comment, 1: replie
    textDisplay = []
    textOriginal = []
    authorDisplayName = []
    authorChannelUrl = []
    likeCount = []
    # isBad = []

    for json_data in json_responses:
        items = json_data["items"]

        for item in items:
            comment_id = item["snippet"]["topLevelComment"]["id"]
            comment_videoId = item["snippet"]["videoId"]
            comment_textDisplay = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comment_textOriginal = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comment_authorDisplayName = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            comment_authorChannelUrl = item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
            comment_likeCount = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            comment_totalReplyCount = item["snippet"]["totalReplyCount"]

            id.append(comment_id)
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
                    replie_id = replie["id"]
                    replie_videoId = replie["snippet"]["videoId"]
                    replie_textDisplay = replie["snippet"]["textDisplay"]
                    replie_textOriginal = replie["snippet"]["textOriginal"]
                    replie_authorDisplayName = replie["snippet"]["authorDisplayName"]
                    replie_authorChannelUrl = replie["snippet"]["authorChannelUrl"]
                    replie_likeCount = replie["snippet"]["likeCount"]

                    id.append(replie_id)
                    videoId.append(replie_videoId)
                    item_type.append(1)
                    textDisplay.append(replie_textDisplay)
                    textOriginal.append(replie_textOriginal)
                    authorDisplayName.append(replie_authorDisplayName)
                    authorChannelUrl.append(replie_authorChannelUrl)
                    likeCount.append(replie_likeCount)

    data = {'id': id, 'videoId': videoId, 'item_type': item_type, 'authorDisplayName': authorDisplayName,
            'textDisplay': textDisplay, 'textOriginal': textOriginal, 'authorChannelUrl': authorChannelUrl, 'likeCount': likeCount}

    df = pd.DataFrame(data)
    df["category"] = "game"
    df["isBad"] = 0
    # print(df.tail())

    print("[INFO] JSON to Pandas Finished.")
    df.to_csv(filepath)
    print("[INFO] CSV File save Finished.")


if __name__ == "__main__":
    get_data(1)
    save_response_to_json_file("data/json/myvideocomment.json")
    json_file = open_json_file("data/json/myvideocomment.json")
    json_file_to_pandas_csv(json_file, "data/csv/myvideocomment.csv")
    print("[INFO] Finished.")
