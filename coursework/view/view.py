
class View:
    @staticmethod
    def print_header():
        print('###########Аналізатор новин######################')
        print('1)Оновити базу даних новин\n2)Записати згенеровані дані\n3)Видалити старі новини\n4)Знайти найгарячіші '
              'новини '
              '\n5)Знайти найпопулярніші теми новин\n6)Знайти схожі новини\n7)Вивести усі новини\n0) - для виходу')
        print('Введіть номер функції, яку хочете виконати:')
        result = input()
        return result

    @staticmethod
    def print_news(news):
        print('///////////////////////////////')
        print('id новини -> {}'.format(news.news_id))
        print('Назва новини -> {}'.format(news.title))
        print('тема -> {}'.format(news.thema))

    @staticmethod
    def choose_news():
        print('Виберіть до якої новини знайти схожі(введіть id новини, попередньо скориставшись опцією 7)')
        id = input()
        if id.isdigit() and id is not -1:
            return int(id)
        else:
            return -1

    @staticmethod
    def __check_input(user_input):
        return user_input.isdigit()


    @staticmethod
    def print_after_update():
        print('Дані оновлені')

    @staticmethod
    def print_error():
        print('Виникла неочікувана помилка, спробуйте ще раз')

    @staticmethod
    def get_path_to_insert():
        print('Вкажіть шлях до папки із згенерованими html даними')
        path = input()
        return path

    @staticmethod
    def completed_insert():
        print('Дані записані, користуйтеся')

    @staticmethod
    def inserting_data():
        print('Дані вписуються у базу даних')
        print('...')

    @staticmethod
    def print_after_delete():
        print('Новини ваидалені')

    @staticmethod
    def print_on_update():
        print('Це може зайняти деякий час(в залежності від розміру даних)')
        print('Якщо хочете прискорити процес, видаліть старі новини, але це може повпливати на точність аналізу')
        print('.....')

    @staticmethod
    def confirm_delete():
        print('Ви точно хочете видалити 5 відсотків старих новин?(Y\\N)')
        desicion = input()
        if desicion is 'Y' or desicion is 'y' or desicion is 'N' or desicion is 'n':
            return desicion
        else:
            return -1



    @staticmethod
    def find_option():
        option = View.print_header()
        if option is '0':
            print('###########Програма завершена...################')
            return 0
        if View.__check_input(option):
            if option is '1':
                return 1
            if option is '2':
                return 2
            if option is '3':
                return 3
            if option is '4':
                return 4
            if option is '5':
                return 5
            if option is '6':
                return 6
            if option is '7':
                return 7
            print('Неправильний номер опції, введіть знову')
            return -1
        else:
            print('Неправильний формат опції, введіть знову')
            return -1
