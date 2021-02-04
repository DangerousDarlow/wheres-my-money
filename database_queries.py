from dbConfig import dbConnectionString
from psycopg2 import connect
from transaction import Transaction
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


def add_filter_for_tag(dbConnection, tagId, regex, condition):
    insertSql = 'INSERT INTO tag_filters(id, tag_id, regex, condition) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING'
    with dbConnection.cursor() as dbCursor:
        dbCursor.execute(insertSql, [uuid4(), tagId, regex, condition])


def get_tag_filters(dbConnection):
    selectSql = 'SELECT tag_id, regex, condition FROM tag_filters'
    with dbConnection.cursor() as dbCursor:
        dbCursor.execute(selectSql)
        return dbCursor.fetchall()


def get_transactions_unordered(dbConnection):
    selectSql = 'SELECT id, timestamp, amount, description, added, account FROM transactions'
    with dbConnection.cursor() as dbCursor:
        dbCursor.execute(selectSql)
        return [Transaction(row[0], row[1], row[2], row[3], row[4], row[5]) for row in dbCursor.fetchall()]


def get_untagged_transactions(dbConnection, limit):
    countSql = 'SELECT COUNT(id) FROM transactions t FULL JOIN transactions_tags tt ON t.id = tt.transaction_id WHERE tt.transaction_id IS NULL'
    selectSql = 'SELECT id, timestamp, amount, description, added, account FROM transactions t FULL JOIN transactions_tags tt ON t.id = tt.transaction_id WHERE tt.transaction_id IS NULL ORDER BY t.timestamp DESC LIMIT %s'

    with dbConnection.cursor() as dbCursor:
        dbCursor.execute(countSql)
        count = dbCursor.fetchone()[0]

        dbCursor.execute(selectSql, [limit])
        transactions = [Transaction(row[0], row[1], row[2], row[3], row[4], row[5]) for row in dbCursor.fetchall()]
        return (count, transactions)