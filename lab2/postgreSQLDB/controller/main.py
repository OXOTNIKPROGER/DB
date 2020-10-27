from view.view import View
from model.AuthorModel import AuthorModel
from  model.UserModel import UserModel
from storages.user import User

in_menu = True
in_author_menu = True
in_book_menu = True
in_subscription_menu = True
in_user_menu = True
authorModel = AuthorModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
userModel = UserModel('lab' , 'postgres' , 'Scorpions' , 'localhost')
user = User(4 , 'name1' , 0.1 , True)
records = userModel.get_entity(1)
#records = userModel.update_entity(user)
#for record in records:
   # print(record.name , record.honor)

while in_menu:
    print("Select table:\n1)Author\n2)Book\n3)Subscription\n4)User\n5)Exit\nInput number:")
    main_input = input()
    if(main_input == '1'):
        in_author_menu = True
        while in_author_menu:
            print("Select command:\n1)Add\n2)Update\n3)Delete\n4)Back")
            author_input = input()
            if(author_input == '1'):
                new_author = View.add_author()
                authorModel.add_entity(new_author)
                View.show_all_authors(authorModel.get_entities())
            elif(author_input == '2'):
                pass
            elif(author_input == '3'):
                pass
            elif(author_input == '4'):
                in_author_menu = False
                continue
            else:
                print("Incorrect command!")
                continue
    elif(main_input == '2'):
                in_book_menu = True
                while in_book_menu:
                    print("Select command:\n1)Add\n2)Update\n3)Delete\n4)Back")
                    book_input = input()
                    if (book_input == '1'):
                        pass
                    elif (book_input == '2'):
                        pass
                    elif (book_input == '3'):
                        pass
                    elif (book_input == '4'):
                        in_book_menu = False
                        continue
                    else:
                        print("Incorrect command!")
                        continue
    elif(main_input == '3'):
        in_subscription_menu = True
        while in_subscription_menu:
            print("Select command:\n1)Add\n2)Update\n3)Delete\n4)Back")
            subscription_input = input()
            if (subscription_input == '1'):
                pass
            elif (subscription_input == '2'):
                pass
            elif (subscription_input == '3'):
                pass
            elif (subscription_input == '4'):
                in_subscription_menu = False
                break
            else:
                print("Incorrect command!")
                continue
    elif(main_input == '4'):
        in_user_menu = True
        while in_user_menu:
            print("Select command:\n1)Add\n2)Update\n3)Delete\n4)Back")
            user_input = input()
            if (user_input == '1'):
                pass
            elif (user_input == '2'):
                pass
            elif (user_input == '3'):
                pass
            elif (user_input == '4'):
                in_user_menu = False
                continue
            else:
                print("Incorrect command!")
                continue
    elif(main_input == '5'):
        print("Exit done")
        in_menu = False
        continue
    else:
        print("Incorrect table")
        continue