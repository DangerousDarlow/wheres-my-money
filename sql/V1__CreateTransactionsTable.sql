create table transactions
(
	id uuid not null
		constraint transactions_pk
			primary key,
	date date not null,
	amount bigint not null,
	description text not null
);

create unique index transactions_index
	on transactions (date, amount, description);