# -*- coding: utf-8 -*-

# Sample Python code for youtube.comments.setModerationStatus
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
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
    comment_ids = ["UgzXTbrztdwwDM6kGLJ4AaABAg", "UgwQhgwG83fMDlidaP14AaABAg"]
    moderationStatus_type = ["heldForReview", "published", "rejected"]
    moderationStatus_type = moderationStatus_type[0]
    request = youtube.comments().setModerationStatus(
        id=comment_ids,
        moderationStatus=moderationStatus_type,
        banAuthor=False
    )
    request.execute()

    print(f'{len(comment_ids)}개의 댓글을 {moderationStatus_type}했습니다.')


if __name__ == "__main__":
    main()
