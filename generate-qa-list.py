from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
# Import the function from my_module
from utils import convert_texts_into_q_with_links_list, push_qa_category_to_qalist, export_to_json
from utils.qalist_util import scrape_answer_texts, scrape_question_texts

# Tabの数 - 1
totalTubs = 6 - 1
# totalTubs = 1 # for test 
qaList = []

for i in range(0, totalTubs):

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

    # Page ソースを取得してBeautifulSoupでスクレイピングする
    page_source = driver.page_source

    # サイトからQAを取得
    category_title, faq_texts, faq_text_links = scrape_question_texts(page_source, icon_number, url, i)
    answer_texts = scrape_answer_texts(page_source)

    # カテゴリの塊を作成
    qa_list = convert_texts_into_q_with_links_list(category_title, faq_texts, faq_text_links, answer_texts, i)

    # QAリストに格納
    push_qa_category_to_qalist(qaList, qa_list)

    # ブラウザ閉じる
    driver.quit()

# print(qaList)
# JSON形式で出力
export_to_json(qaList, '.')