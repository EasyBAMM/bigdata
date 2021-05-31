import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import shutil
import time
from dotenv import dotenv_values
from bs4 import BeautifulSoup

driver = None


def open_web(url="https://youtube.com"):
    global driver
    try:
        shutil.rmtree("log")  # 쿠키 / 캐쉬파일 삭제
    except FileNotFoundError:
        pass

    options = uc.ChromeOptions()

    # setting profile
    # options.user_data_dir = "log"

    # another way to set profile is the below (which takes precedence if both variants are used
    # options.add_argument('--user-data-dir=log')

    # just some options passing in to skip annoying popups
    # --password-store=basic --start-maximized
    options.add_argument(
        '--no-first-run --no-service-autorun')
    driver = uc.Chrome(options=options)
    # known url using cloudflare's "under attack mode"
    driver.get(url)
    print("[INFO] open_web")
    time.sleep(3)


def get_id_pw():
    '''
    Get ID, PW from .env
    '''
    config = dotenv_values(".env")
    return (config['ID'], config['PW'])


def login_web():
    print("[INFO] login_web start")
    id, password = get_id_pw()

    # login button
    login_button = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='buttons']/ytd-button-renderer")))
    print("[INFO] login 버튼을 찾았습니다.")
    login_button.click()
    print("[INFO] login 버튼을 클릭했습니다.")

    # login id input
    login_id = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='identifierId']")))
    login_id.send_keys(id)
    print("[INFO] id 입력했습니다.")
    time.sleep(2)

    # next button
    next_button = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='identifierNext']")))
    print("[INFO] 다음 버튼을 찾았습니다.")
    next_button.click()
    print("[INFO] 다음 버튼을 클릭했습니다.")
    time.sleep(2)

    # login password input
    login_password = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='password']/div[1]/div/div[1]")))
    login_password.click()
    print("[INFO] password 버튼을 찾았습니다.")
    actions = ActionChains(driver)
    actions.send_keys(password)
    actions.perform()
    print("[INFO] password 입력했습니다.")
    time.sleep(2)

    # next button
    next_button = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='passwordNext']")))
    print("[INFO] 다음 버튼을 찾았습니다.")
    next_button.click()
    print("[INFO] 다음 버튼을 클릭했습니다.")
    print("[INFO] 로그인 성공")


def move_videoId(url="https://www.youtube.com/watch?v=49ysegAFDoY"):
    driver.get(url)
    print("[INFO] move_videoId start")
    time.sleep(3)


def scroll_comment():
    print("[INFO] scroll_comment start")
    INTERVAL = 3   # 3초에 한번씩 스크롤 내림
    time.sleep(INTERVAL*2)
    print("[INFO] 스크롤 시작")
    # 스크롤을 가장 아래로 내림(반복수행 전 필수, comment 떠야함)
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(INTERVAL*3)
    # comment창 대기
    # next button
    comment_window = WebDriverWait(driver, timeout=20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='simple-box']")))

    if comment_window:
        print("[INFO] comment_window")
    else:
        print("[ERROR] comment_window")
        time.sleep(INTERVAL*2)

    # 현재 문서 높이를 가져와서 저장
    prev_height = driver.execute_script(
        "return document.documentElement.scrollHeight")

    # 반복 수행
    while True:
        # 스크롤을 가장 아래로 내림
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")

        # 페이지 로딩 대기
        time.sleep(INTERVAL*2)

        # 현재 문서 높이를 가져와서 저장
        curr_height = driver.execute_script(
            "return document.documentElement.scrollHeight")

        if curr_height == prev_height:
            break
        prev_height = curr_height
        print("[INFO] 스크롤 진행중...")

    time.sleep(INTERVAL)
    print("[INFO] 스크롤 완료")

    # 유튜브 프리미엄 광고 뜨면 제거
    try:
        premium_banner = driver.find_element_by_link_text("나중에")
        premium_banner.click()
        print("[INFO] 배너 제거 완료")
    except exceptions.NoSuchElementException:
        print("[INFO] No Banner")

    # 답글 보기 클릭
    print("[INFO] 답글 보기 시작")
    try:
        replies = driver.find_elements_by_tag_name(
            "ytd-comment-replies-renderer")
        for index, replie in enumerate(replies):
            button = replie.find_element_by_id("button")
            button.send_keys(Keys.ENTER)
            print(f"[INFO] {index+1}.답글 보기 클릭")
            time.sleep(INTERVAL*2)

    except exceptions.NoSuchElementException:
        print("[INFO] 답글 보기 없음")
    time.sleep(INTERVAL)
    print("[INFO] 답글 보기 완료")

    # 답글 더보기 클릭
    print("[INFO] 답글 더보기 시작")
    index = 0
    try:
        # 답글 더보기 클릭
        while driver.find_element_by_xpath("//*[@id='continuation']/yt-next-continuation/tp-yt-paper-button/yt-formatted-string").text.strip() != '':
            driver.find_element_by_xpath(
                "//*[@id='continuation']/yt-next-continuation/tp-yt-paper-button").send_keys(Keys.ENTER)
            index += 1
            print(f"[INFO] {index}.답글 더보기 클릭")
            time.sleep(INTERVAL*4)
    except:
        print("[INFO] 답글 더보기 없음")
    time.sleep(INTERVAL)
    print("[INFO] 답글 더보기 완료")

    print("[INFO] 완료")


def get_comments_data():
    print("[INFO] get_comments_data start")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # 'div#text-container > yt-formatted-string#text'
    youtube_authors = soup.select(
        'div#text-container > yt-formatted-string#text')
    youtube_comments = soup.select('yt-formatted-string#content-text')

    authors = []
    comments = []
    for element in youtube_authors:
        print("author: ", element.text)
        authors.append(element.text)
    for element in youtube_comments:
        print("comment: ", element.text)
        comments.append(element.text)

    # data = list(zip(authors, comments))
    # data = [' '.join(x) for x in data]
    # print(data)


def loaded_model():
    # 모델 예측
    global loaded_model
    loaded_model = load_model('best_model.h5')
    max_len = 181


def predict_comment(loaded_model, new_sentence, max_len):
    pattern = '[^가-힣 ]|[\t\n\r\f\v]|([ㄱ-ㅎㅏ-ㅣ]+)'
    new_sentence = re.sub(pattern, '', new_sentence)
    new_token = new_sentence.split()
    vocab_size = 1000
    tokenizer = Tokenizer(num_words=vocab_size)
    new_sequences = tokenizer.texts_to_sequences([new_token])
    new_pad = pad_sequences(new_sequences, maxlen=max_len)
    score = float(loaded_model.predict(new_pad))

    # print("score: ", score)
    if score > 0.5:
        print("- {} -> 나쁨({:.2f}%)".format(new_sentence, score*100))
    else:
        print("- {} -> 괜찮음({:.2f}%)".format(new_sentence, (1-score)*100))


if __name__ == "__main__":
    open_web("https://www.youtube.com/watch?v=49ysegAFDoY")
    # login_web()
    # move_videoId()
    scroll_comment()
    get_comments_data()
    time.sleep(1000)
