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


INSERT INTO task1_game (title, cost, size, description, age_limited) VALUES
('Red Dead Redemption 2', '69.99.29', '100', 'Открытый мир в сеттинге Дикого Запада XIX века.', false),
('Cyberpunk 2077', '59.99', '60', 'Ролевая игра в стиле киберпанк, действие которой происходит в мрачном будущем.', false),
('Resident Evil Village', '39.99', '30', 'Хоррор от третьего лица, продолжающий историю серии Resident Evil.', true),
('Halo Infinite', '47.99', '100', 'Шутер от первого лица, являющийся продолжением популярной серии Halo.', false),
('God of War', '12.99', '60.654', 'Эпическое приключение Кратоса и его сына Атрея в мире скандинавской мифологии.', false),
('Metroid Dread', '24.99', '30', 'Метроидвания с элементами стелса, в которой игрок исследует таинственную планету ZDR.', true),
('Horizon Zero Dawn', '69.99', '100', 'Приключенческий боевик с открытым миром, где игроки сражаются с механическими животными.', false),
('Final Fantasy VII Remake', '59.99', '60', 'Ремейк культовой японской ролевой игры с улучшенной графикой и новым сюжетом.', false),
('Battlefield V', '39.99', '30', 'Шутер от первого лица, посвященный Второй мировой войне.', true),
('Star Wars Jedi: Fallen Order', '69.99', '100.834', 'Действие игры разворачивается после событий фильма "Звездные войны: Эпизод III".', false),
('Far Cry 6', '59.99', '60.543', 'Сетевой шутер с открытым миром, действия которого происходят на тропическом острове Яра.', false),
('Marvels Spider-Man', '859.99', '30', 'Игра про Человека-паука, в которой игрокам предстоит бороться с преступностью в Нью-Йорке.', true),
('Minecraft', '69.99', '100', 'Кубическая песочница, позволяющая игрокам строить и исследовать различные миры.', false),
('Forza Horizon 5', '42.99', '60', 'Автосимулятор с открытым миром, события которого разворачиваются в Мексике.', false),
('The Legend of Zelda: Breath of the Wild', '36.99', '30', 'Приключенческий экшен с открытым миром, действия которого происходят в королевстве Хайрул.', true),
('Ratchet & Clank: Rift Apart', '69.99', '100', 'Платформер с открытым миром, в котором герои путешествуют через межпространственные разломы.', false),
('Super Mario Odyssey', '59.99', '60', 'Платформер, в котором Марио отправляется в путешествие по различным мирам.', false),
('Doom Eternal', '53.99', '30', 'Шутер от первого лица, являющийся продолжением игры Doom 2016 года.', true),
('Deathloop', '69.99', '100', 'Шутер от первого лица с элементами временной петли.', false),
('Outriders', '59.99', '60', 'Кооперативный шутер с элементами ролевой игры, действие которого происходит в постапокалиптическом мире.', false),
('Ghost of Tsushima', '23.99', '30', 'Приключенческий экшен, события которого разворачиваются на острове Цусима в Японии.', true),
('Uncharted 4: A Thiefs End', '69.99', '100', 'Приключенческий экшен, завершающий серию Uncharted о поиске сокровищ.', false),
('Grand Theft Auto V', '38.99', '60', 'Экшен с открытым миром, действия которого разворачиваются в вымышленном городе Лос-Сантос.', false),
('Call of Duty: Black Ops Cold War', '39.99', '30', 'Шутер от первого лица, события которого разворачиваются во время холодной войны.', true),
('Fallout 4', '75.99', '100', 'Ролевая игра с открытым миром, действие которой происходит в постапокалиптической Америке.', false),
('Dragon Age: Inquisition', '59.99', '60.642', 'Ролевая игра, в которой игроки берут на себя роль инквизитора, борющегося с демонами.', false),
('Devil May Cry 5', '37.99', '30', 'Характерный экшен, в котором игроки играют за Данте, сражающегося с демонами.', true),
('Sea of Thieves', '99.99', '100', 'Многопользовательская игра, в которой игроки управляют пиратскими кораблями.', false),
('Pokémon Sword and Shield', '59.99', '60', 'Ролевая игра, в которой игроки путешествуют по миру Галар, собирая покемонов.', false),
('NieR: Automata', '29.99', '30', 'Постапокалиптический экшен, в котором игроки сражаются против роботов.', true),
('Elden Ring', '69.99', '100', 'Ролевая игра с открытым миром, действие которой разворачивается в фантастическом мире.', false),
('Gears 5', '54.99', '60', 'Шутер от третьего лица, пятая часть серии Gears of War.', false);
