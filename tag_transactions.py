from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect
from re import compile
from database_queries import get_tags_regex, get_transactions_unordered


if __name__ == "__main__":
    parser = ArgumentParser(description='Associate transactions with tags')
    args = parser.parse_args()

    with connect(dbConnectionString) as dbConnection:
        dbConnection.autocommit = False
        matches = [(row[0], compile(row[1])) for row in get_tags_regex(dbConnection)]

        insertSql = 'INSERT INTO transactions_tags(transaction_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING'
        
        transactions = get_transactions_unordered(dbConnection)

        with dbConnection.cursor() as dbCursor:
            for transaction in transactions:
                tags = []
                for match in matches:
                    if match[1].search(transaction.description):
                        dbCursor.execute(insertSql, [transaction.id, match[0]])

            dbConnection.commit()
