from model.DBmodel import DBModel
from storages.book import Book
import psycopg2

class BookModel(DBModel):
    def __init__(self , dbname , user , password , host ):
        super(BookModel, self).__init__(dbname , user, password , host)
        try:
            self.cursor = self.conn.cursor()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def add_entity(self , new_entity):
       request = 'INSERT INTO book(title , print_date , publishing_house) VALUES (%s, %s, %s)'
       data = (new_entity.title, new_entity.print_date, new_entity.publishing_house)
       try:
           self.cursor.execute(request, data)
           self.conn.commit()
       except(Exception,psycopg2.DatabaseError) as error:
           print(error)

    def get_entities(self):
        request = 'SELECT * FROM book'
        books = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            for record in records:
                books.append(Book(record[0] , record[1] , record[2] , record[3]))
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return books

    def update_entity(self, update_entity):
        pass

    def delete_entity(self, id):
        pass