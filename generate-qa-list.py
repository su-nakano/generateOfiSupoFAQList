from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# Import the function from my_module
from qalistUtil import convert_texts_into_q_with_links_list, push_qa_category_to_qalist, export_to_json

totalTubs = 6 - 1
qaList = []

for i in range(0,totalTubs):

    # Navigate to the URL of the site
    tabNum = i
    url = f'https://www.gmo-office.com/faq/?tab={tabNum}'

    # Set up the Selenium WebDriver (e.g., using Chrome)
    driver = webdriver.Chrome()
    driver.get(url)

    # オフィサポFAQのクラス名が連番でないため（会議室予約FAQだけなぜかicon-07になってる。理想はicon-06なのだが。。）
    icon_number = i + 2 if i == 5 else i + 1
    # タブがクリックできる状態になっているのかを確認した後、クリック
    is_category_active = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'.faq-listtab.js-tabsarea li.icon-0{icon_number}'))
    )
    ActionChains(driver).move_to_element(is_category_active).click().perform()

    # 指定したタブが選択されているか
    is_shown_tab_content = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.fq-list-box.js-tabContents.is-show'))
    )

    # 画面がロードされるまで待つ
    time.sleep(1)


    # Extract the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    category_text = soup.find('li', class_=f'icon-0{icon_number} active').text
    category_title = f'{category_text}に関する質問'

    # Find the second fq-list-box js-tabContents with the class 'is-show'
    faq_section = soup.find('section', class_='fq-list-box js-tabContents is-show')
    # 質問のタイトルの場所を確認
    question_titles = faq_section.find('dl', class_='faqlist__item js-faqAccordion')
    # 'lazyload' か 'lazyloaded' がクラス名になっている質問Elementを抽出
    if len(question_titles.find_all('dt', class_='lazyloaded')) > 0:
        faq_elements = question_titles.find_all('dt', class_='lazyloaded')
    elif len(question_titles.find_all('dt', class_='lazyload')) > 0:
        faq_elements = question_titles.find_all('dt', class_='lazyload')

    # Elementのテキスト部分のみを抽出
    faq_texts = [faq.text.strip() for faq in faq_elements]
    # 質問文へのLinkを抽出
    faq_text_links = [ f'{url}#{i+1}' for i in range(0,len(faq_elements))]

    # カテゴリの塊を作成
    qa_list = convert_texts_into_q_with_links_list(category_title, faq_texts, faq_text_links, i)

    # QAリストに格納
    push_qa_category_to_qalist(qaList, qa_list)

    # ブラウザ閉じる
    driver.quit()

print(qaList)
# JSON形式で出力
export_to_json(qaList, '.')