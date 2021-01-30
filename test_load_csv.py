from csv import reader as CsvReader
from datetime import datetime
from io import StringIO

from load_csv import buildFieldLookup, normaliseDescription, loadFile


def test_field_names_have_leading_and_trailing_whitespace_trimmed():
    reader = CsvReader(StringIO(' header1, header 2  ,header3 '))
    fields = buildFieldLookup(reader)
    assert len(fields) == 3
    assert fields['header1'] == 0
    assert fields['header 2'] == 1
    assert fields['header3'] == 2


def test_field_names_are_all_lower_case():
    reader = CsvReader(StringIO('hEaDer'))
    fields = buildFieldLookup(reader)
    assert len(fields) == 1
    assert fields['header'] == 0


def test_leading_blank_lines_are_ignored():
    reader = CsvReader(StringIO("""
    
    header"""))
    fields = buildFieldLookup(reader)
    assert len(fields) == 1
    assert fields['header'] == 0


def test_description_has_whitespace_trimmed():
    assert normaliseDescription(
        ' the years  to   come    seemed      waste of breath  ') == 'the years to come seemed waste of breath'


def test_description_is_all_lower_case():
    assert normaliseDescription(
        'A WASTE of breath the Years behind') == 'a waste of breath the years behind'


def test_load_multiple_transactions():
    reader = CsvReader(StringIO("""
    Date,Description,Amount
    01/02/2021,D1,-123.45
    02/02/2021,D2,-543.21
    """))

    added = datetime.utcnow()
    account = "test account"
    transactions = loadFile(reader, added, account)

    assert len(transactions) == 2

    assert transactions[0].timestamp == datetime.strptime('01/02/2021', '%d/%m/%Y').date()
    assert transactions[0].description == 'd1'
    assert transactions[0].amount == -123450000
    assert transactions[0].added == added
    assert transactions[0].account == account

    assert transactions[1].timestamp == datetime.strptime('02/02/2021', '%d/%m/%Y').date()
    assert transactions[1].description == 'd2'
    assert transactions[1].amount == -543210000
    assert transactions[1].added == added
    assert transactions[1].account == account


def test_transaction_field_order_defined_in_first_row():
    reader = CsvReader(StringIO("""
    Ignore,Amount,Date,AlsoIgnore,Description
    red,-123.45,01/02/2021,blue,D1
    """))

    added = datetime.utcnow()
    account = "test account"
    transactions = loadFile(reader, added, account)

    assert len(transactions) == 1

    assert transactions[0].timestamp == datetime.strptime('01/02/2021', '%d/%m/%Y').date()
    assert transactions[0].description == 'd1'
    assert transactions[0].amount == -123450000
    assert transactions[0].added == added
    assert transactions[0].account == account