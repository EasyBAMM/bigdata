import json
import pandas as pd


def open_json_file():
    with open("data/samplejson2.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data


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
    response = open_json_file()
    json_to_pandas(response)
