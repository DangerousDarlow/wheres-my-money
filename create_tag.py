from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect
from uuid import uuid4


def get_or_create_tag(dbConnection, name):
    insertSql = 'INSERT INTO tags(id, name) VALUES (%s, %s)'
    selectSql = 'SELECT id FROM tags WHERE name = %s'

    with dbConnection.cursor() as dbCursor:
        try:
            id = uuid4()
            dbCursor.execute(insertSql, [id, name])
            return id
        except:
            dbConnection.rollback()
            dbCursor.execute(selectSql, [name])
            result = dbCursor.fetchone()
            return result[0]


def add_regex_for_tag(dbConnection, tagId, regexes):
    insertSql = 'INSERT INTO tags_regex(id, tag_id, regex) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING'
    with dbConnection.cursor() as dbCursor:
        for regex in regexes:
            dbCursor.execute(insertSql, [uuid4(), tagId, regex])


if __name__ == "__main__":
    parser = ArgumentParser(description='Create tag (idempotent)')
    parser.add_argument('name', type=str, help='Name of tag')
    parser.add_argument('regex', type=str, nargs='*', default=[], help='Regular expression matches for tag')
    args = parser.parse_args()

    with connect(dbConnectionString) as dbConnection:
        tag_id = get_or_create_tag(dbConnection, args.name)
        if len(args.regex) > 0:
            add_regex_for_tag(dbConnection, tag_id, args.regex)

        print(tag_id)
