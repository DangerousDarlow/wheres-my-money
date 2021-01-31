from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect
from transaction import Transaction


def get_untagged_transactions(dbConnection, limit):
    countTransactions = 'SELECT COUNT(id) FROM transactions t FULL JOIN transactions_tags tt ON t.id = tt.transaction_id WHERE tt.transaction_id IS NULL'
    selectTransactions = 'SELECT id, timestamp, amount, description, added, account FROM transactions t FULL JOIN transactions_tags tt ON t.id = tt.transaction_id WHERE tt.transaction_id IS NULL ORDER BY t.timestamp DESC LIMIT %s'

    with dbConnection.cursor() as dbCursor:
        dbCursor.execute(countTransactions)
        count = dbCursor.fetchone()[0]

        dbCursor.execute(selectTransactions, [limit])
        transactions = [Transaction(row[0], row[1], row[2], row[3], row[4], row[5]) for row in dbCursor.fetchall()]
        return (count, transactions)


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
