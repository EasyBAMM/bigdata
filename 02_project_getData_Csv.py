import pandas as pd

import json
import pandas as pd

num = 10
category = "popular_new_"
src = "data/" + category + str(num) + ".json"
dst = "data/csv/" + category + str(num) + ".csv"


def open_json_file():
    with open(src, "r", encoding="utf-8") as f:
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
    df["category"] = "game"
    df["isBad"] = 0

    df.to_csv(dst)


if __name__ == "__main__":
    response = open_json_file()
    json_to_pandas(response)


# data = []

# for i in range(1, 11):
#     path = "data/csv/popular_new_" + str(i) + ".csv"
#     df = pd.read_csv(path)
#     data.append(df)

# finalDf = pd.concat(data)
# finalDf.to_csv("data/csv/popular_new_sum.csv")


# data = []

# df = pd.read_csv("data/csv/popular_new_sum.csv")
# df2 = pd.read_csv("data/csv/popular_music_sum.csv")
# df3 = pd.read_csv("data/csv/popular_game_sum.csv")

# df["category"] = "new"
# df2["category"] = "music"
# df3["game"] = "game"


# finalDf = pd.concat(data)
# finalDf.to_csv("data/csv/popular_final_sum.csv")
# 인기동영상 모두 병합
