class Categories:
    """Queries by categories"""
    __ru = ['Где поесть', 'Гостиница', 'Продукты', 'Достопримечательность', \
        'WiFi', 'Транспорт', 'Заправка', 'Парковка', 'Шопинг', 'Банкомат', \
        'Ночная жизнь', 'Отдых с детьми', 'Банк', 'Развлечения', 'Больница', \
        'Аптека', 'Полиция', 'Туалет', 'Почта']
    
    __eng = ['Where to eat', 'Hotel', 'Groceries', 'Sight', 'WiFi', \
        'Transport', 'Petrol', 'Parking', 'Shopping', 'ATM', 'Hightlife', \
        'Family holiday', 'Bank', 'Entertainment', 'Hospital', 'Pharmacy', \
            'Police', 'Toilet', 'Post']
    
    def is_in(query):
        return query in Categories.__ru or query in Categories.__eng


class Collector:
    """Collects statistics of queries"""
    def __init__(self):
        self.__queries = dict()

    def add_query(self, query, locale, is_from_Moscow):
        if not query in self.__queries:
            is_by_category = Categories.is_in(query)
            self.__queries[query] = {'ru': 0, 'eng': 0, 'from_Moscow': 0, 'is_by_category': is_by_category}
        
        if self.__is_ru(locale):
            self.__queries[query]['ru'] += 1
        else:
            self.__queries[query]['eng'] += 1

        if is_from_Moscow:
            self.__queries[query]['from_Moscow'] += 1
    
    def __is_ru(self, locale):
        return locale.find('ru', 0, len(locale)) == 0
    
    @property
    def queries(self):
        return self.__queries
