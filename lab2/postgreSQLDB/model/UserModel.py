from model.DBmodel import DBModel
from storages.user import User
import psycopg2
import time

class UserModel(DBModel):
    def __init__(self, dbname, user, password, host):
        super(UserModel, self).__init__(dbname, user, password, host)
        try:
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entities(self):
        request = 'SELECT * FROM "user"'
        users = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if(records != None):
                for record in records:
                    users.append(User(record[0] , record[1] , record[2] , record[3]))
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        finally:
            return users

    def get_entity(self , entity_id):
        request = 'SELECT * FROM "user" WHERE id = %s'
        data = (entity_id, )
        user = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchone()
            user = User(record[0] , record[1] , record[2] , record[3])
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return user

    def add_entity(self , new_entity):
        request = 'INSERT INTO "user"(name , honor , blacklist) VALUES (%s , %s , %s)'
        data = (new_entity.name , new_entity.honor , new_entity.blacklist)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def update_entity(self , update_entity):
        request = 'UPDATE "user" SET name = %s , honor = %s , blacklist = %s WHERE id = %s'
        data = (update_entity.name , update_entity.honor , update_entity.blacklist , update_entity.id)
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
            self.cursor.execute('ROLLBACK')
            print(error)

    def set_links(self , first_entity_id , second_entity_id):
        request = 'SELECT * FROM book WHERE id = %s'
        try:
            self.cursor.execute(request, (second_entity_id,))
            book = self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
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
            self.cursor.execute('ROLLBACK')
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
        request = 'DELETE FROM books_users WHERE user_id = %s'
        try:
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
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
        request = 'INSERT INTO "user"(name , honor , blacklist) SELECT MD5(random()::text), random(), (random()::int)::boolean FROM generate_series(1 , %s)'
        data = (number , )
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def filter_from_id(self , min , max):
        request = 'SELECT * FROM "user" WHERE "user".id >= %s AND "user".id <= %s ORDER BY(SELECT COUNT(*) FROM "subscription" WHERE "subscription".user_id = "user".id)'
        data = (min , max)
        Users = list()
        try:
            start = time.time()
            self.cursor.execute(request , data)
            users = self.cursor.fetchall()
            finish = time.time()
            print("///Execution time: ")
            print(finish - start)
            for item in users:
                Users.append(User(item[0] , item[1] , item[2] , item[3]))
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return Users

    def filter_from_desc(self , limit):
        request = 'SELECT * FROM "user" ORDER BY(SELECT COUNT("subscription".id) FROM "subscription" WHERE "subscription".user_id = "user".id), "user".name DESC LIMIT %s'
        data = (limit , )
        Users = list()
        try:
            start = time.time()
            self.cursor.execute(request , data)
            users = self.cursor.fetchall()
            finish = time.time()
            print("///Execution time: ")
            print(finish - start)
            for item in users:
                Users.append(User(item[0] , item[1] , item[2] , item[3]))
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return Users

    def filter_from_blacklist(self):
        request = 'SELECT * FROM "user" WHERE "user".blacklist = false ORDER BY(SELECT COUNT(id) FROM "subscription" WHERE "subscription".user_id = "user".id)'
        data = ()
        Users = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            users = self.cursor.fetchall()
            finish = time.time()
            print("///Execution time: ")
            print(finish - start)
            for item in users:
                Users.append(User(item[0], item[1], item[2], item[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return Users