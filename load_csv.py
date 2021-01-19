from argparse import ArgumentParser
from csv import reader as CsvReader
from datetime import date, datetime
from dbConfig import dbConnectionString
from os import path, walk
from psycopg2 import connect
from re import sub
from transaction import AmountScalingFactor, Transaction
from uuid import uuid4


def readNotEmpty(reader):
    while reader:
        row = next(reader, None)
        if row and row[0].strip():
            return row


def buildFieldLookup(reader):
    headerRow = readNotEmpty(reader)
    headers = {}
    for i in range(len(headerRow)):
        headers[headerRow[i].lower().strip()] = i

    return headers


def normaliseDescription(raw):
    return sub(r'\s+', ' ', raw.strip().lower())


def loadFile(path):
    print(f"Reading CSV file '{path}'")

    transactions = []
    with open(path, encoding='utf8') as csvFile:
        reader = CsvReader(csvFile)
        field = buildFieldLookup(reader)
        for row in reader:
            if len(row) < 3:
                continue

            date = datetime.strptime(row[field['date']], '%d/%m/%Y').date()
            amount = int(float(row[field['amount']]) * AmountScalingFactor)
            description = normaliseDescription(row[field['description']])
            transactions.append(Transaction(
                id=uuid4(), date=date, amount=amount, description=description))

    print(f"Found {len(transactions)} transactions")
    return transactions


if __name__ == "__main__":
    parser = ArgumentParser(description='Load data from one or more CSV files')
    parser.add_argument('directory', type=str, help='Data file directory')
    args = parser.parse_args()

    transactions = []
    for root, dirPaths, filePaths in walk(args.directory):
        for filePath in filePaths:
            (_, extension) = path.splitext(filePath)
            if extension != '.csv':
                continue

            transactions += loadFile(path.abspath(path.join(root, filePath)))

    insertSql = 'INSERT INTO transactions (id,date,amount,description) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING'

    with connect(dbConnectionString) as dbConnection:
        dbConnection.autocommit = False
        with dbConnection.cursor() as dbCursor:
            for transaction in transactions:
                dbCursor.execute(insertSql, (transaction.id, transaction.date,
                                             transaction.amount, transaction.description))

            dbConnection.commit()
