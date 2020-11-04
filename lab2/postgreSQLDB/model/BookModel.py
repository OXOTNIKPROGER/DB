from model.DBmodel import DBModel
from storages.book import Book
import psycopg2
import time

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
            self.conn.close()
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
            if (records != None):
                for record in records:
                    books.append(Book(record[0] , record[1] , record[2] , record[3]))
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return books

    def update_entity(self, update_entity):
        request = 'UPDATE book SET title = %s , print_date = %s , publishing_house = %s WHERE id = %s'
        data = (update_entity.title, update_entity.print_date, update_entity.publishing_house, update_entity.id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def delete_entity(self, id):
        records = self.get_entities()
        temp = False
        for record in records:
            if (id == record.id):
                temp = True

        if (temp == False):
            print("No book on this id")
            return
        request = 'DELETE FROM book WHERE id = %s'
        try:
            self.delete_links(id)
            self.cursor.execute(request, (id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_entity(self, entity_id):
        request = 'SELECT * FROM book WHERE id = %s'
        book = None
        try:
            self.cursor.execute(request, (entity_id,))
            record = self.cursor.fetchone()
            book = Book(record[0], record[1], record[2], record[3])
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return book

    def set_links(self, first_entity_id, second_entity_id):
        request = 'SELECT * FROM author WHERE id = %s'
        try:
            self.cursor.execute(request, (second_entity_id,))
            author = self.cursor.fetchall()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        if (self.get_entity(first_entity_id) == None or author == None):
            print('No entities on this ids')
            return
        request = 'INSERT INTO books_authors(book_id , author_id) VALUES (%s,%s)'
        data = (first_entity_id, second_entity_id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def delete_links(self, entity_id):
        records = self.get_entities()
        temp = False
        for record in records:
            if (entity_id == record.id):
                temp = True
        if (temp == False):
            print("No book on this id")
            return
        request = 'DELETE FROM books_authors WHERE book_id = %s'
        try:
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __get_generate_datas(self , request , data):
        try:
            self.cursor.execute(request, data)
            datas = self.cursor.fetchall()
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        return datas

    def generate(self, number):
        request = 'INSERT INTO "book"(title , print_date , publishing_house) SELECT MD5(random()::text), timestamp \'1-1-1\' + random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') , MD5(random()::text) FROM generate_series(1 , %s)'
        data = (number , )
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
    def find_book_user(self):
        request = 'SELECT b.title , "user".name FROM "book" b JOIN "books_users" ON b.id = "books_users".book_id JOIN "user" ON "user".id = "books_users".user_id ORDER BY title DESC, name ASC'
        data = ()
        connections = list()
        try:
            start = time.time()
            self.cursor.execute(request , data)
            temp = self.cursor.fetchall()
            finish = time.time()
            print("///Execution time: ")
            print(finish - start)
            for item in temp:
                conne = (item[0] , item[1])
                connections.append(conne)
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        return connections