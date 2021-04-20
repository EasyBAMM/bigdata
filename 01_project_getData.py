from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
'''
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

# comments = soup.select("#replies")
# 댓글 이름
names = soup.select("#replies > span.ytd-comment-renderer")
# 댓글 날짜
days = soup.select("#replies > a.yt-simple-endpoint")
# 댓글 본문
contents = soup.select("#replies > #content-text")
# 댓글 좋아요수
likes = soup.select("#replies > #vote-count-middle")
'''

INTERVAL = 3


def scrape_comment():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(7)
    driver.maximize_window()

    # url = "https://www.youtube.com/watch?v=wYn8TeTMUL4"
    # url = "https://www.youtube.com/watch?v=7guaCiO21iM"
    url = "https://www.youtube.com/watch?v=wZRg4f8uBzw"
    driver.get(url)

    INTERVAL = 3   # 3초에 한번씩 스크롤 내림
    time.sleep(INTERVAL)
    print("스크롤 시작")

    # 스크롤을 가장 아래로 내림(반복수행 전 필수, comment 떠야함)
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight - parseInt(document.documentElement.scrollHeight/2));")
    # comment창 대기
    time.sleep(INTERVAL)

    # 현재 문서 높이를 가져와서 저장
    prev_height = driver.execute_script(
        "return document.documentElement.scrollHeight")

    # 반복 수행
    while True:
        # 스크롤을 가장 아래로 내림
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")

        # 페이지 로딩 대기
        time.sleep(INTERVAL)

        # 현재 문서 높이를 가져와서 저장
        curr_height = driver.execute_script(
            "return document.documentElement.scrollHeight")

        if curr_height == prev_height:
            break
        prev_height = curr_height

    print("스크롤 완료")

    # 유튜브 프리미엄 광고 뜨면 제거
    try:
        premium_banner = driver.find_element_by_link_text("나중에")
        premium_banner.click()
        print("배너 제거 완료")
    except exceptions.NoSuchElementException:
        print("No Banner")

    # 답글 보기 클릭
    print("댓글 보기 시작")
    try:
        replies = driver.find_elements_by_tag_name(
            "ytd-comment-replies-renderer")
        for index, replie in enumerate(replies):
            button = replie.find_element_by_id("button")
            button.send_keys(Keys.ENTER)
            print(f"{index+1}.답글 보기 클릭")
            time.sleep(INTERVAL)

    except exceptions.NoSuchElementException:
        print("답글 보기 없음")
    print("답글 보기 완료")

    # 답글 더보기 클릭
    print("답글 더보기 시작")
    index = 0

    try:
        # 답글 더보기 클릭
        while driver.find_element_by_xpath("//*[@id='continuation']/yt-next-continuation/tp-yt-paper-button/yt-formatted-string").text.strip() != '':
            driver.find_element_by_xpath(
                "//*[@id='continuation']/yt-next-continuation/tp-yt-paper-button").send_keys(Keys.ENTER)
            index += 1
            print(f"{index}.답글 더보기 클릭")
            time.sleep(INTERVAL*4)
    except:
        print("답글 더보기 없음")
    print("답글 더보기 완료")
    # try:
    #     button_wrap = driver.find_elements_by_id("continuation")
    #     for index, button in enumerate(button_wrap):
    #         button.find_element_by_tag_name(
    #             "tp-yt-paper-button").send_keys(Keys.ENTER)
    #         print(f"{index}.답글 더보기 클릭")
    #         time.sleep(INTERVAL*3)
    # except exceptions.NoSuchElementException:
    #     print("답글 더보기 없음")
    # print("답글 더보기 완료")

    print("scrape_comment 완료")
    time.sleep(500)
    # driver.quit()


def get_data():
    # 제목
    # title = browser.find_element_by_xpath(
    #     "//*[@id='container']/h1/yt-formatted-string").text
    # # 조회수
    # wriiten = browser.find_element_by_xpath(
    #     "//*[@id='count']/ytd-video-view-count-renderer/span[1]").text.split()[1]

    # print(f"제목 : {title}")
    # print(f"조회수 : {wriiten}")
    pass


scrape_comment()
