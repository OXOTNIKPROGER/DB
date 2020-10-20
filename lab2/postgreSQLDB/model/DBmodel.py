from abc import ABC, abstractmethod
import psycopg2

class DBModel(ABC):
    def __init__(self , dbname_ , user_ , password_ , host_):
        self._dbname = dbname_
        self._user = user_
        self._password = password_
        self._host = host_
        try:
            self.conn = psycopg2.connect(dbname = self._dbname , user = self._user , password = self._password , host = self._host)
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        try:
            self.conn.close()
        except (Exception , psycopg2.DatabaseError) as error:
            print(error)

    @abstractmethod
    def add_entity(self , new_entity):
        pass

    @abstractmethod
    def get_entities(self):
        pass

    @abstractmethod
    def update_entity(self , update_entity):
        pass

    @abstractmethod
    def delete_entity(self , id):
        pass