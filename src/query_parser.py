from csv import DictReader
from enum import Enum
import logging
import json

from analyzer import Analyzer
from utils import Utils
from collector import Collector
from worker import Worker

class Direction(Enum):
    """Direction of changing query length for searching local maximum"""
    LEFT = -1
    UNDEFINED = 0
    RIGHT = 1


class QueryParser:
    """
    Parses input file, analyzes queries and
    select possible options of completed queries
    """
    def __init__(self, filename):
        self.__filename = filename
        self.__stat = Collector()
        self.__worker = None
        self.__prev_row = None
        self.__lcl_max_row = None
    
    def run(self):
        """Start parsing input file"""
        with open(self.__filename, "r", encoding='utf-8', errors='ignore') as f:
            reader = DictReader(f, delimiter=';')
            self.__search_queries(reader)
    
    @property
    def stat(self):
        return self.__stat

    def __search_queries(self, reader):
        """
        Analyzes neighboring queries and queries whose length is
        local maximum (prev and next queries are shorter).
        Groups in Worker serial queries related to a single user.
        """
        self.__prev_row = next(reader)
        lcl_max = self.__prev_row['query']
        self.__lcl_max_row = self.__prev_row
        self.__create_storage(self.__prev_row)
        direction = Direction.UNDEFINED

        # Parsing input file
        for cur_row in reader:
            prev_query = self.__prev_row['query']
            prev_uid = self.__prev_row['uid']

            cur_query = cur_row['query']
            cur_uid = cur_row['uid']
            
            try:
                prev_dt = Utils.get_datetime_from_str(self.__prev_row['datetime'])
                cur_dt = Utils.get_datetime_from_str(cur_row['datetime'])
            except (ValueError, IndexError):
                logging.basicConfig(filename='query.log', filemode='w', format='%(levelname)s - %(message)s\n')
                logging.warning('wrong query string: ' + json.dumps(cur_row))
                continue

            if prev_uid != cur_uid or \
                not Analyzer.is_acceptable_datetime(prev_dt, cur_dt):
                # Time or senders of prev and cur queries are
                # different. Analyzes prev local maximum and prev query.
                if self.__analyze_max_and_end(lcl_max, prev_query):
                    self.__store_query(self.__prev_row)
                if prev_uid != cur_uid:
                    self.__worker.run()
                    self.__create_storage(cur_row)
                lcl_max = cur_query
                self.__lcl_max_row = cur_row
                direction = Direction.UNDEFINED
            else:
                # Cur and prev queries were written by the same user
                # at the same time
                if len(prev_query) <= len(cur_query):
                    direction = Direction.RIGHT
                    if not Analyzer.is_query(lcl_max):
                        lcl_max = prev_query
                        self.__lcl_max_row = self.__prev_row
                    elif Analyzer.is_query(prev_query) and \
                        self.__contain(cur_query, prev_query) and \
                        not Analyzer.is_correction(prev_query, cur_query):
                        # Using __contain() here is necessary in order to
                        # reduce a big number of calls is_correction().
                        # 
                        # Cur query is longer than prev and greatly differs
                        # from it. Analyzes prev local maximum and prev query.
                        if self.__analyze_max_and_end(lcl_max, prev_query):
                            self.__store_query(self.__prev_row)
                        lcl_max = cur_query
                        self.__lcl_max_row = cur_row
                        direction = Direction.UNDEFINED
                else:
                    if direction == Direction.RIGHT:
                        # Found local maximum.
                        # Analyzes prev and cur local maximum.
                        if self.__analyze_max_and_max(lcl_max, prev_query):
                            lcl_max = prev_query
                            self.__lcl_max_row = self.__prev_row
                    direction = Direction.LEFT
                    if self.__contain(prev_query, cur_query):
                        # Cur query is shorter than prev and greatly differs
                        # from it, so this is a new query.
                        self.__store_query(self.__lcl_max_row)
                        lcl_max = cur_query
                        self.__lcl_max_row = cur_row
                        direction = Direction.UNDEFINED
                        
            self.__prev_row = cur_row
        self.__store_query(self.__lcl_max_row)
    
    def __analyze_max_and_max(self, prev_max, cur_max):
        """
        Analyze prev and cur local max of query.
        Return True if cur local max is unique query.
        """
        if not Analyzer.is_query(prev_max):
            return True
        if prev_max == cur_max:
            return True
        if len(prev_max) <= len(cur_max):
            if Analyzer.is_correction(cur_max, prev_max):
                return True
            else:
                self.__store_query(self.__lcl_max_row)
                return True
        else:
            if not Analyzer.is_correction(cur_max, prev_max):
                self.__store_query(self.__lcl_max_row)
                return True
        return False
    
    def __analyze_max_and_end(self, prev_max, query_end):
        """
        Analyze prev local max and final state of query.
        Return True if final state of query is unique query.
        """
        if not Analyzer.is_query(prev_max):
            return False
        if prev_max == query_end:
            return True
        if len(prev_max) <= len(query_end):
            if Analyzer.is_correction(query_end, prev_max):
                return True
            else:
                self.__store_query(self.__lcl_max_row)
                return True
        else:
            self.__store_query(self.__lcl_max_row)
        return False
    
    def __contain(self, src, part):
        return src.find(part, 0, len(src)) == -1
    
    def __store_query(self, row):
        self.__worker.add_query(row)
    
    def __create_storage(self, row):
        self.__worker = Worker(self.__stat)
