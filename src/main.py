import sys

from query_parser import QueryParser
from reporter import Reporter

if __name__ == "__main__":
    filename = 'raw_search_data.csv'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    parser = QueryParser(filename)
    try:
        parser.run()
    except FileNotFoundError:
        print("File does't exist")
        exit(1)

    reporter = Reporter(parser.stat)

    #TODO: Make file output
    print("REPORT")
    
    print("\nQuery top for RUSSIAN language of device WITHOUT categories")
    print(reporter.get_top_ru_queries(10, with_category=False))

    print("\nQuery top for ENGLISH language of device WITHOUT categories")
    print(reporter.get_top_eng_queries(10, with_category=False))

    print("\nQuery top for ENGLISH language of device WITH categories")
    print(reporter.get_top_eng_queries(10, with_category=True))

    print("\nQuery top writing from MOSCOW")
    print(reporter.get_top_queries_from_Moscow(10))

    print("\nCategory queries top for RUSSIAN language of device")
    print(reporter.get_top_ru_category_queries(10))

    print("\nCategory queries top for ENGLISH language of device")
    print(reporter.get_top_eng_category_queries(10))
