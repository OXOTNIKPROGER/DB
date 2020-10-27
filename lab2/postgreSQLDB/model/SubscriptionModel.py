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

    def add_entity(self, new_entity):
        pass

    def get_entity(self, entity_id):
        request = 'SELECT * FROM subscription WHERE id = %s'
        data = (entity_id,)
        subscription = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchall()
            print(record)
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
        pass

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
