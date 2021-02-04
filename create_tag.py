from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect
from database_queries import add_filter_for_tag, get_or_create_tag


if __name__ == "__main__":
    parser = ArgumentParser(description='Create tag')
    parser.add_argument('name', type=str, help='Name of tag')
    parser.add_argument('--regex', type=str, help='Regular expression pattern for tag')
    parser.add_argument('--condition', type=str, help='Python code condition for tag')
    args = parser.parse_args()

    with connect(dbConnectionString) as dbConnection:
        tag_id = get_or_create_tag(dbConnection, args.name)
        if args.regex:
            add_filter_for_tag(dbConnection, tag_id, args.regex, args.condition)

        print(tag_id)
