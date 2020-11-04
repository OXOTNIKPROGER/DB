from model.DBmodel import DBModel
from storages.subscription import Subscription
import psycopg2

class SubscriptionModel(DBModel):
    def __init__(self, dbname, user, password, host):
        super(SubscriptionModel, self).__init__(dbname, user, password, host)
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

    def check_user(self, id):
        try:
            request = 'SELECT * FROM "user" WHERE id = %s'
            data = (id , )
            self.cursor.execute(request , data)
            temp = self.cursor.fetchall()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        if(temp == []):
            print("No user on this id")
            return False
        return True

    def add_entity(self, new_entity):
        check = self.check_user(new_entity.user_id)
        if(check == False):
            return
        request = 'INSERT INTO subscription(number , price , expire_date , number_of_books , user_id) VALUES (%s, %s, %s, %s, %s)'
        data = (new_entity.number , new_entity.price , new_entity.expire_date , new_entity.number_of_books , new_entity.user_id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_entity(self, entity_id):
        request = 'SELECT * FROM subscription WHERE id = %s'
        data = (entity_id,)
        subscription = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchone()
            subscription = Subscription(record[0], record[1], record[2], record[3] , record[4] , record[5])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return subscription

    def get_entities(self):
        request = 'SELECT * FROM subscription'
        subscriptions = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if (records != None):
                for record in records:
                    subscriptions.append(Subscription(record[0], record[1], record[2], record[3] , record[4] , record[5]))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return subscriptions

    def update_entity(self, update_entity):
        check = self.check_user(update_entity.user_id)
        if (check == False):
            return
        request = 'UPDATE subscription SET number = %s , price = %s , expire_date = %s, number_of_books = %s, user_id = %s WHERE id = %s'
        data = (update_entity.number, update_entity.price, update_entity.expire_date, update_entity.number_of_books , update_entity.user_id, update_entity.id)
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
            print("No subscription on this id")
            return
        request = 'DELETE FROM subscription WHERE id = %s'
        try:
            self.cursor.execute(request, (id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def set_links(self, first_entity_id, second_entity_id):
        pass

    def delete_links(self, entity_id):
        pass

    def __get_generate_datas(self , request , data):
        try:
            self.cursor.execute(request, data)
            datas = self.cursor.fetchall()
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
        return datas

    def generate(self , number):
        request = 'INSERT INTO "subscription"(number , price , expire_date , number_of_books , user_id) SELECT  trunc(random()*%s)::int, trunc(random()*%s)::int,timestamp \'1-1-1\' + random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') , trunc(random()*%s)::int , RANDOM() * (SELECT MAX(id) FROM "user") FROM generate_series(1 , %s)'
        data = (number , number , number , number)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)
