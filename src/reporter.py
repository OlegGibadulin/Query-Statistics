class Reporter:
    """Makes report based on statictics"""
    def __init__(self, stat):
        self.__queries = stat.queries
        self.__sorted_by_count = sorted(self.__queries.items(), \
            key=lambda item: item[1]['ru'] + item[1]['eng'], reverse=True)
    
    def get_top_ru_queries(self, count=-1, with_category=True):
        return self.__get_top_queries(count, with_category, 'ru')
    
    def get_top_eng_queries(self, count=-1, with_category=True):
        return self.__get_top_queries(count, with_category, 'eng')
    
    def get_top_ru_category_queries(self, count=-1):
        return self.__get_top_category_queries(count, 'ru')
    
    def get_top_eng_category_queries(self, count=-1):
        return self.__get_top_category_queries(count, 'eng')
    
    def get_top_queries_from_Moscow(self, count=-1, with_category=True):
        """Gets queries sorted by number of uses from Moscow"""
        sorted_queries = sorted(self.__queries.items(), \
            key=lambda item: item[1]['from_Moscow'], reverse=True)
        res = list()
        added = 0
        if count == -1:
            count = len(sorted_queries)
        
        for i in range(len(sorted_queries)):
            query_data = sorted_queries[i]
            from_Moscow = query_data[1]['from_Moscow']
            if added == count or from_Moscow == 0:
                break
            is_by_category = query_data[1]['is_by_category']
            if with_category or not is_by_category:
                row = {'query': query_data[0], 'from_Moscow': from_Moscow}
                res.append(row)
                added += 1

        return res
    
    def __get_top_category_queries(self, count, locale):
        """Gets queries sorted by number of uses and selected by category"""
        sorted_queries = sorted(self.__queries.items(), \
            key=lambda item: item[1][locale], reverse=True)
        res = list()
        added = 0
        if count == -1:
            count = len(sorted_queries)
        
        for i in range(len(sorted_queries)):
            if added == count:
                break
            query_data = sorted_queries[i]
            is_by_category = query_data[1]['is_by_category']
            if is_by_category:
                ru_count = query_data[1]['ru']
                eng_count = query_data[1]['eng']
                row = {'query': query_data[0], 'ru': ru_count, 'eng': eng_count}
                res.append(row)
                added += 1

        return res
    
    def __get_top_queries(self, count, with_category, locale):
        """Gets queries sorted by number of uses with given locale"""
        sorted_queries = sorted(self.__queries.items(), \
            key=lambda item: item[1][locale], reverse=True)
        res = list()
        added = 0
        if count == -1:
            count = len(sorted_queries)
        
        for i in range(len(sorted_queries)):
            if added == count:
                break
            query_data = sorted_queries[i]
            is_by_category = query_data[1]['is_by_category']
            if with_category or not is_by_category:
                ru_count = query_data[1]['ru']
                eng_count = query_data[1]['eng']
                row = {'query': query_data[0], 'ru': ru_count, 'eng': eng_count}
                res.append(row)
                added += 1

        return res
