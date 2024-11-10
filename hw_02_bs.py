import requests
from bs4 import BeautifulSoup
import urllib.parse
# from fake_useragent import UserAgent

'''
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте во всех категориях: 
название, 
цену, 
количество товара в наличии (In stock (19 available)) в формате integer,
описание.
'''

# Запрос веб-страницы
# url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
# base_url = 'https://books.toscrape.com/catalogue/page-50.html'
base_url = 'https://books.toscrape.com/catalogue/'
max_page = 2


headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}

book_urls = []
for i in range(max_page):
    dop_url = f'page-{i + 1}.html'
    url = base_url + dop_url
    response = requests.get(url)
    # https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html


# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    for book in soup.find_all('article',('class', 'product_pod')):
        b_url = book.find('h3').find('a').get('href')
        book_urls.append(base_url + b_url)

        data = []

#  по полученному списку ссылок - проходим СУпом и собираем то, что нужно.
    for i_url in book_urls:
        row_data = {}
        response = requests.get(i_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # ------------- сами данные ---------
        title = soup.find('div',('class', 'col-sm-6 product_main')).find('h1').text
        price = soup.find('div',('class', 'col-sm-6 product_main')).find('p',('class', 'price_color')).text
        sclad_t = soup.find('div',('class', 'col-sm-6 product_main')).find('p',('class', 'instock availability')).text
        sclad = sclad_t.replace('\n\n    \n        In stock (', '').replace(')\n    \n','')
        description = soup.find('div',('class', 'sub-header')).find_next_sibling('p')
        row_data['title'] = title
        row_data['price'] = price
        row_data['sclad'] = sclad
        row_data['description'] = description
        data.append(row_data)
        print(row_data)

import pandas as pd
df = pd.DataFrame(data)
print(data)

print(book_urls)
print(len(book_urls))