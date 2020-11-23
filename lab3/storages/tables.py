from sqlalchemy import Table, Column, Integer, ForeignKey, Text, Float , Boolean , Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Books_users(Base):
    __tablename__ = "books_users"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('"user".id'), nullable=False)

    def __init__(self , book_id , user_id):
        self.book_id = book_id
        self.user_id = user_id

class Books_authors(Base):
    __tablename__ = "books_authors"
    id = Column(Integer , primary_key=True)
    book_id = Column(Integer ,  ForeignKey('book.id') , nullable= False)
    author_id = Column(Integer , ForeignKey('author.id'), nullable=False)

    def __init__(self , book_id , author_id):
        self.book_id = book_id
        self.author_id = author_id

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer , primary_key=True)
    title = Column(Text , nullable=False)
    print_date = Column(Date , nullable=False)
    publishing_house = Column(Text , nullable=False)
    authors = relationship("Author" , secondary = "books_authors")
    users = relationship("User" , secondary = "books_users")

    def __init__(self , title , print_date , publishing_house):
        self.title = title
        self.print_date = print_date
        self.publishing_house = publishing_house

class Author(Base):
    __tablename__ = "author"
    id = Column(Integer , primary_key=True)
    name = Column(Text , nullable=False)
    date_of_first_publication = Column(Date , nullable=False)
    year_of_birth = Column(Integer , nullable=False)
    year_of_death = Column(Integer , nullable=False)
    books = relationship("Book" , secondary = "books_authors")

    def __init__(self , name , date_of_first_publication , year_of_birth , year_of_death):
        self.name = name
        self.date_of_first_publication = date_of_first_publication
        self.year_of_death = year_of_death
        self.year_of_birth = year_of_birth

class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key=True)
    name = Column(Text , nullable=False)
    honor = Column(Float , nullable=False)
    blacklist = Column(Boolean , nullable=False)
    children = relationship("Subscription")
    books = relationship("Book" , secondary = "books_users")

    def __init__(self , name , honor , blacklist):
        self.name = name
        self.honor = honor
        self.blacklist = blacklist

class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(Integer , primary_key=True)
    number = Column(Integer , nullable=False)
    price = Column(Integer , nullable=False)
    expire_date = Column(Date , nullable=False)
    number_of_books = Column(Integer , nullable=False)
    user_id = Column(Integer , ForeignKey('user.id') , nullable=False)

    def __init__(self , number , price , expire_date , number_of_books , user_id):
        self.number = number
        self.price = price
        self.expire_date = expire_date
        self.number_of_books = number_of_books
        self.user_id = user_id