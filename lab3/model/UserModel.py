from model.DBmodel import DBModel
from storages.tables import User
from storages.tables import Books_users
import psycopg2
import time
from sqlalchemy import exc

class UserModel(DBModel):
    def __init__(self, dbname, user, password, host):
        super(UserModel, self).__init__(dbname, user, password, host)
        try:
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError , exc.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError ,exc.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entities(self):
        try:
            users = self.session.query(User)
        except(Exception , exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return users

    def get_entity(self , entity_id):
        try:
            user = self.session.query(User).get(entity_id)
            self.session.commit()
        except(Exception , exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return user

    def delete_entity(self , id):
        try:
            self.delete_links(id)
            self.session.query(User).filter_by(id = id).delete()
            self.session.commit()
        except(Exception , exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    def set_links(self , first_entity_id , second_entity_id):
        try:
            new_entity = Books_users(second_entity_id , first_entity_id)
            self.session.add(new_entity)
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            self.session.execute('ROLLBACK')
            print(error)

    def delete_links(self , entity_id):
        try:
            self.session.query(Books_users).filter_by(user_id=entity_id).delete()
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