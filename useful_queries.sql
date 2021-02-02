SELECT id, timestamp, readable(amount), description, account FROM transactions ORDER BY timestamp DESC;

DELETE FROM tags_regex;
DELETE FROM tags;
DELETE FROM transactions_tags;
DELETE FROM transactions;
