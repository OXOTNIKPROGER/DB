from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor


def load_url(url):
    try:
        html = requests.get(url, stream=True)
        amount = len(url.split("/"))
        filename = '{}/{}'.format(filepath, url.split("/")[amount - 1])
        try:
            f = open(filename, 'wb')
        except:
            print("Incorrect path")
        try:
            f.write(bytearray(html.text.encode('utf-8')))
            f.close()
        except:
            f.close()
    except requests.exceptions.RequestException as e:
        return e


def start_requests(url):
    req = requests.get(url)
    html_text = req.text
    B_soup = BeautifulSoup(html_text, 'lxml')
    if url == 'https://tsn.ua/news':
        soup = B_soup.find_all('a', {'class': 'c-card__link'})
    if url == 'https://www.unian.ua/detail/main_news':
        soup = B_soup.select('div.list-thumbs__info > a')
    link_list = []
    for temp in soup:
        link_list.append(temp.get('href'))
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in link_list:
            threads.append(executor.submit(load_url, url))


while True:
    print('Choose what webpage do you want to parse:')
    print('1)tsn.ua\n2)unian.ua')
    options = input()
    if options.isdigit():
        if int(options) is 1:
            url = 'https://tsn.ua/news'
        elif int(options) is 2:
            url = 'https://www.unian.ua/detail/main_news'
        else:
            print('Incorrect option')
            continue
        print('Input relative path from project:')
        data = input()
        filepath = data
        start_requests(url)
        print('Data generated')
        break
    else:
        print('Incorrect option')
        continue
