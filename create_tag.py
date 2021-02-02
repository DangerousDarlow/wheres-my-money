from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect
from database_queries import add_regex_for_tag, get_or_create_tag


if __name__ == "__main__":
    parser = ArgumentParser(description='Create tag')
    parser.add_argument('name', type=str, help='Name of tag')
    parser.add_argument('regex', type=str, nargs='*', default=[], help='Regular expression matches for tag')
    args = parser.parse_args()

    with connect(dbConnectionString) as dbConnection:
        tag_id = get_or_create_tag(dbConnection, args.name)
        if len(args.regex) > 0:
            add_regex_for_tag(dbConnection, tag_id, args.regex)

        print(tag_id)
