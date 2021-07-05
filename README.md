# Where's My Money

Where's My Money is a personal financial analysis tool. It allows transactions to be imported from statements, grouped and analysed.

## Quick Start

Performing these steps will give an overview of how the tool works

1. Create and initialise database
1. Import transaction data
1. Show untagged transactions
1. Create a tag
1. Tag transactions

### Create and initialise database

Where's My Money uses a PostgreSQL database to store application data. Use docker-compose to

1. Start PostgreSQL
1. Create and initialise the database using flyway

```
docker-compose up
```

### Import transaction data

Import data from CSV files in a directory using script `load_transactions_from_csv`. Two sample data sets have been provided

1. demo
1. small

Load the small data set using

```
python .\load_transactions_from_csv.py .\data\small\
```

_The demo data contains 834 transactions but there are 847 lines in the file. This is because transactions with zero amount are not imported._

### Show untagged transactions

Transactions can be tagged zero or more times. You might use tag `food` for food purchases. To list transactions that have not been tagged run script `list_untagged_transactions`. All transactions imported from the small data set will be untagged.

```
python .\list_untagged_transactions.py
```
```
11 transactions without tags

f755bb18-e769-4960-bb7f-6d34c0f6796b   2021-01-29    5000.00   wages
63301a8f-3661-419a-a88d-adb10a4b7bbf   2021-01-22     -43.00   amazon
fcdae36c-1422-4878-bf2a-6578a895321d   2021-01-22     -56.00   shell
c1e8d1e1-faf0-4a90-8e61-76b0e15d8f54   2021-01-21      -3.00   tesco petrol station
f7674586-11b4-4ac3-9d3e-ee9a5b56e179   2021-01-19     -34.00   tesco petrol station
0b1df334-817c-45bc-a47f-9e4c38d1c948   2021-01-12     -78.00   tesco
ca16a117-3a56-46f2-b0ec-5bd9665a83f1   2021-01-12     -61.00   tesco
b65b0dd9-b070-4bfb-b00e-e37fd6b650de   2021-01-04    -120.00   council tax
d7dd6392-241c-4736-8136-4ae00e38470e   2021-01-04     -40.00   energy supplier
5f8db806-d05c-46ce-b634-a83a3ec3bb5d   2021-01-03     -31.00   amazon
```

### Create a tag

Tags are used to group transactions. Create a tag named `tesco` matching description regex `tesco`. The tag uuid is returned.

```
python .\create_tag.py tesco --regex tesco
```

### Tag transactions

Iterate through all transactions and assign tags where tag criteria matches.

```
python .\tag_transactions.py
```

If you list untagged transactions after this operation 7 are now untagged.

## Running Tests

Run the tests with command

```
python -m pytest
```