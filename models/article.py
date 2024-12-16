import sqlite3
from database.connection import get_db_connection


class Article:
    def __init__(self, id=None, title=None, author=None, magazine=None):
        if id is None and title and author and magazine:
            self._create_article_in_db(title, author, magazine)
        else:
            self._id = id
            self._title = title
            self._author_id = author.id if hasattr(author, "id") else author
            self._magazine_id = magazine.id if hasattr(
                magazine, "id") else magazine

    def _create_article_in_db(self, title, author, magazine):
        """
        Creates a new article in the database and sets its ID.
        """
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError(
                "Title must be a string between 5 and 50 characters.")
        if not hasattr(author, "id") or not hasattr(magazine, "id"):
            raise ValueError(
                "Author and Magazine must be valid instances with IDs.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
        ''', (title, author.id, magazine.id))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()
        self._title = title
        self._author_id = author.id
        self._magazine_id = magazine.id

    def __str__(self):
        return f"Article(id={self.id}, title='{self.title}', author_id={self._author_id}, magazine_id={self._magazine_id})"

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError(
            "Title cannot be changed after the article is created.")

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?",
                       (self._author_id,))
        author_data = cursor.fetchone()
        conn.close()
        from models.author import Author
        return Author(author_data["id"], author_data["name"])

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?",
                       (self._magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()
        from models.magazine import Magazine
        return Magazine(magazine_data["id"], magazine_data["name"], magazine_data["category"])
