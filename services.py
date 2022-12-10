import psycopg2
from psycopg2.extensions import (cursor as Cursor, connection as Connection, ISOLATION_LEVEL_AUTOCOMMIT)
from psycopg2 import Error
from typing import Any

from config import (USER, PASSWORD, HOST, PORT)


class Connecting():
    def __init__(self) -> None:
        try:
            self.connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = self.connection.cursor()
            print('Connection success!')
            cursor.execute('CREATE DATABASE homework6;')
            print('Database Created!')
        except (Exception, Error) as e:
            print(f'Error {e}')

    def __new__(cls: type[Any]):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connecting, cls).__new__(cls)

        return cls.instance

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database='homework6',
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('Connection to database success')
        except (Exception, Error) as e:
            print(f'Error {e}')

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(30) UNIQUE NOT NULL,
                    description TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS genres(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(30) UNIQUE NOT NULL,
                    description TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS result(
                    id SERIAL PRIMARY KEY,
                    game_id INTEGER REFERENCES games(id),
                    genre_id INTEGER REFERENCES genres(id)
                );
            """)
        self.connection.commit()
        print('Tables successfuly created!')

    def set_genres(self, title, description):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO genres(title, description)
                VALUES ('{title}','{description}');
            """)
        self.connection.commit()
        print('Row has added to genre')

    def get_genres(self):
        data: list[tuple] = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM genres;')
            data = cursor.fetchall()
        self.connection.commit()
        return data

    def set_game(self, title, description):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO games(title, description)
                VALUES ('{title}', '{description}');
            """)
        self.connection.commit()
        print('Game added!')

    def get_games(self):
        data: list[tuple] = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM games;')
            data = cursor.fetchall()
        self.connection.commit()
        return data

    def res(self, game_id, genre_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO result(game_id, genre_id)
                VALUES ({game_id}, {genre_id});
            """)
        self.connection.commit()
        print('ADDED!')