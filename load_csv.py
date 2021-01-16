from argparse import ArgumentParser
from csv import reader as CsvReader
from os import path as Path, walk as Walk



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



def loadFile(path):
    print(f"Opening CSV file '{path}'")
    with open(path, encoding='utf8') as csvFile:
        reader = CsvReader(csvFile)
        field = buildFieldLookup(reader)
        for row in reader:
            print(row[field['date']])



if __name__ == "__main__":
    parser = ArgumentParser(description='Load data from one or more CSV files')
    parser.add_argument('directory', type=str, help='Data file directory')
    args = parser.parse_args()

    for root, dirPaths, filePaths in Walk(args.directory):
        for filePath in filePaths:
            loadFile(Path.abspath(Path.join(root, filePath)))
