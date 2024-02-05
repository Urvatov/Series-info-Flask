import sqlite3
from flask import request, flash


class Data:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        
    def add(self, title, seasons, finished, release):
        try:
            self.__cur.execute("INSERT INTO series VALUES(NULL, ?, ?, ?, ?)", (title, seasons, finished, release))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления сериала" + str(e))
            return False
        return True
    
    def get_series(self, id):
        try:
            self.__cur.execute(f"SELECT title, seasons, finished, release FROM series WHERE id = {id} LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения сериала " + str(e))
        
        return(False, False)
    
    def get_series_id(self, id):
        try:
            self.__cur.execute(f"SELECT id FROM series WHERE id = {id} LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения id сериала " + str(e))

    def get_posts(self):
        try:
            self.__cur.execute("SELECT id, title FROM series ORDER BY title")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения поста" + str(e))
        
        return []
    
    def add_user(self, nickname, hash):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM user WHERE nickname LIKE '{nickname}' ")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("ПОЛЬЗОВАТЕЛЬ С ТАКИМ ИМЕНЕМ УЖЕ СУЩЕСТВУЕТ")

            self.__cur.execute("INSERT INTO user VALUES(NULL, ?, ?)", (nickname, hash))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления юзера" + str(e))
            return False
        return True
    
    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН")
                return False
            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения юзера" + str(e))

        return False
    
    def get_user_by_nickname(self, nickname):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE nickname = '{nickname}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("ПОльзователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения юзера" + str(e))

        return False
    
    def add_genre(self, name):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM genre WHERE title LIKE '{name}' ")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                flash("ЖАНР С ТАКИМ ИМЕНЕМ УЖЕ СУЩЕСТВУЕТ")
            
            else:
                self.__cur.execute("INSERT INTO genre VALUES(NULL, ?)", (name,))
                self.__db.commit()
                flash("Жанр успешно добавлен")

        except sqlite3.Error as e:
            print("Ошибка добавления жанра " + str(e))
        
    def add_genre_to_series(self, id_series, genre):
        try:
            genre_title = genre
            self.__cur.execute(f"SELECT id FROM genre WHERE title = '{genre}' ")
            genre_id = self.__cur.fetchone()
            self.__cur.execute("INSERT INTO series_genre VALUES(?, ?, ?)", (id_series, genre_id[0], genre_title))
            self.__db.commit()
            flash("Жанр успешно добавлен")

        except sqlite3.Error as e:
            print("Ошибка добавления жанра " + str(e))

    def get_genre_from_series(self, series_id):
        try:
            self.__cur.execute(f"SELECT genre_title FROM series_genre WHERE id_series = {series_id}")
            s_genres = self.__cur.fetchall()

            return s_genres
        except sqlite3.Error as e:
            print("Ошибка получения жанра " + str(e))

    def add_human(self, fullname, birthday, job):
        if job == "Актер":
            try:
                self.__cur.execute("INSERT INTO actor VALUES(NULL, ?, ?)", (fullname, birthday))
                self.__db.commit()
                flash("Актер успешно добавлен")

            except sqlite3.Error as e:
                print("Ошибка добавления актера " + str(e))
        
        if job == "Режиссер":
            try:
                self.__cur.execute("INSERT INTO director VALUES(NULL, ?, ?)", (fullname, birthday))
                self.__db.commit()
                flash("Режиссер успешно добавлен")

            except sqlite3.Error as e:
                print("Ошибка добавления режиссера " + str(e))
        
        if job == "Сценарист":
            try:
                self.__cur.execute("INSERT INTO writer VALUES(NULL, ?, ?)", (fullname, birthday))
                self.__db.commit()
                flash("Сценарист успешно добавлен")

            except sqlite3.Error as e:
                print("Ошибка добавления сценариста " + str(e))
    
    def get_genres(self):
        try:
            self.__cur.execute("SELECT title FROM genre ORDER BY title DESC")
            genres = self.__cur.fetchall()
            if genres: 
                return genres

        except sqlite3.Error as e:
            print("Ошибка получения Жанра " + str(e))

    def get_actors(self):
        try:
            self.__cur.execute("SELECT fullname FROM actor ORDER BY fullname DESC")
            actors = self.__cur.fetchall()
            if actors: 
                return actors

        except sqlite3.Error as e:
            print("Ошибка получения актера " + str(e))

    def get_directors(self):
            try:
                self.__cur.execute("SELECT fullname FROM director ORDER BY fullname DESC")
                directors = self.__cur.fetchall()
               
                return directors

            except sqlite3.Error as e:
                print("Ошибка получения режиссера " + str(e))
    
    def get_writers(self):
        try:
            self.__cur.execute("SELECT fullname FROM writer ORDER BY fullname DESC")
            writers = self.__cur.fetchall()
            if writers: 
                return writers

        except sqlite3.Error as e:
            print("Ошибка получения сценариста " + str(e))

    def add_actor_to_series(self, id_series, actor):
        try:
            actor_name = actor
            self.__cur.execute(f"SELECT id FROM actor WHERE fullname = '{actor}' ")
            actor_id = self.__cur.fetchone()
            self.__cur.execute("INSERT INTO series_actor VALUES(?, ?, ?)", (id_series, actor_id[0], actor_name))
            self.__db.commit()
            flash("Актер успешно добавлен")

        except sqlite3.Error as e:
            print("Ошибка добавления Актер " + str(e))

    def get_actors_from_series(self, series_id):
        try:
            self.__cur.execute(f"SELECT actor_name FROM series_actor WHERE id_series = {series_id}")
            actors = self.__cur.fetchall()
            if actors: 
                return actors
            
        except sqlite3.Error as e:
            print("Ошибка получения актера " + str(e))
    
    def add_director_to_series(self, id_series, director):
        try:
            director_name = director
            self.__cur.execute(f"SELECT id FROM director WHERE fullname = '{director}'")
            director_id = self.__cur.fetchone()
            self.__cur.execute("INSERT INTO series_director VALUES(?, ?, ?)", (id_series, director_id[0], director_name))
            self.__db.commit()
            flash("Режиссер успешно добавлен")

        except sqlite3.Error as e:
            print("Ошибка добавления Режиссера " + str(e))

    def add_writer_to_series(self, id_series, writer):
        try:
            writer_name = writer
            self.__cur.execute(f"SELECT id FROM writer WHERE fullname = '{writer}'")
            writer_id = self.__cur.fetchone()
            self.__cur.execute("INSERT INTO series_writer VALUES(?, ?, ?)", (id_series, writer_id[0], writer_name))
            self.__db.commit()
            flash("Сценарист успешно добавлен")

        except sqlite3.Error as e:
            print("Ошибка добавления Сценариста " + str(e))

    def get_directors_from_series(self, series_id):
        try:
            self.__cur.execute(f"SELECT director_name FROM series_director WHERE id_series = {series_id}")
            directors = self.__cur.fetchall()
            if directors:
                return directors

        except sqlite3.Error as e:
            print("Ошибка получения режиссера " + str(e))

    def get_writers_from_series(self, series_id):
        try:
            self.__cur.execute(f"SELECT writer_name FROM series_writer WHERE id_series = {series_id}")
            writers = self.__cur.fetchall()
            if writers:
                return writers

        except sqlite3.Error as e:
            print("Ошибка получения сценариста " + str(e))
        
    
    def add_rating(self, user, sereies_id, rating):
        try:
            self.__cur.execute("INSERT INTO series_rating VALUES(?, ?, ?)", (sereies_id, user, rating))
            self.__db.commit()
            flash("Вы оставили оценку")

        except sqlite3.Error as e:
            print("Ошибка добавления рейтинга " + str(e))
            if str(e) == "UNIQUE constraint failed: series_rating.id_user, series_rating.id_series":
                flash("Вы уже оставили оценку.")

    def get_rating(self, series_id):
        try:
            self.__cur.execute(f"SELECT AVG(rating) FROM series_rating WHERE id_series = {series_id}")
            rating = self.__cur.fetchone()
            if rating: 
                return rating[0]

        except sqlite3.Error as e:
            print("Ошибка получения сценариста " + str(e))
    
    def add_season(self, title, series_id, order_number, episodes_number):
        try:
            self.__cur.execute(f"INSERT INTO season VALUES (?, ?, ?, ?)", (title, series_id, order_number, episodes_number))
            self.__db.commit()    

        except sqlite3.Error as e:
            print("Ошибка добавления сезона " + str(e))

    def get_season(self, series_id):
        try:
            self.__cur.execute(f"SELECT title, order_number, episodes_number FROM season WHERE id_series = {series_id} ORDER BY order_number ")
            series_seasons = self.__cur.fetchall()
            if series_seasons: 
                return series_seasons

        except sqlite3.Error as e:
            print("Ошибка получения сезона " + str(e))

