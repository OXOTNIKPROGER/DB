class View:
    @staticmethod
    def show_all_authors(items , ):
        print('All Authors: ')
        for item in items:
            print('{} id-> {}'.format(items , item.id))
