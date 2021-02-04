SELECT id, timestamp, readable(amount), description, account
FROM transactions
ORDER BY timestamp DESC;


SELECT t.id, timestamp, readable(amount), description, account, tg.name
FROM transactions t
JOIN transactions_tags tt on t.id = tt.transaction_id
JOIN tags tg on tt.tag_id = tg.id
ORDER BY t.timestamp DESC;


DELETE FROM tag_filters;
DELETE FROM tags;
DELETE FROM transactions_tags;
DELETE FROM transactions;
