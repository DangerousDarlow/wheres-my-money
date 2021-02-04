from argparse import ArgumentParser
from dbConfig import dbConnectionString
from decimal import Decimal
from psycopg2 import connect
from re import compile
from database_queries import get_tag_filters, get_transactions_unordered
from transaction import AmountScalingFactor


if __name__ == "__main__":
    parser = ArgumentParser(description='Associate transactions with tags')
    args = parser.parse_args()

    with connect(dbConnectionString) as dbConnection:
        dbConnection.autocommit = False
        filters = [(row[0], compile(row[1]), row[2]) for row in get_tag_filters(dbConnection)]

        insertSql = 'INSERT INTO transactions_tags(transaction_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING'
        
        transactions = get_transactions_unordered(dbConnection)

        with dbConnection.cursor() as dbCursor:
            for transaction in transactions:
                tags = []
                for filter in filters:
                    # If the tag filter has a condition and that condition is not met then skip this filter
                    if filter[2]:
                        timestamp = transaction.timestamp
                        amount = Decimal(transaction.amount) / AmountScalingFactor
                        if not eval(filter[2], {"__builtins__": None}, {"timestamp": timestamp, "amount": amount}):
                            continue

                    if filter[1].search(transaction.description):
                        dbCursor.execute(insertSql, [transaction.id, filter[0]])

            dbConnection.commit()
