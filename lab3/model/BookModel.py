from model.DBmodel import DBModel
from storages.tables import Book
from storages.tables import Books_authors
from storages.tables import Books_users
import psycopg2
import time
from sqlalchemy import exc

class BookModel(DBModel):
    def __init__(self , dbname , user , password , host ):
        super(BookModel, self).__init__(dbname , user, password , host)
        try:
            self.cursor = self.conn.cursor()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entities(self):
        try:
            books = self.session.query(Book)
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return books

    def delete_entity(self, id):
        try:
            self.delete_links(id)
            self.session.query(Book).filter_by(id = id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    def get_entity(self, entity_id):
        try:
            book = self.session.query(Book).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return book

    def set_links(self, first_entity_id, second_entity_id):
        try:
            new_entity = Books_authors(first_entity_id , second_entity_id)
            self.session.add(new_entity)
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            self.session.execute('ROLLBACK')
            print(error)

    def delete_links(self, entity_id):
        try:
            self.session.query(Books_users).filter_by(book_id=entity_id).delete()
            self.session.query(Books_authors).filter_by(book_id=entity_id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    def __get_generate_datas(self , request , data):
        try:
            self.cursor.execute(request, data)
            datas = self.cursor.fetchall()
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return datas

    def generate(self, number):
        request = 'INSERT INTO "book"(title , print_date , publishing_house) SELECT MD5(random()::text), timestamp \'1-1-1\' + random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') , MD5(random()::text) FROM generate_series(1 , %s)'
        data = (number , )
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
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
            self.cursor.execute('ROLLBACK')
            print(error)
        return connections