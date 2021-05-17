import json
import pandas as pd


def open_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        json_file = json.load(f)
    return json_file


def json_file_to_pandas_csv(json_file, filepath):
    print("[INFO] JSON to Pandas Started.")
    json_responses = json_file["responses"]

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
    print(df.tail())
    print("[INFO] JSON to Pandas Finished.")


def read_csv_to_pandas():
    # titanic = pd.read_csv("data/titanic.csv")
    pass


def save_pandas_to_csvfile():
    # df = pd.DataFrame(data)
    # df.to_csv("titanic.xlsx", sheet_name="passengers")
    pass


def pandas_concat():
    # res = pd.concat([df_C, df_D])
    pass


def pandas_dropna():
    # df = df.dropna(axis=0)
    pass


if __name__ == "__main__":
    json_file = open_json_file("data/sample.json")
    json_file_to_pandas_csv(json_file, "data/csv/sample.csv")
