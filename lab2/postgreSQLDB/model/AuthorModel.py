from model.DBmodel import DBModel
from storages.author import Author
import psycopg2
import time

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

    def add_entity(self , new_entity):
       request = 'INSERT INTO author(name , date_of_first_publication , year_of_birth , year_of_death) VALUES (%s, %s, %s, %s)'
       data = (new_entity.name, new_entity.date_of_first_publication, new_entity.year_of_birth, new_entity.year_of_death)
       try:
           self.cursor.execute(request, data)
           self.conn.commit()
       except(Exception,psycopg2.DatabaseError) as error:
           self.cursor.execute('ROLLBACK')
           print(error)

    def get_entities(self):
        request = 'SELECT * FROM author'
        authors = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if (records != None):
                for record in records:
                    authors.append(Author(record[0] , record[1] , record[2] , record[3] , record[4]))
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        finally:
            return authors

    def update_entity(self , update_entity):
        request = 'UPDATE author SET name = %s , date_of_first_publication = %s , year_of_birth = %s , year_of_death = %s WHERE id = %s'
        data = (update_entity.name , update_entity.date_of_first_publication , update_entity.year_of_birth , update_entity.year_of_death , update_entity.id)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_entity(self , id):
        records = self.get_entities()
        temp = False
        for record in records:
            if(id == record.id):
                temp = True

        if(temp == False):
            print("No author on this id")
            return
        request = 'DELETE FROM author WHERE id = %s'
        try:
            self.delete_links(id)
            self.cursor.execute(request , (id ,))
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entity(self, entity_id):
        request = 'SELECT * FROM author WHERE id = %s'
        author = None
        try:
            self.cursor.execute(request , (entity_id,))
            record = self.cursor.fetchone()
            author = Author(record[0] , record[1] , record[2] ,record[3] , record[4])
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return author

    def set_links(self , first_entity_id , second_entity_id):
        request = 'SELECT * FROM book WHERE id = %s'
        try:
            self.cursor.execute(request , (second_entity_id,))
            book = None
            book = self.cursor.fetchall()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
            return
        request = 'INSERT INTO books_authors(book_id , author_id) VALUES (%s,%s)'
        data = (second_entity_id , first_entity_id)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_links(self , entity_id):
        request = 'DELETE FROM books_authors WHERE author_id = %s'
        try:
            self.cursor.execute(request , (entity_id, ))
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

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