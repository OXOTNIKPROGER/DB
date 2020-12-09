from bs4 import BeautifulSoup
import requests

class News_spider:

    def __init__(self , filepath):
        self.urls = ['https://tsn.ua/news', 'https://www.unian.ua/detail/main_news']
        self.filepath = filepath

    def start_requests(self):
        for url in self.urls:
            req = requests.get(url)
            html_text = req.text
            B_soup = BeautifulSoup(html_text, 'lxml')
            soup = B_soup.find_all('a', {'class': 'c-card__link'})
            if(soup == []):
                soup = B_soup.select('div.list-thumbs__info > a')
            for link in soup:
                link = link.get('href')
                req = requests.get(link)
                amount = len(link.split("/"))
                filename = '{}/{}'.format(self.filepath , link.split("/")[amount - 1])
                try:
                    f = open(filename , 'wb')
                except:
                    print("Incorrect path")
                    break
                try:
                    f.write(bytearray(req.text.encode('utf-8')))
                    f.close()
                except:
                    f.close()
                    continue

print('Input relative path from project:')
data = input()
news = News_spider(data)
news.start_requests()
