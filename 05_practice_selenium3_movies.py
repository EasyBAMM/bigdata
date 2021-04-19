import requests
from bs4 import BeautifulSoup
import time

url = "https://play.google.com/store/movies/top"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "Accept-Language": "Ko-KR,Ko"
}

res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")


# with open("movie.html", "w", encoding="utf-8") as f:
#     # f.write(res.text)
#     f.write(soup.prettify())    # html 문서를 예쁘게 출력

start = time.time()
movies = soup.find_all("div", attrs={"class": "ImZGtf mpg5gc"})
for movie in movies:
    title = movie.find("div", attrs={"class": "WsMG1c nnK0zc"}).get_text()
    print(title)
end = time.time()
print("time : ", end - start)
