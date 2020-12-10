import os

class View:
    @staticmethod
    def print_header():
        print('###########Аналізатор новин######################')
        print('1)Оновити базу даних новин\n2)Записати згенеровані дані\n3)Видалити старі новини\n4)Знайти найгарячіші '
              'новини '
              '\n5)Знайти найпопулярніші теми новин\n6)Знайти схожі новини\n0) - для виходу')
        print('Введіть номер функції, яку хочете виконати:')
        result = input()
        return result

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
    def print_on_update():
        print('Це може зайняти деякий час(в залежності від розміру даних)')
        print('Якщо хочете прискорити процес, видаліть старі новини, але це може повпливати на точність аналізу')
        print('.....')

    @staticmethod
    def find_option():
        option = View.print_header()
        if option is '0':
            print('########### Програма завершена...')
            return 0
        if View.__check_input(option):
            if option is '1':
                return 1
            if option is '2':
                return 2
            if option is '3':
                return '3'
            if option is '4':
                return 4
            if option is '5':
                return 5
            if option is '6':
                return 6
            print('Неправильний номер опції, введіть знову')
            return -1
        else:
            print('Неправильний формат опції, введіть знову')
            return -1
