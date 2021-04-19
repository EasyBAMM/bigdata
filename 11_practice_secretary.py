'''
Project ) 웹 스크래핑을 이용하여 나만의 비서를 만드시오.

[조건]
1. 네이버에서 오늘 서울의 날씨정보를 가져온다.
2. 헤드라인 뉴스 3건을 가져온다.
3. IT 뉴스 3건을 가져온다.
4. 해커스 어학원 홈페이지에서 오늘의 영어 회화 지문을 가져온다.

[출력 예시]

[오늘의 날씨]
위치 : 서울특별시 중구 을지로1가
흐림, 어제보다 00℃ 높아요.
현재 00℃ (최저 00 / 최고 00)
오전 강수확률 00％ / 오후 강수확률 00％

미세먼지 00㎍/㎡ 좋음
초미세먼지 00㎍/㎡  좋음

[헤드라인 뉴스]
1. 무슨 무슨 일이...
  (링크 : https://...)
2. 어떤 어떤 일이...
  (링크 : https://...)
3. 어떤 어떤 일이...
  (링크 : https://...)

[오늘의 영어 회화]
(영어 지문)
Rob: I'm going to the soccer game this evening.
Heidi: Who's playing tonight?

(한글 지문)
Rob: 오늘 저녁에 축구 경기를 보러 갈 거예요.
Heidi: 오늘 저녁에 누가 경기를 하나요?
'''


from bs4 import BeautifulSoup
import requests
import re


def create_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    }
    res = requests.get(url, headers=headers)

    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def print_news(index, title, link):
    print(f"{index+1}. {title}")
    print(f"  (링크 : {link})")


def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.asiw&fbm=0&acr=1&acq=%EC%84%9C%EC%9A%B8&qdt=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"

    soup = create_soup(url)

    # 위치 : 서울특별시 중구 을지로1가
    loc = soup.find("span", attrs={"class": "btn_select"}).get_text()
    # 흐림, 어제보다 00℃ 높아요.
    cast = soup.find("p", attrs={"class": "cast_txt"}).get_text()
    # 현재 00℃ (최저 00 / 최고 00)
    curr_temp = soup.find(
        "p", attrs={"class": "info_temperature"}).get_text().replace("도씨", "")    # 현재온도
    min_temp = soup.find("span", attrs={"class": "min"}).get_text()  # 최저온도
    max_temp = soup.find("span", attrs={"class": "max"}).get_text()  # 최고온도
    # 오전 강수확률 00％ / 오후 강수확률 00％
    morning_rain_rate = soup.find(
        "span", attrs={"class": "point_time morning"}).get_text().strip()  # 오전강수확률
    afternoon_rain_rate = soup.find(
        "span", attrs={"class": "point_time afternoon"}).get_text().strip()  # 오후강수확률

    # 미세먼지 00㎍/㎡ 좋음
    # 초미세먼지 00㎍/㎡  좋음
    dust = soup.find("dl", attrs={"class": "indicator"}).find_all("dd")
    pm10 = dust[0].get_text()
    pm25 = dust[1].get_text()

    # 출력
    print(f"위치 : {loc}")
    print(cast)
    print(f"현재 {curr_temp} (최저 {min_temp} / 최고 {max_temp})")
    print(f"오전 강수확률 {morning_rain_rate} / 오후 강수확률 {afternoon_rain_rate}")
    print()
    print(f"미세먼지 {pm10}")
    print(f"초미세먼지 {pm25}")


def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"

    soup = create_soup(url)

    news_list = soup.find(
        "ul", attrs={"class": "hdline_article_list"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print_news(index, title, link)
    print()


def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)

    news_list = soup.find(
        "ul", attrs={"class": "type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1   # img가 있으면 1번째 a 태그의 정보사용

        a_tag = news.find_all("a")[a_idx]
        title = a_tag.get_text().strip()
        link = a_tag["href"]
        print_news(index, title, link)
    print()


def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]:
        print(sentence.get_text().strip())
    print()

    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2]:
        print(sentence.get_text().strip())
    print()


if __name__ == "__main__":
    scrape_weather()    # 오늘의 날씨 정보 가져오기
    scrape_headline_news()  # 헤드라인 뉴스정보 가져오기
    scrape_it_news()    # IT 뉴스 정보 가져오기
    scrape_english()    # 오늘의 영어 회화 가져오기
