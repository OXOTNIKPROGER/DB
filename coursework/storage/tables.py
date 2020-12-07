from sqlalchemy import Column, Integer, ForeignKey, Text, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    news_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    thema = Column(Text, nullable=False)
    children = relationship('Tags')

    def __init__(self, title, author, thema):
        self.title = title
        self.author = author
        self.thema = thema


class Tags(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True)
    tag = Column(Text, nullable=False)
    news_id = Column(Integer, ForeignKey('news.news_id'), nullable=False)

    def __init__(self, tag, news_id):
        self.tag = tag
        self.news_id = news_id


class Statistics(Base):
    __tablename__ = "statistics"
    statistics_id = Column(Integer, ForeignKey('news.news_id'), primary_key=True)
    views = Column(Integer, nullable=False)
    time = Column(Time, nullable=False)

    def __init__(self, statistics_id, views, time):
        self.statistics_id = statistics_id
        self.views = views
        self.time = time


class Content(Base):
    __tablename__ = "content"
    content_id = Column(Integer, ForeignKey('news.news_id'), primary_key=True)
    link = Column(Text, nullable=False)

    def __init__(self, content_id, link):
        self.content_id = content_id
        self.link = link
