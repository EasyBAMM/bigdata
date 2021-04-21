'''
Quiz ) 부동산 매물(송파 헬리오시티) 정보를 스크래핑 하는 프로그램을 만드시오.

[조회 조건]
1. https://daum.net 접속
2. '송파 헬리오시티' 검색
3. 다음 부동산 부분에 나오는 결과 정보

[출력 결과]
=========== 매물 1 ===========
거래 : 매매
면적 : 84/59 (공급/전용)
가격 : 165,000 (만원)
동 : 214동
층 : 고/23
=========== 매물 2 ===========
거래 : 전세
면적 : 84/59 (공급/전용)
'''

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

url = "https://daum.net"

# 1
browser = webdriver.Chrome()
browser.get(url)

# 2
elem = browser.find_element_by_id("q")
elem.send_keys("송파 헬리오시티")
elem.send_keys(Keys.ENTER)

soup = BeautifulSoup(browser.page_source, "lxml")

# 3
sales = soup.find("table", attrs={"class": "tbl"}).find("tbody").find_all("tr")


for idx, sale in enumerate(sales):
    data = sale.find_all("div", attrs={"class": "txt_ac"})
    trade = data[0].get_text()
    width = data[1].get_text()
    price = data[2].get_text()
    where = data[3].get_text()
    floor = data[4].get_text()

    print(f"=========== 매물 {idx+1} ===========")
    print(f"거래 : {trade}")
    print(f"면적 : {width} (공급/전용)")
    print(f"가격 : {price} (만원)")
    print(f"동 : {where}")
    print(f"층 : {floor}")

browser.quit()
