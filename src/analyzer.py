from datetime import timedelta
from jellyfish import jaro_distance

class Analyzer:
    """Methods for analyzing queries"""
    
    # Acceptable time difference of writing queries
    accpt_min = 1

    # Acceptable coefficient of likeness between queries.
    # The higher coefficient value, the more similar queries should be
    accpt_likeness = 0.7

    # Minimum possible query length
    query_min_len = 2

    def is_acceptable_datetime(prev, cur):
        accpt_time = timedelta(minutes=Analyzer.accpt_min)
        return cur >= prev and cur <= prev + accpt_time

    def is_correction(prev_query, prob_query):
        likeness = 0
        if len(prev_query) < len(prob_query):
            likeness = jaro_distance(prev_query, prob_query[:len(prev_query)])
        else:
            likeness = jaro_distance(prev_query[:len(prob_query)], prob_query)
        return likeness > Analyzer.accpt_likeness
    
    def is_query(prob_query):
        return len(prob_query) >= Analyzer.query_min_len
