from model.DBmodel import DBModel
from storages.tables import Author
from storages.tables import Books_authors
import psycopg2
import time
from sqlalchemy import exc


class AuthorModel(DBModel):
    def __init__(self , dbname , user , password , host ):
        super(AuthorModel, self).__init__(dbname , user, password , host)
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
            authors = self.session.query(Author)
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return authors

    def delete_entity(self , id):
        try:
            self.delete_links(id)
            self.session.query(Author).filter_by(id = id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    def get_entity(self, entity_id):
        try:
            author = self.session.query(Author).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return author

    def set_links(self , first_entity_id , second_entity_id):
        try:
            new_entity = Books_authors(second_entity_id , first_entity_id)
            self.session.add(new_entity)
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            self.session.execute('ROLLBACK')
            print(error)

    def delete_links(self , entity_id):
        try:
            self.session.query(Books_authors).filter_by(author_id = entity_id).delete()
            self.session.commit()
        except(Exception , exc.DatabaseError) as error:
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
        request = 'INSERT INTO "author"(name , date_of_first_publication , year_of_birth , year_of_death) SELECT MD5(random()::text), ' \
                  'timestamp \'1-1-1\' + random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') , trunc(random()*%s)::int , trunc(random()*%s)::int FROM generate_series(1 , %s)'
        data = (number , number , number)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def find_alive_author_filter_books(self):
        request = 'SELECT * FROM "author" WHERE year_of_death = 0 ORDER BY(SELECT COUNT(*) FROM "books_authors" WHERE "books_authors".author_id = "author".id) ASC'
        data = ()
        authors = list()
        try:
            start = time.time()
            self.cursor.execute(request , data)
            temp = self.cursor.fetchall()
            finish = time.time()
            print("///Execution time:")
            print(finish - start)
            for item in temp:
                authors.append(Author(item[0] , item[1] , item[2] , item[3] , item[4]))
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return authors

    def find_author_filter_date_pub(self , min , max):
        request = 'SELECT "author".id , "author".name , "author".date_of_first_publication , "author".year_of_birth , "author".year_of_death , "book".title FROM "author" JOIN "books_authors" ON "books_authors".author_id = "author".id JOIN "book" ON "books_authors".book_id = "book".id WHERE "book".print_date >= %s AND "book".print_date <= %s ORDER BY id ASC'
        data = (min , max)
        authors = list()
        try:
            start = time.time()
            self.cursor.execute(request , data)
            temp = self.cursor.fetchall()
            finish = time.time()
            print("///Execution time:")
            print(finish - start)
            for item in temp:
                author = (item[0] , item[1] , item[2] , item[3] , item[4] , item[5])
                authors.append(author)
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return authors