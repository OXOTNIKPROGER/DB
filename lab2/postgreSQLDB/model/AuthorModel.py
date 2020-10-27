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
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def add_entity(self , new_entity):
       request = 'INSERT INTO author(name , date_of_first_publication , year_of_birth , year_of_death) VALUES (%s, %s, %s, %s)'
       data = (new_entity.name, new_entity.date_of_first_publication, new_entity.year_of_birth, new_entity.year_of_death)
       try:
           self.cursor.execute(request, data)
           self.conn.commit()
       except(Exception,psycopg2.DatabaseError) as error:
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
            print(error)

    def get_entity(self, entity_id):
        request = 'SELECT * FROM author WHERE id = %s'
        author = None
        try:
            self.cursor.execute(request , (entity_id,))
            record = self.cursor.fetchall()
            author = Author(record[0] , record[1] , record[2] ,record[3] , record[4])
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        return author

    def set_links(self , first_entity_id , second_entity_id):
        request = 'SELECT * FROM book WHERE id = %s'
        try:
            self.cursor.execute(request , (second_entity_id,))
            book = None
            book = self.cursor.fetchall()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
            return
        request = 'INSERT INTO books_authors(book_id , author_id) VALUES (%s,%s)'
        data = (second_entity_id , first_entity_id)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def delete_links(self , entity_id):
        request = 'DELETE FROM books_authors WHERE author_id = %s'
        try:
            self.cursor.execute(request , (entity_id, ))
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)