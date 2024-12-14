import sqlite3
from database.connection import get_db_connection


class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = name

        if id is None and name is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name cannot be changed once set")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE author_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        from models.article import Article
        return [Article(article["id"], article["title"], article["author_id"], article["magazine_id"]) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        from models.magazine import Magazine
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines]
