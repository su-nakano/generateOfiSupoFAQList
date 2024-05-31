from datetime import datetime
import json
import os

from bs4 import BeautifulSoup

def scrape_question_texts(page_source, icon_number, url, iterateNum):
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
    faq_text_links = [ f'{url}#{iterateNum + 1}' for i in range(0,len(faq_elements))]

    return {category_title, faq_texts, faq_text_links}

def scrape_answer_texts(page_source, icon_number, url, iterateNum):
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
    faq_text_links = [ f'{url}#{iterateNum + 1}' for i in range(0,len(faq_elements))]

    return {category_title, faq_texts, faq_text_links}


def convert_texts_into_q_with_links_list(categoryTitle, questionTexts, links, iterateNum):
    # Create the output structure
    output = {
        "categoryId": f'10000{iterateNum}',
        "categoryTitle": categoryTitle,
        "questions": [],
        "answers": []
    }

    # Iterate through questions and links to populate the structure
    for i, (question, link) in enumerate(zip(questionTexts, links)):
        question_id = f"Q{1000 + i}"
        keywords = question.split()
        
        output["questions"].append({
            "id": question_id,
            "title": question,
            "index": keywords
        })
        
        output["answers"].append({
            "id": question_id,
            "content": question,
            "link": link,
            "index": keywords
        })
    
    return output

def push_qa_category_to_qalist(qaList, categoryObj):
    qaList.append(categoryObj)
    return qaList

def create_dir(base_dir):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Create a new directory with the current date and time
    dir_path = os.path.join(base_dir, current_datetime)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def export_to_json(qaList, file_path):
    """Export the qaList object to a JSON file."""
    # Define the file path for the JSON file
    dir_path = create_dir(file_path)
    file_path = os.path.join(dir_path, 'qaList.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(qaList, json_file, ensure_ascii=False, indent=4)