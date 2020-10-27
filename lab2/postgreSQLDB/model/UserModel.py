from model.DBmodel import DBModel
from storages.user import User
import psycopg2

class UserModel(DBModel):
    def __init__(self, dbname, user, password, host):
        super(UserModel, self).__init__(dbname, user, password, host)
        try:
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_entities(self):
        request = 'SELECT * FROM "user" AS u LEFT JOIN subscription AS s ON(s.user_id = u.id)'
        users = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if(records != None):
                for record in records:
                    users.append(User(record[0] , record[1] , record[2] , record[3]))
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return users

    def get_entity(self , entity_id):
        request = 'SELECT * FROM "user" WHERE id = %s'
        data = (entity_id, )
        user = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchall()
            print(record)
            user = User(record[0] , record[1] , record[2] , record[3])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return user

    def add_entity(self , new_entity):
        request = 'INSERT INTO "user"(name , honor , blacklist) VALUES (%s , %s , %s)'
        data = (new_entity.name , new_entity.honor , new_entity.blacklist)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def update_entity(self , update_entity):
        request = 'UPDATE "user" SET name = %s , honor = %s , blacklist = %s WHERE id = %s'
        data = (update_entity.name , update_entity.honor , update_entity.blacklist , update_entity.id)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def delete_entity(self , id):
        records = self.get_entities()
        temp = False
        for record in records:
            if (id == record.id):
                temp = True

        if (temp == False):
            print("No user on this id")
            return
        request = 'DELETE FROM "user" WHERE id = %s'
        try:
            self.delete_links(id)
            self.cursor.execute(request, (id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def set_links(self , first_entity_id , second_entity_id):
        request = 'SELECT * FROM book WHERE id = %s'
        try:
            self.cursor.execute(request, (second_entity_id,))
            book = self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        if (self.get_entity(first_entity_id) == None or book == None):
            print('No entities on this ids')
            return
        request = 'INSERT INTO books_users(book_id , user_id) VALUES (%s,%s)'
        data = (second_entity_id, first_entity_id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def delete_links(self , entity_id):
        records = self.get_entities()
        temp = False
        for record in records:
            if (entity_id == record.id):
                temp = True
        if (temp == False):
            print("No user on this id")
            return
        request = 'DELETE FROM books_users WHERE users_id = %s'
        try:
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)