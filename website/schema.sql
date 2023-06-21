SELECT * FROM users;
SELECT name 
FROM sqlite_master 
WHERE type = 'table';
SELECT * FROM sqlite_master WHERE type = 'table' AND name LIKE 'sqlite_%';
SELECT * FROM sqlite_sequence;

CREATE TABLE IF NOT EXISTS properties(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING(150) UNIQUE, size INTEGER);
INSERT INTO properties (name, size) VALUES ('Mahut', 2300);
INSERT INTO properties (name, size) VALUES ('Mjei', 3400);
SELECT * FROM properties;