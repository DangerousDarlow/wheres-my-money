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

create unique index transactions_uindex
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
	name text not null
);

create unique index tags_name_uindex
	on tags (name);



create table transactions_tags
(
	transaction_id uuid not null
		constraint transactions_tags_transactions_fk
			references transactions,
	tag_id uuid not null
		constraint transactions_tags_tags_fk
			references tags,
	constraint transactions_tags_pk
		primary key (transaction_id, tag_id)
);



create table tags_regex
(
	id uuid not null
		constraint tags_regex_pk
			primary key,
	tag_id uuid not null
		constraint tags_regex_tags_fk
			references tags,
	regex text not null
);



create unique index tags_regex_uindex
	on tags_regex (tag_id, regex);



create function readable(bigint) returns numeric
	language sql
as $$
SELECT CAST($1 AS numeric) / 1000000
$$;
