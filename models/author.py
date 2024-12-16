import sqlite3
from database.connection import get_db_connection


class Author:
    def __init__(self, id=None, name=None):
        if id is None and name:
            self._create_author_in_db(name)
        else:
            self._id = id
            self._name = name

    def _create_author_in_db(self, name):
        """
        Creates a new author in the database and sets its ID.
        """
        if not isinstance(name, str) or len(name) <= 0:
            raise ValueError("Name must be a non-empty string.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()
        self._name = name

    def __str__(self):
        return f"Author(id={self.id}, name='{self.name}')"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name cannot be changed once set.")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        from models.article import Article
        return [Article(article["id"], article["title"], article["author_id"], article["magazine_id"]) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        from models.magazine import Magazine
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines]
