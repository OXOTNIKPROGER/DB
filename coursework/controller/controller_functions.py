import glob
from bs4 import BeautifulSoup
from model.DBModel import DBModel
from storage.tables import News
from storage.tables import Statistics
from storage.tables import Tags
from storage.tables import Content
import os
import concurrent.futures
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from textwrap import wrap

dbModel = DBModel('coursework', 'postgres', 'Scorpions', 'localhost')
PLOT_LABEL_FONT_SIZE = 14
PLOT_MEANING_FONT_SIZE = 6


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

def get_news_link(news_id):
    contents = dbModel.get_entities(Content)
    for iterator in contents:
        if iterator.content_id == news_id:
            return iterator.link

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


def delete_old_news():
    length = dbModel.get_entities(News).count()
    old_length = int(length * 0.05)
    news = dbModel.get_entities(News).order_by(News.news_id)
    for iterator in range(0, old_length):
        dbModel.delete_News(News, news[0].news_id)


def insert_generating_data(path):
    files = glob.glob('{}/*.html'.format(path))
    if files is []:
        return -1
    for file in files:
        html_text = read_text_file(file)
        soup = BeautifulSoup(html_text, 'lxml')
        title = get_title(soup)
        if dbModel.check_news(News, title):
            os.remove(file)
            continue
        author = get_author(soup)
        thema = get_thema(soup)
        views = get_views(soup)
        time = get_time(soup)
        tags = get_tags(soup)
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
    dbModel.update_themas_Ukraine()
    return 1


class request_result:
    def __init__(self, text, id):
        self.text = text
        self.id = id


def load_url(url, id):
    ans = requests.get(url)
    return request_result(ans.text, id)


def update_info():
    contents = dbModel.get_entities(Content)
    amount = 0
    for content in contents:
        amount = amount + 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=amount) as executor:
        future_to_url = (executor.submit(load_url, content.link, content.content_id) for content in contents)
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            soup = BeautifulSoup(data.text, 'lxml')
            views = get_views(soup)
            if views is None:
                continue
            stat = dbModel.get_entity(Statistics, data.id)
            amount = amount + 1
            stat.views = views
            dbModel.update_entity(stat)


def create_News_arguments_table():
    trends = dbModel.do_request(
        "with thema_views as(SELECT * FROM statistics JOIN news ON statistics_id = news.news_id) SELECT * , current_timestamp - time as duration FROM thema_views")
    df = pd.DataFrame(trends,
                      columns=['statistics_id', 'views', 'time', 'news_id', 'title', 'author', 'thema', 'duration'])
    return df


def getColors(n):
    COLORS = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        COLORS.append(cm(i))
    return COLORS


def get_duration_in_seconds(duration):
    result = duration.days * 24 * 60 * 60 + duration.seconds
    return result


def analize_views():
    df = create_News_arguments_table()
    selected_df = df[['views', 'thema']]
    selected_df = selected_df.groupby('thema')['views'].median().reset_index().sort_values(by=['views'],
                                                                                           ascending=False)
    plt.title('Медіана переглядів станом на {}'.format(datetime.now()), fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(selected_df['thema'], selected_df['views'], color=getColors(len(selected_df['thema'])))
    plt.ylabel('медіанне значення переглядів', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(rotation=90, fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()


def analize_views_per_hour():
    df = create_News_arguments_table()
    speed_data = []
    title_data = []
    news_ids_data = []
    for iterator in range(0, len(df)):
        hours = get_duration_in_seconds(df['duration'][iterator]) / 3600
        speed_data.append((df['views'][iterator] / hours))
        title_data.append(df['title'][iterator])
        news_ids_data.append(df['news_id'][iterator])
    title_data = ['\n'.join(wrap(t, 20)) for t in title_data]
    selected_df = pd.DataFrame({'news_id': news_ids_data, 'title': title_data, 'speed': speed_data})
    selected_df = selected_df.sort_values(by=['speed'], ascending=False).head(10)
    plt.title('Топ 10 найгарячіших новин станом на {}'.format(datetime.now()), fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(selected_df['title'], selected_df['speed'], color=getColors(len(selected_df['title'])))
    plt.ylabel('Швидкість переглядів за годину', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.xticks(fontsize=PLOT_MEANING_FONT_SIZE)
    plt.show()


def get_all_news():
    result = dbModel.get_entities(News).order_by(News.news_id)
    return result


def create_tags_arguments():
    tags = dbModel.do_request(
        "with news_tags as (SELECT * , news.news_id as n_id FROM news JOIN tags ON news.news_id = tags.news_id JOIN statistics ON statistics.statistics_id = news.news_id) SELECT n_id , title , tag , thema , views FROM news_tags")
    df = pd.DataFrame(tags, columns=['n_id', 'title', 'tag', 'thema', 'views'])
    return df


def analize_similar(news_id):
    df = create_tags_arguments()
    selected_df = df[['n_id', 'tag', 'title', 'views']]
    tags_df = selected_df
    selected_df = selected_df.loc[selected_df['n_id'] == news_id]
    if len(selected_df) is 0:
        return -1
    list_of_tags = selected_df['tag']
    selected_df = selected_df[0:0]
    for tag in list_of_tags:
        current_tag_df = tags_df
        current_tag_df = current_tag_df.loc[(current_tag_df['tag'] == tag) & (current_tag_df['n_id'] != news_id)]
        current_tag_df = current_tag_df.sort_values(by='views', ascending=False).head(2)
        if len(current_tag_df) != 0:
            selected_df = selected_df.append(current_tag_df, ignore_index=True)
    result = []
    for news_id in selected_df['n_id']:
        result.append(dbModel.get_entity(News, news_id))
    return result
