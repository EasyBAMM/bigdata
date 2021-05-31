# -*- coding: utf-8 -*-

# Sample Python code for youtube.comments.setModerationStatus
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import pandas as pd
from dotenv import dotenv_values
# 모델 예측
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import pickle


def get_api_key():
    ''' 
    Youtube API Key
    '''
    config = dotenv_values(".env")
    return config['API_KEY']


def get_data(videoId):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = get_api_key()   # "YOUR_API_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # example >> part="id, snippet, replies", pageToken="dsdsdd", maxResults=100, videoId="X9IeRJmBL7g"
    request = youtube.commentThreads().list(
        part="id, snippet, replies",
        maxResults=100,
        order="relevance",
        videoId=videoId,
    )
    response = request.execute()

    comment_list = []
    for item in response['items']:
        comment_id = item['id']
        comment_author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_text = item['snippet']['topLevelComment']['snippet']['textOriginal']
        comment_totalReplyCount = item["snippet"]["totalReplyCount"]
        comment_list.append((comment_id, comment_author+" "+comment_text))

        if comment_totalReplyCount != 0:
            replies = item["replies"]["comments"]

            for replie in replies:
                replie_id = replie["id"]
                replie_authorDisplayName = replie["snippet"]["authorDisplayName"]
                replie_textOriginal = replie["snippet"]["textOriginal"]
                comment_list.append(
                    (replie_id, replie_authorDisplayName+" "+replie_textOriginal))
    return comment_list


def preprocessing(comment_list):
    result = []
    for i in range(len(comment_list)):
        comment_id, text = comment_list[i]
        pattern = '[^가-힣 ]|[\t\n\r\f\v]|([ㄱ-ㅎㅏ-ㅣ]+)'
        text = re.sub(pattern, '', text)
        text = re.sub(' +', ' ', text)
        if len(text) > 1:
            result.append((comment_id, text))

    return result


def predict_comments(comment_list):
    comment_bad_ids = []
    for i in range(len(comment_list)):
        comment_id, text = comment_list[i]
        if predict_comment(text):
            comment_bad_ids.append((comment_id))

    print("comment_ids: ", comment_bad_ids)
    return comment_bad_ids


loaded_model = load_model('model/best_model.h5')
with open('model/tokenizer.pkl', 'rb') as input:
    tokenizer = pickle.load(input)
max_len = 181


def predict_comment(new_sentence):
    # pattern = '[^가-힣 ]|[\t\n\r\f\v]|([ㄱ-ㅎㅏ-ㅣ]+)'
    # new_sentence = re.sub(pattern, '', new_sentence)
    new_token = new_sentence.split()
    new_sequences = tokenizer.texts_to_sequences([new_token])
    new_pad = pad_sequences(new_sequences, maxlen=max_len)
    score = float(loaded_model.predict(new_pad))

    # print("score: ", score)
    if score > 0.5:
        print("- {} -> 나쁨({:.2f}%)".format(new_sentence, score*100))
        return True
    else:
        print("- {} -> 괜찮음({:.2f}%)".format(new_sentence, (1-score)*100))
        return False


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main(comment_bad_ids):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # https://developers.google.com/youtube/v3/docs/comments/setModerationStatus

    moderationStatus_type = ["heldForReview", "published", "rejected"]
    moderationStatus_type = moderationStatus_type[0]
    request = youtube.comments().setModerationStatus(
        id=comment_bad_ids,
        moderationStatus=moderationStatus_type,
        banAuthor=False
    )
    request.execute()

    print(f'{len(comment_bad_ids)}개의 댓글을 {moderationStatus_type}했습니다.')


if __name__ == "__main__":
    comment_list = get_data("49ysegAFDoY")  # YouTube videoId
    comment_list = preprocessing(comment_list)
    comment_bad_ids = predict_comments(comment_list)
    main(comment_bad_ids)
