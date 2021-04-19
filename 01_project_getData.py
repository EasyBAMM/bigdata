import requests
from bs4 import BeautifulSoup

url = "https://www.youtube.com/watch?v=yQ20jZwDjTE"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
data = []


'''댓글'''
# comments = soup.select("ytd-comment-renderer")
# 댓글 이름
names = soup.select("ytd-comment-renderer > span.ytd-comment-renderer")
for name in names:
    print(name.get_text())
# 댓글 날짜
days = soup.select("ytd-comment-renderer > a.yt-simple-endpoint")
# 댓글 본문
contents = soup.select("ytd-comment-renderer > #content-text")
# 댓글 좋아요수
likes = soup.select("ytd-comment-renderer > #vote-count-middle")

'''댓글-답글'''
# comments = soup.select("#replies")
# 댓글 이름
names = soup.select("#replies > span.ytd-comment-renderer")
# 댓글 날짜
days = soup.select("#replies > a.yt-simple-endpoint")
# 댓글 본문
contents = soup.select("#replies > #content-text")
# 댓글 좋아요수
likes = soup.select("#replies > #vote-count-middle")
