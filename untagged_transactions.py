from argparse import ArgumentParser
from dbConfig import dbConnectionString
from psycopg2 import connect

if __name__ == "__main__":
    parser = ArgumentParser(description='List transactions without tags')
    parser.add_argument('--limit', type=int, default=10, help='Maximum number of transactions returned')
    args = parser.parse_args()

    countTransactions = 'SELECT COUNT(id) FROM transactions t FULL JOIN transactions_tags tt ON t.id = tt.transaction_id WHERE tt.transaction_id IS NULL'
    selectTransactions = 'SELECT id, timestamp, description, readable(amount) FROM transactions t FULL JOIN transactions_tags tt ON t.id = tt.transaction_id WHERE tt.transaction_id IS NULL ORDER BY t.timestamp DESC LIMIT %s'

    with connect(dbConnectionString) as dbConnection:
        with dbConnection.cursor() as dbCursor:
            dbCursor.execute(countTransactions)
            count = dbCursor.fetchone()
            print(f'{count[0]} transactions without tags')
            print()

            dbCursor.execute(selectTransactions, [args.limit])
            transactions = dbCursor.fetchall()
            for transaction in transactions:
                amount = '{0:.2f}'.format(transaction[3])
                print('{:<}   {:<}   {:<8}   {:<}'.format(str(transaction[0]), str(transaction[1]), amount, transaction[2]))
