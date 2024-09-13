DROP TABLE IF EXISTS demo;

CREATE TABLE IF NOT EXISTS buyer (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                  name VARCHAR(30) NOT NULL,
                                  balance DECIMAL NOT NULL,
                                  age TINYINT NOT NULL);

CREATE TABLE IF NOT EXISTS game (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                 title VARCHAR(100) NOT NULL,
                                 cost DECIMAL NOT NULL, size DECIMAL NOT NULL,
                                 description TEXT NOT NULL,
                                 age_limited BOOL NOT NULL);

INSERT INTO buyer (name, balance, age)
	VALUES ('Alex', 100, 27),
           ('Pasha', 1000, 39);

INSERT INTO game (title, cost, size, description, age_limited)
	VALUES ('Tetris', 5.99, 3.45, 'Легендарная игра', 0),
           ('World of Tanks', 49.99, 343.34, 'Танчикм', 1);

SELECT * FROM buyer;
SELECT * FROM game;
SELECT * FROM sqlite_sequence;