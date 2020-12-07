from bs4 import BeautifulSoup
import glob
from model.DBModel import DBModel
from storage.tables import News
from storage.tables import Statistics
from storage.tables import Tags
from storage.tables import Content
import os
from requests_futures import sessions

dbModel = DBModel('coursework', 'postgres', 'Scorpions', 'localhost')


def read_text_file(path):
    f = open(path, 'rb')
    html_text = f.read()
    f.close()
    return html_text


def get_title(soup):
    try:
        title = soup.find('h1', {'class': 'c-card__title js-si-title'})
        if title is not None:
            title = title.get_text().strip()
        else:
            title = soup.find('div', {'class': 'col-lg-10 col-sm-12'}).find('h1').get_text().strip()
    except:
        title = None
    return title


def get_author(soup):
    try:
        author = soup.find('dl', {'class': 'c-author-dl'})
        if author is not None:
            author = author.get_text().replace("Автор:", "").strip()
        else:
            author = soup.find('div', {'class': 'col-lg-10 col-sm-12'})
            if author is not None:
                author = author.find('p', {'class': 'article__author--bottom'}).find('a').get_text().strip()
            else:
                author = ""
    except:
        author = None
    return author


def get_thema(soup):
    try:
        thema = soup.find('footer', {'class': 'c-card__box c-card__foot'})
        if thema is not None:
            thema = thema.find('a').get_text().strip()
        else:
            thema = soup.find('div', {'class': 'col-lg-10 col-sm-12'}).find('a', {
                'class': 'article__info-item gray-marker'}).get_text().strip()
    except:
        thema = None
    return thema


def get_views(soup):
    try:
        views = soup.find('dd', {'class': 'i-reset--b i-view'})
        if views is not None:
            views = views.get_text().strip()
        else:
            views = soup.find('div', {'class': 'col-lg-10 col-sm-12'}).find('span', {
                'class': 'article__info-item views'}).get_text().strip()
    except:
        views = None
    return views


def get_time(soup):
    try:
        time = soup.find('footer', {'class': 'c-card__foot'})
        if time is not None:
            time = time.find('time').get('datetime').strip()
        else:
            time = soup.find('div', {'class': 'col-lg-10 col-sm-12'}).find('div', {
                'class': 'article__info-item time'}).get_text().strip()
            list_time = time.split(',')
            time = list_time[1] + 'T' + list_time[0].strip()
    except:
        time = None
    return time


def get_tags(soup):
    try:
        list_tags = soup.find('ul', {'class': 'c-tag-list'})
        if list_tags is not None:
            list_tags = list_tags.find_all('li')
            tags = []
            for tag in list_tags:
                tags.append(tag.get_text())
        else:
            list_tags = soup.find('div', {'class': 'col-lg-10 col-sm-12'}).find('div', {
                'class': 'article__tags'}).find_all('a')
            if list_tags is not None:
                tags = []
                for tag in list_tags:
                    tags.append(tag.get_text().strip())
    except:
        tags = None
    return tags


def get_link(soup):
    try:
        link = soup.find('link', {'rel': 'alternate'})
        if link is not None:
            link = link.get('href')
        else:
            link = soup.find('link', {'rel': 'amphtml'})
            if link is not None:
                link = link.get('href')
    except:
        link = None
    return link


def insert_generating_data():
    files = glob.glob('webdata/*.html')
    for file in files:
        html_text = read_text_file(file)
        soup = BeautifulSoup(html_text, 'lxml')
        #############Create News##########################
        title = get_title(soup)
        author = get_author(soup)
        thema = get_thema(soup)
        #############Create Statistics##########################
        views = get_views(soup)
        time = get_time(soup)
        ################Create Tags##############################
        tags = get_tags(soup)
        ##############Create Content#############################
        link = get_link(soup)

        if title is None or link is None or views is None or time is None or thema is None or tags is None:
            os.remove(file)
            continue
        news = News(title, author, thema)
        dbModel.add_entity(news)
        stat = Statistics(news.news_id, views, time)
        dbModel.add_entity(stat)
        cont = Content(news.news_id, link)
        dbModel.add_entity(cont)
        for tag in tags:
            new_tag = Tags(tag, news.news_id)
            dbModel.add_entity(new_tag)
        os.remove(file)


def update_info():
    links = dbModel.get_entities(Content)
    session = sessions.FuturesSession()
    for link in links:
        req = session.get(link.link)
        html_text = req.result().text
        soup = BeautifulSoup(html_text , 'lxml')
        views = get_views(soup)
        if views is None:
            continue
        stat = dbModel.get_entity(Statistics , link.content_id)
        stat.views = views
        dbModel.update_entity(stat)

update_info()
