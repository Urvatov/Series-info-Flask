
CREATE TABLE IF NOT EXISTS user
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL,
    psw TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS series
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    seasons INTEGER NOT NULL,
    finished BOOLEAN NOT NULL,
    release DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS genre
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actor
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    birthday DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS director
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    birthday DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS writer
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    birthday DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS series_rating
(
    id_series INTEGER,
    id_user INTEGER,
    rating INTEGER,
    PRIMARY KEY(id_user, id_series),
    FOREIGN KEY(id_series) REFERENCES series(id) ON UPDATE CASCADE,
    FOREIGN KEY(id_user) REFERENCES user(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS series_genre
(
    id_series INTEGER,
    id_genre INTEGER,
    genre_title TEXT,

    PRIMARY KEY(id_genre, id_series),
    FOREIGN KEY(id_series) REFERENCES series(id) ON UPDATE CASCADE,
    FOREIGN KEY(id_genre) REFERENCES genre(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS series_actor
(
    id_series INTEGER,
    id_actor INTEGER,
    actor_name TEXT,

    PRIMARY KEY(id_actor, id_series),
    FOREIGN KEY(id_series) REFERENCES series(id) ON UPDATE CASCADE,
    FOREIGN KEY(id_actor) REFERENCES actor(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS series_director
(
    id_series INTEGER,
    id_director INTEGER,
    director_name TEXT,

    PRIMARY KEY(id_director, id_series),
    FOREIGN KEY(id_series) REFERENCES series(id) ON UPDATE CASCADE,
    FOREIGN KEY(id_director) REFERENCES director(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS series_writer
(
    id_series INTEGER,
    id_writer INTEGER,
    writer_name TEXT,

    PRIMARY KEY(id_writer, id_series),
    FOREIGN KEY(id_series) REFERENCES series(id) ON UPDATE CASCADE,
    FOREIGN KEY(id_writer) REFERENCES writer(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS season
(   
    title TEXT,
	id_series INT,
	order_number INT,
	episodes_number INT,
	PRIMARY KEY (order_number, id_series),
	FOREIGN KEY (id_series) REFERENCES series(id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS episode
(
    id_series VARCHAR(20),
    season_order_number INT,
    order_number INT,
    PRIMARY KEY(order_number, season_order_number, id_series),
    FOREIGN KEY (season_order_number, id_series) REFERENCES season(order_number, id_series)
);

