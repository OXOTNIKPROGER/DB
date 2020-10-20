import psycopg2
from storages.author import Author
conn = psycopg2.connect(dbname='lab', user='postgres',
                        password='Scorpions', host='localhost')
cursor = conn.cursor()
cursor.execute('SELECT * FROM author')
records = cursor.fetchall()
cursor.close()
conn.close()
x = Author(records[0][0] , records[0][1] , records[0][2] , records[0][3] , records[0][4])

print(x.id , x.year_of_death)
def print_hi(name):

    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')
