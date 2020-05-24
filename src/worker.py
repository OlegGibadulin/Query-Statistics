from geolocator import MoscowIndentifier
from collector import Collector
from analyzer import Analyzer

class Worker:
    """Handle queries of a single user session"""
    def __init__(self, stat):
        self.__stat = stat
        self.__queries = []
    
    def run(self):
        """Handle and store queries of single user"""
        for row in self.__queries:
            query = row['query']
            gps = row['gps']
            locale = row['locale']
            is_from_Moscow = MoscowIndentifier.is_Moscow(gps)
            self.__stat.add_query(query, locale, is_from_Moscow)
    
    def add_query(self, query_data):
        self.__queries.append(query_data)
    
    def handle_query(self, query_data):
        """Add query with checking"""
        if self.__is_unique_query(query_data):
            add_query(query_data)
    
    def __is_unique_query(self, query_data):
        #TODO: Make a correct condition for better analyzing requests
        # from a single user. This function is not used yet.
        prob_query = query_data['query']
        prob_dt = query_data['datetime']
        prob_locale = query_data['locale']
        
        for row in self.__queries:
            query = row['query']
            dt = row['datetime']
            locale = row['locale']
            
            if not Analyzer.is_acceptable_datetime(prob_datetime, dt) or \
                    Analyzer.is_correction(query, prob_query):
                return False
        return True







