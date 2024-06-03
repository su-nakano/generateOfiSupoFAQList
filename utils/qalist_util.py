from datetime import datetime
import json
import os

from bs4 import BeautifulSoup

def scrape_question_texts(page_source, icon_number, url, iterateNum):
    soup = BeautifulSoup(page_source, 'html.parser')

    category_text = soup.find('li', class_=f'icon-0{icon_number} active').text
    category_title = f'{category_text}に関する質問'

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
    faq_text_links = [ f'{url}#{i + 1}' for i in range(0,len(faq_elements))]

    return category_title, faq_texts, faq_text_links

def scrape_answer_texts(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    faq_section = soup.find('section', class_='fq-list-box js-tabContents is-show')

    # 質問のタイトルの場所を確認
    question_titles = faq_section.find('dl', class_='faqlist__item js-faqAccordion')
    answers =  question_titles.find_all('dd')

    # 文字だけを抽出
    answer_texts = [answer.text.strip() for answer in answers]

    return answer_texts


def convert_texts_into_q_with_links_list(categoryTitle, questionTexts, links, answerTexts, iterateNum):
    # Create the output structure
    output = {
        "categoryId": f'{100000 + iterateNum + 1}',
        "categoryTitle": categoryTitle,
        "questions": [],
        "answers": []
    }

    # Iterate through questions and links to populate the structure
    for i, (question, answer, link) in enumerate(zip(questionTexts, answerTexts, links)):
        question_id = f"Q{(iterateNum+1) * 10000 + i}"
        keywords_question = question.split()
        keywords_answer = answer.split()

        output["questions"].append({
            "id": question_id,
            "title": question,
            "index": keywords_question
        })
        
        output["answers"].append({
            "id": question_id,
            "content": answer,
            "link": link,
            "index": keywords_answer
        })
    
    return output

def convert_category_title_to_group(categoryTitle, iterateNum):
    return {
        "categoryId": f'{100000 + iterateNum + 1}',
        "categoryTitle": categoryTitle,
        "index": categoryTitle.split()
    }
    

def push_obj_to_list(list, obj):
    list.append(obj)
    return list

def push_qa_category_to_first_question_list(firstQuestionList, categoryTitles):

    for(categoryTitle,i) in categoryTitles:
       categoryObj =  {
           'id': f'{100000 + i + 1}',
           'title': categoryTitle,
           'index': categoryTitle.split()
       }
    firstQuestionList.append(categoryObj)
    return firstQuestionList

def create_dir(base_dir):
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    # Create a new directory with the current date and time
    dir_path = os.path.join(base_dir, current_datetime)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def export_to_json(qaList, file_path, file_name):
    """Export the qaList object to a JSON file."""
    # Define the file path for the JSON file
    dir_path = create_dir(file_path)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(qaList, json_file, ensure_ascii=False, indent=4)