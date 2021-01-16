create table transactions
(
    date        date  not null,
    amount      money not null,
    description text  not null,
    constraint transactions_pk
        primary key (date, amount, description)
);