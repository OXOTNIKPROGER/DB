from view.view import View
from model.AuthorModel import AuthorModel
from model.BookModel import BookModel
from model.UserModel import UserModel
from model.SubscriptionModel import SubscriptionModel

in_menu = True
authorModel = AuthorModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
bookModel = BookModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
userModel = UserModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
subscriptionModel = SubscriptionModel('lab' , 'postgres' , 'Scorpions' , 'localhost')

while(in_menu):
    info = View.main_menu()
    if(info == 'error'):
        print("Incorrect input")
        continue
    if(info == '1'):
        while True:
            sub_info = View.sub_menu()
            if(sub_info == -1):
                continue
            else:
                break
        if(sub_info == '1'):
            author = View.add_author()
            authorModel.add_entity(author)
            continue
        elif(sub_info == '2'):
            while True:
                id = View.id_find()
                if(id == -1):
                    continue
                else:
                    break
            if(authorModel.get_entity(id) == None):
                print("No author on this id!")
            else:
                authorModel.update_entity(View.update_author(authorModel.get_entity(id)))
        elif(sub_info == '3'):
            while True:
                id = View.id_find()
                if(id == -1):
                    continue
                else:
                    break
            authorModel.delete_entity(id)
        elif(sub_info == '4'):
            while True:
                temp = View.generate_entity()
                if(temp == -1):
                    continue
                else:
                    break
            authorModel.generate(temp)
        elif(sub_info == '5'):
            while True:
                temp = View.find_authors()
                if(temp == -1):
                    continue
                else:
                    break
            if(temp == '1'):
                authors = authorModel.find_alive_author_filter_books()
                for item in authors:
                    View.show_author(item)
            elif(temp == '2'):
                dd = View.input_sort_date()
                authors = authorModel.find_author_filter_date_pub(dd[0], dd[1])
                for item in authors:
                    View.formated_author(item)
            else:
                print("Exit done")
                continue
        elif(sub_info == '6'):
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            if(authorModel.get_entity(id) == None):
                print("No author on this id")
            else:
                View.show_author(authorModel.get_entity(id))
        elif(sub_info == '7'):
            View.set_link_print()
            while True:
                first_id = View.id_find()
                if (first_id == -1):
                    continue
                else:
                    break
            while True:
                second_id = View.id_find()
                if (second_id == -1):
                    continue
                else:
                    break
            authorModel.set_links(first_id , second_id)
        elif(sub_info == '8'):
            View.delete_link_print()
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            authorModel.delete_links(id)
        else:
            continue
    elif(info == '2'):
        while True:
            sub_info = View.sub_menu()
            if (sub_info == -1):
                continue
            else:
                break
        if (sub_info == '1'):
            book = View.add_book()
            bookModel.add_entity(book)
            continue
        elif (sub_info == '2'):
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            if (bookModel.get_entity(id) == None):
                print("No book on this id!")
            else:
                bookModel.update_entity(View.update_book(bookModel.get_entity(id)))
        elif (sub_info == '3'):
            while True:
                id = View.id_find()
                if(id == -1):
                    continue
                else:
                    break
            bookModel.delete_entity(id)
        elif (sub_info == '4'):
            while True:
                temp = View.generate_entity()
                if(temp == -1):
                    continue
                else:
                    break
            bookModel.generate(temp)
        elif (sub_info == '5'):
            books = bookModel.find_book_user()
            for item in books:
                View.formated_book(item)
        elif (sub_info == '6'):
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            if (bookModel.get_entity(id) == None):
                print("No book on this id")
            else:
                View.show_book(bookModel.get_entity(id))
        elif (sub_info == '7'):
            View.set_link_print()
            while True:
                first_id = View.id_find()
                if (first_id == -1):
                    continue
                else:
                    break
            while True:
                second_id = View.id_find()
                if (second_id == -1):
                    continue
                else:
                    break
            bookModel.set_links(first_id, second_id)
        elif (sub_info == '8'):
            View.delete_link_print()
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            bookModel.delete_links(id)
        else:
            continue
    elif(info == '3'):
        while True:
            sub_info = View.sub_menu()
            if (sub_info == -1):
                continue
            else:
                break
        if (sub_info == '1'):
            user = View.add_user()
            userModel.add_entity(user)
            continue
        elif (sub_info == '2'):
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            if (userModel.get_entity(id) == None):
                print("No user on this id!")
            else:
                userModel.update_entity(View.update_user(userModel.get_entity(id)))
        elif (sub_info == '3'):
            while True:
                id = View.id_find()
                if(id == -1):
                    continue
                else:
                    break
            userModel.delete_entity(id)
        elif (sub_info == '4'):
            while True:
                temp = View.generate_entity()
                if(temp == -1):
                    continue
                else:
                    break
            userModel.generate(temp)
        elif (sub_info == '5'):
            while True:
                temp = View.find_users()
                if(temp == -1):
                    continue
                else:
                    break
            if(temp == '1'):
                min = View.input_sort_id()
                max = View.input_sort_id()
                users = userModel.filter_from_id(min , max)
                for item in users:
                    View.show_user(item)
            elif(temp == '2'):
                users = userModel.filter_from_desc()
                for item in users:
                    View.show_user(item)
            elif(temp == '3'):
                users = userModel.filter_from_blacklist()
                for item in users:
                    View.show_user(item)
            else:
                print("Exit done")
                continue
        elif (sub_info == '6'):
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            if (userModel.get_entity(id) == None):
                print("No user on this id")
            else:
                View.show_user(userModel.get_entity(id))
        elif (sub_info == '7'):
            View.set_link_print()
            while True:
                first_id = View.id_find()
                if (first_id == -1):
                    continue
                else:
                    break
            while True:
                second_id = View.id_find()
                if(second_id == -1):
                    continue
                else:
                    break
            userModel.set_links(first_id, second_id)
        elif (sub_info == '8'):
            View.delete_link_print()
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            userModel.delete_links(id)
        else:
            continue
    elif(info == '4'):
        while True:
            sub_info = View.sub_menu()
            if (sub_info == -1):
                continue
            else:
                break
        if (sub_info == '1'):
            subscription = View.add_subscription()
            subscriptionModel.add_entity(subscription)
            continue
        elif (sub_info == '2'):
            while True:
                id = View.id_find()
                if (id == -1):
                    continue
                else:
                    break
            if (subscriptionModel.get_entity(id) == None):
                print("No subscription on this id!")
            else:
                subscriptionModel.update_entity(View.update_subscription(subscriptionModel.get_entity(id)))
        elif (sub_info == '3'):
            while True:
                id = View.id_find()
                if(id == -1):
                    continue
                else:
                    break
            subscriptionModel.delete_entity(id)
        elif (sub_info == '4'):
            while True:
                temp = View.generate_entity()
                if(temp == -1):
                    continue
                else:
                    break
            subscriptionModel.generate(temp)
        elif (sub_info == '5'):
            View.find_subsciption()
        elif (sub_info == '6'):
            while True:
                id = View.id_find()
                if(id == -1):
                    continue
                else:
                    break
            if (subscriptionModel.get_entity(id) == None):
                print("No subscription on this id")
            else:
                View.show_subscription(subscriptionModel.get_entity(id))
        elif (sub_info == '7'):
            print("No realization(1 to many)")
        elif (sub_info == '8'):
            print("No realization(1 to many)")
        else:
            continue
    else:
        in_menu = False
        continue