create table transactions
(
	id uuid not null
		constraint transactions_pk
			primary key,
	timestamp date not null,
	amount bigint not null,
	description text not null,
	added timestamp with time zone not null,
	account text not null
);

create unique index transactions_unique_index
	on transactions (timestamp, amount, description);

create index transactions_amount_index
	on transactions (amount);

create index transactions_description_index
	on transactions (description);

create index transactions_timestamp_index
	on transactions (timestamp);



create table tags
(
	id uuid not null
		constraint tags_pk
			primary key,
	name text not null,
	regex text not null
);



create table transactions_tags
(
	transaction_id uuid not null,
	tag_id uuid not null,
	constraint transactions_tags_pk
		primary key (transaction_id, tag_id)
);
