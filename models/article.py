import sqlite3
from database.connection import get_db_connection


class Article:
    def __init__(self, title=None, content=None, author=None, magazine=None):
        # Initialize title, content, author, and magazine
        self._title = title
        self._content = content
        self._author_id = author.id if author else None
        self._magazine_id = magazine.id if magazine else None

        # Insert into the database if a new article is being created (no ID provided)
        if title and content and author and magazine:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            ''', (title, content, self._author_id, self._magazine_id))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError(
            "Title cannot be changed after the article is created")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        raise AttributeError(
            "Content cannot be changed after the article is created")

    @property
    def author(self):
        # Retrieve the author from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM authors WHERE id = ?
        ''', (self._author_id,))
        author_data = cursor.fetchone()
        conn.close()
        from models.author import Author
        return Author(author_data["id"], author_data["name"]) if author_data else None

    @property
    def magazine(self):
        # Retrieve the magazine from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM magazines WHERE id = ?
        ''', (self._magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()
        from models.magazine import Magazine
        return Magazine(magazine_data["id"], magazine_data["name"], magazine_data["category"]) if magazine_data else None
