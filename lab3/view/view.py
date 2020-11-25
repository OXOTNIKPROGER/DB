import datetime
from storages.tables import Author
from storages.tables import Book
from storages.tables import User
from storages.tables import Subscription

class View:

    @staticmethod
    def set_link_print():
        print("Input main_entity than second")

    @staticmethod
    def delete_link_print():
        print("Input main_entity id")

    @staticmethod
    def id_find():
        id = input("Input id:\n")
        if(id.isdigit() == False):
            print("Not a number")
            return -1
        else:
            return int(id)

    @staticmethod
    def update_author(update_author):
        while True:
            info = input("Choose what field do you want to change:\n1)name\n2)date_of_first_publication\n3)year_of_birth\n4)year_of_death\n5)Exit\n")
            if(info == '1'):
                update_author.name = input("Input name\n")
                continue
            elif(info == '2'):
                try:
                    date = datetime.datetime.strptime(input("Input date of first publication(yyyy-mm-dd):\n") , '%Y-%m-%d')
                except:
                    print("Incorrect data format")
                    continue
                update_author.date_of_first_publication = date
            elif(info == '3'):
                num = input("Input year_of_birth\n")
                if(num.isdigit() == False):
                    print("Not a number")
                    continue
                update_author.year_of_birth = num
            elif(info == '4'):
                num = input("Input year_of_death\n")
                if(num.isdigit() == False):
                    print("Not a number")
                    continue
                update_author.year_of_death = num
            elif(info == '5'):
                print("Quit done")
                return update_author

    @staticmethod
    def update_user(update_user):
        while True:
            info = input(
                "Choose what field do you want to change:\n1)name\n2)honor\n3)blacklist\n4)Exit\n")
            if (info == '1'):
                update_user.name = input("Input name\n")
                continue
            elif (info == '2'):
                honor = input("Input honor(double):\n")
                try:
                    honor = float(honor)
                    if (honor >= 0 and honor <= 1):
                        update_user.honor = honor
                    else:
                        print("Incorrect format")
                        continue
                except:
                    print("Incorrect format")
                    continue
            elif (info == '3'):
                blacklist = input("Input blaclist(True/False):\n")
                if (blacklist == "True" or blacklist == "False"):
                    update_user.blacklist = bool(blacklist)
                    continue
                else:
                    print("Incorrect format")
                    continue
            elif (info == '4'):
                print("Quit done")
                break;
        return update_user

    @staticmethod
    def find_subsciption():
        print("No realization!")

    @staticmethod
    def update_subscription(update_subscription):
        while True:
            info = input(
                "Choose what field do you want to change:\n1)number\n2)price\n3)expire_date\n4)number_of_books\n5)user_id\n6)Exit")
            if (info == '1'):
                num = input("Input number\n")
                if (num.isdigit() == False):
                    print("Not a number")
                    continue
                update_subscription.number = num
            elif (info == '2'):
                num = input("Input price\n")
                if (num.isdigit() == False):
                    print("Not a number")
                    continue
                update_subscription.price = num
            elif (info == '3'):
                try:
                    date = datetime.datetime.strptime(input("Input expire date(yyyy-mm-dd):\n"),
                                                      '%Y-%m-%d')
                except:
                    print("Incorrect data format")
                    continue
                update_subscription.expire_date = date
            elif (info == '4'):
                num = input("Input number of books\n")
                if (num.isdigit() == False):
                    print("Not a number")
                    continue
                update_subscription.number_of_books = num
            elif(info == '5'):
                num = input("Input user_id\n")
                if (num.isdigit() == False):
                    print("Not a number")
                    continue
                update_subscription.user_id = num
            elif(info == '6'):
                print("Quit done")
                return update_subscription

    @staticmethod
    def update_book(update_book):
        while True:
            info = input(
                "Choose what field do you want to change:\n1)title\n2)print_date\n3)publishing_house\n4)Exit\n")
            if (info == '1'):
                update_book.title = input("Input title\n")
                continue
            elif (info == '2'):
                try:
                    date = datetime.datetime.strptime(input("Input print date(yyyy-mm-dd):\n"),
                                                      '%Y-%m-%d')
                except:
                    print("Incorrect data format")
                    continue
                update_book.print_date = date
            elif (info == '3'):
                update_book.publishing_house = input("Input publishing_house\n")
            elif (info == '4'):
                print("Quit done")
                return update_book

    @staticmethod
    def generate_entity():
        number = input("Input generate number\n")
        if(number.isdigit() == False):
            print("Not a number")
            return -1
        else:
            return int(number)

    @staticmethod
    def sub_menu():
        print("Choose action:\n1)Add\n2)Update\n3)Delete\n4)Generate\n5)Find/Filter\n6)Get\n7)Set links\n8)Delete links\nQuit-for exit")
        info = input("Input number\n")
        if(info == '1' or info == '2' or info == '3' or info == '4' or info == '5' or info == '6' or info == '7' or info == '8'):
            return info
        elif(info == 'Quit'):
            print("Exit done")
            return
        else:
            print("Incorrect input")
            return -1

    @staticmethod
    def add_book():
        title = input("Input title:\n")
        while True:
            try:
                date = datetime.datetime.strptime(input("Input print date(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect date format")
                continue
        publishing_house = input("Input publishing house:\n")
        new_book = Book(title, date, publishing_house)
        return new_book

    @staticmethod
    def formated_book(item):
        print("title-> {} ".format(item[0]))
        print("user name-> {} ".format(item[1]))
        print('\n')

    @staticmethod
    def show_user(item):
        print('User id-> {}'.format(item.id))
        print('User name-> {}'.format(item.name))
        print('User honor-> {}'.format(item.honor))
        print('User blacklist-> {}'.format(item.blacklist))
        print('\n')

    @staticmethod
    def show_book(item):
        print('Book id-> {}'.format(item.id))
        print('Book title-> {}'.format(item.title))
        print('Book publishing_house-> {}'.format(item.publishing_house))
        print('\n')

    @staticmethod
    def show_subscription(item):
        print('Subscription id-> {}'.format(item.id))
        print('Subscription number-> {}'.format(item.number))
        print('Subscription expire_date-> {}'.format(item.expire_date))
        print('Subscription number_of_books-> {}'.format(item.number_of_books))
        print('Subscription price-> {}'.format(item.price))
        print('Subscription user_id-> {}'.format(item.user_id))
        print('\n')

    @staticmethod
    def main_menu():
        print("Choose number of option:\n1)Author\n2)Book\n3)User\n4)Subscription\nQuit - for exit")
        info = input("Input number\n")
        if(info == '1' or info == '2' or info == '3' or info == '4' or info == 'Quit'):
            return info
        else:
            print("Incorrect number")
            return 'error'

    @staticmethod
    def add_user():
        name = input("Input name:\n")
        while True:
            honor = input("Input honor(double):\n")
            try:
                honor = float(honor)
                if(honor >= 0 and honor <= 1):
                    break
                else:
                    print("Incorrect format")
                    continue
            except:
                print("Incorrect format")
                continue
        while True:
            blacklist = input("Input blaclist(True/False):\n")
            if (blacklist == "True"):
                blacklist = True
            if (blacklist == "False"):
                blacklist = False
                break
            else:
                print("Incorrect format")
                continue
        new_user = User(name, honor, blacklist)
        return new_user

    @staticmethod
    def add_subscription():
        while True:
            number = input("Input number:\n")
            if(number.isdigit() == False):
                print("Not a number!")
                continue
            else:
                break
        while True:
            price = input("Input price:\n")
            if(price.isdigit() == False):
                print("Not a number!")
                continue
            else:
                break
        while True:
            try:
                date = datetime.datetime.strptime(input("Input expire_date(yyyy-mm-dd):\n") , '%Y-%m-%d')
                break
            except:
                print("Incorrect date format")
                continue
        while True:
            number_of_books = input("Input number of books:\n")
            if(number_of_books.isdigit() == False):
                print("Not a number!")
                continue
            else:
                break
        while True:
            user_id = input("Input user_id:\n")
            if(user_id.isdigit() == False):
                print("Not a number!")
                continue
            else:
                break
        new_subscription = Subscription(number , price , date , number_of_books, user_id )
        return new_subscription

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
        new_author = Author(name , date , year_of_birth , year_of_death)
        return new_author

    @staticmethod
    def input_sort_date():
        while True:
            try:
                min = datetime.datetime.strptime(input("Input min print_date(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect data format")
                continue
        while True:
            try:
                max = datetime.datetime.strptime(input("Input max print_date(yyyy-mm-dd):\n") , '%Y-%m-%d')
                break
            except:
                print("Incorrect data format")
                continue
        return (min , max)

    @staticmethod
    def find_users():
        print("1)Find users sorted by amount subscription from id\n2)Find users sorted by amount subscription desc\n3)Find users with false blacklist order by subscription(amount)\n4)Exit")
        info = input("Choose option:\n")
        if(info == '1' or info == '2' or info == '3' or info == '4'):
            return info
        else:
            print("Incorrect option")
            return -1

    @staticmethod
    def input_sort_id():
        while True:
            temp = input("Input id")
            if(temp.isdigit() == True):
                min = temp
                break
            else:
                print("Incorrect input")
                continue
        return int(min)

    @staticmethod
    def find_authors():
        print("1)Find alive author sorted by amount of books\n2) Find alive authors sorted by book`s print date\n3) Exit")
        info = input("Choose option:\n")
        if(info == '1' or info == '2' or info == '3'):
            return info
        else:
            print("Incorrect option")
            return -1

    @staticmethod
    def get_limit():
        limit = input("Input limit")
        if(limit.isdigit() == True):
            return int(limit)
        else:
            return -1

    @staticmethod
    def formated_author(item):
        print('{} id-> {}'.format('Author', item[0]))
        print('{} name-> {}'.format('Author', item[1]))
        print('{} date_of_first_publication-> {}'.format('Author', item[2]))
        print('{} year_of_birth-> {}'.format('Author', item[3]))
        print('{} year_of_death-> {}'.format('Author', item[4]))
        print('{} book-> {}'.format('Author' , item[5]))
        print('\n')

    @staticmethod
    def show_author(item):
            print('{} id-> {}'.format('Author' , item.id))
            print('{} name-> {}'.format('Author', item.name))
            print('{} date_of_first_publication-> {}'.format('Author', item.date_of_first_publication))
            print('{} year_of_birth-> {}'.format('Author', item.year_of_birth))
            print('{} year_of_death-> {}'.format('Author', item.year_of_death))
            print('\n')
