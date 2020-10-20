import datetime

from model.AuthorModel import AuthorModel
from model.BookModel import BookModel
from storages.book import Book
from storages.author import Author

x = BookModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
au = Book(0 , 'title' , datetime.date(1999 ,1 , 10), "house")
#x.add_entity(au)
#a = x.get_entities()
for x in a:
    print(x.id , x.title, x.publishing_house)
#print(x.id , x.year_of_death)
def print_hi(name):

    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')
