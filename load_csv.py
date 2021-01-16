from argparse import ArgumentParser
from csv import reader as CsvReader
from datetime import date, datetime
from os import path, walk
from re import sub



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
    print(f"Opening CSV file '{path}'")
    with open(path, encoding='utf8') as csvFile:
        reader = CsvReader(csvFile)
        field = buildFieldLookup(reader)
        for row in reader:
            date = datetime.strptime(row[field['date']], '%d/%m/%Y').date()
            description = normaliseDescription(row[field['description']])
            print(date, description)



if __name__ == "__main__":
    parser = ArgumentParser(description='Load data from one or more CSV files')
    parser.add_argument('directory', type=str, help='Data file directory')
    args = parser.parse_args()

    for root, dirPaths, filePaths in walk(args.directory):
        for filePath in filePaths:
            loadFile(path.abspath(path.join(root, filePath)))
