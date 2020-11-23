from model.DBmodel import DBModel
from storages.tables import Subscription
import psycopg2
from sqlalchemy import exc

class SubscriptionModel(DBModel):
    def __init__(self, dbname, user, password, host):
        super(SubscriptionModel, self).__init__(dbname, user, password, host)
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

    def check_user(self, id):
        try:
            request = 'SELECT * FROM "user" WHERE id = %s'
            data = (id , )
            self.cursor.execute(request , data)
            temp = self.cursor.fetchall()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        if(temp == []):
            print("No user on this id")
            return False
        return True

    def get_entity(self, entity_id):
        try:
            subsc = self.session.query(Subscription).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return subsc

    def get_entities(self):
        try:
            subscs = self.session.query(Subscription)
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return subscs

    def delete_entity(self, id):
        try:
            self.session.query(Subscription).filter_by(id = id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError) as error:
            print(error)
            self.session.execute("ROLLBACK")

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
            self.cursor.execute('ROLLBACK')
            print(error)
        return datas

    def generate(self , number):
        request = 'INSERT INTO "subscription"(number , price , expire_date , number_of_books , user_id) SELECT  trunc(random()*%s)::int, trunc(random()*%s)::int,timestamp \'1-1-1\' ' \
                  '+ random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') , trunc(random()*%s)::int , RANDOM() * (SELECT MAX(id) FROM "user") FROM generate_series(1 , %s)'
        data = (number , number , number , number)
        try:
            self.cursor.execute(request , data)
            self.conn.commit()
        except (Exception , psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
