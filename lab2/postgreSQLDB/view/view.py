import datetime
from storages.author import Author

class View:

    @staticmethod
    def update_author():
        id = input('Input id:\n')
        if(id.isdigit() == False):
            print('Incorrect number')
            return


    @staticmethod
    def add_author():
        name = input("Input name:\n")
        while True:
            try:
                date = datetime.datetime.strptime(input("Input date of first publication(yyyy-mm-dd):\n") , '%Y-%m-%d')
                break
            except:
                print("Incorrect date format")
                continue
        while True:
            year_of_birth = input("Input year of birth:\n")
            if(year_of_birth.isdigit() == False):
                print("Not a number!")
                continue
            else:
                break
        while True:
            year_of_death = input("Input year of death:\n")
            if(year_of_death.isdigit() == False):
                print("Not a number!")
                continue
            else:
                break
        new_author = Author(0 , name , date , year_of_birth , year_of_death)
        return new_author



    @staticmethod
    def show_all_authors(items):
        print('All Authors: ')
        print('//////////////////////////////////////////////////////////')
        for item in items:
            print('{} id-> {}'.format('Author' , item.id))
            print('{} name-> {}'.format('Author', item.name))
            print('{} date_of_first_publication-> {}'.format('Author', item.date_of_first_publication))
            print('{} year_of_birth-> {}'.format('Author', item.year_of_birth))
            print('{} year_of_death-> {}'.format('Author', item.year_of_death))
            print('//////////////////////////////////////////////////////////')
