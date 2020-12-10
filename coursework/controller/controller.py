from controller.controller_functions import update_info, insert_generating_data, delete_old_news, \
    analize_views_per_hour, analize_views, analize_similar, get_all_news, get_news_link
from view.view import View
import time


def wait():
    time.sleep(int(1))


def menu():
    in_menu = True
    while in_menu:
        option = View.find_option()
        if option is 0:
            in_menu = False
            continue
        if option is -1:
            wait()
            continue
        if option is 1:
            View.print_on_update()
            update_info()
            View.print_after_update()
            wait()
            continue
        if option is 2:
            path = View.get_path_to_insert()
            View.inserting_data()
            status = insert_generating_data(path)
            if status is -1:
                View.print_error()
            else:
                View.completed_insert()
            wait()
            continue
        if option is 3:
            result = View.confirm_delete()
            if result is 'Y' or result is 'y':
                delete_old_news()
                View.print_after_delete()
                wait()
                continue
            if result is 'N' or result is 'n':
                wait()
                continue
            if result is -1:
                View.print_error()
                wait()
                continue
        if option is 4:
            analize_views_per_hour()
            wait()
            continue
        if option is 5:
            analize_views()
            wait()
            continue
        if option is 6:
            news_id = View.choose_news()
            if news_id is -1:
                View.print_error()
                wait()
                continue
            result = analize_similar(news_id)
            if result is -1:
                View.print_error()
                wait()
                continue
            for res in result:
                link = get_news_link(res.news_id)
                View.print_news(res, link)
            wait()
            continue
        if option is 7:
            news = get_all_news()
            for item in news:
                View.print_news(item)
            wait()
