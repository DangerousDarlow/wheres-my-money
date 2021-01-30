from argparse import ArgumentParser
from csv import reader as CsvReader
from datetime import date, datetime
from dbConfig import dbConnectionString
from os import walk
from psycopg2 import connect
from re import sub
from transaction import AmountScalingFactor, Transaction
from uuid import uuid4
import ntpath


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


def loadFile(reader, added, account):
    transactions = []
    
    fieldIndexes = buildFieldLookup(reader)
    for row in reader:
        if len(row) < 3:
            continue

        amount = int(float(row[fieldIndexes['amount']]) * AmountScalingFactor)
        if amount == 0:
            continue

        timestamp = datetime.strptime(row[fieldIndexes['date']].strip(), '%d/%m/%Y').date()
        description = normaliseDescription(row[fieldIndexes['description']])
        transactions.append(Transaction(
            id=uuid4(),
            timestamp=timestamp,
            amount=amount,
            description=description,
            added=added,
            account=account))

    return transactions


if __name__ == "__main__":
    parser = ArgumentParser(description='Load data from one or more CSV files')
    parser.add_argument('directory', type=str, help='Data file directory')
    args = parser.parse_args()

    added = datetime.now()

    transactions = []
    for root, dirPaths, filePaths in walk(args.directory):
        for filePath in filePaths:
            (filePathWithoutExtension, fileExtension) = ntpath.splitext(filePath)
            if fileExtension != '.csv':
                continue

            print(f"Reading CSV file '{filePath}'")
            with open(ntpath.abspath(ntpath.join(root, filePath)), encoding='utf8') as csvFile:
                reader = CsvReader(csvFile)
                account = ntpath.basename(filePathWithoutExtension)
                transactions += loadFile(reader, added, account)

    print(f"Found {len(transactions)} transactions")

    insertSql = 'INSERT INTO transactions (id,timestamp,amount,description,added,account) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'

    with connect(dbConnectionString) as dbConnection:
        dbConnection.autocommit = False
        with dbConnection.cursor() as dbCursor:
            for transaction in transactions:
                dbCursor.execute(insertSql, (transaction.id, transaction.timestamp,
                                             transaction.amount, transaction.description,
                                             transaction.added, transaction.account))

            dbConnection.commit()
