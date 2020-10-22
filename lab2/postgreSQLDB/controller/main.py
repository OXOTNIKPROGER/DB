import datetime

from model.AuthorModel import AuthorModel
from model.BookModel import BookModel
from storages.book import Book
from storages.author import Author

x = BookModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
au = Book(5 , 'update_title' , datetime.date(1999 ,1 , 10), 'update_house')
x.update_entity(au)

x.delete_entity(3)
a = x.get_entities()

for item in a:
    print(item.id ,  item.title)

def print_hi(name):

    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')
