import pandas as pd
import json

# merge csv files to one csv.


def merge_each_csv():
    # csv 1~10 통합
    data = []

    for i in range(1, 11):
        path = "data/csv/popular_game_" + str(i) + ".csv"
        df = pd.read_csv(path)
        data.append(df)

    finalDf = pd.concat(data)
    finalDf.to_csv("data/csv/popular_game_sum.csv")


def merge_category_csv():
    # 인기동영상(new, music, game) 모두 병합
    data = []

    df = pd.read_csv("data/csv/popular_new_sum.csv")
    df2 = pd.read_csv("data/csv/popular_music_sum.csv")
    df3 = pd.read_csv("data/csv/popular_game_sum.csv")

    df["category"] = "new"
    df2["category"] = "music"
    df3["category"] = "game"

    data.append(df)
    data.append(df2)
    data.append(df3)
    finalDf = pd.concat(data)
    finalDf.to_csv("data/csv/popular_final_without_music_sum.csv")

    # idx 순서대로 변경해주기
    df = pd.read_csv("data/csv/popular_final_without_music_sum.csv")
    df.reset_index()
    df.to_csv("data/csv/popular_final_without_music_sum2.csv")


if __name__ == "__main__":
    merge_each_csv()
    merge_category_csv()
