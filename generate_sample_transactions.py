from argparse import ArgumentParser
from datetime import date, timedelta
from random import choice, randrange

def random_date(earliest, latest):
    difference = latest - earliest
    offset = randrange(difference.days)
    return earliest + timedelta(days=offset)


if __name__ == "__main__":
    parser = ArgumentParser(description='Generate random transaction data')
    parser.add_argument('count', type=int, help='Number of transactions to generate')
    args = parser.parse_args()

    descriptions = [
        'Amazon',
        'Tesco',
        'Tesco Petrol Station'
    ]

    for index in range(args.count):
        date = random_date(date.fromisoformat('2021-01-01'), date.fromisoformat('2022-01-01'))
        description = choice(descriptions)
        amount = randrange(-100, 20)
        print(f'{date.strftime("%d/%m/%y")},{description},{amount}')