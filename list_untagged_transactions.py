from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect
from database_queries import get_untagged_transactions


if __name__ == "__main__":
    parser = ArgumentParser(description='List transactions without tags')
    parser.add_argument('--limit', type=int, default=10, help='Maximum number of transactions returned')
    args = parser.parse_args()

    with connect(dbConnectionString) as dbConnection:
        (count, transactions) = get_untagged_transactions(dbConnection, args.limit)
        print(f'{count} transactions without tags')
        print()

        for transaction in transactions:
            print(transaction.to_string())
