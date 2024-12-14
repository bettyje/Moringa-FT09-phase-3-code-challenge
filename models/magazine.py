import sqlite3
from database.connection import get_db_connection


class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category

        if id is None and name is not None and category is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
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
        self._name = value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE magazines SET name = ? WHERE id = ?', (self._name, self.id))
        conn.commit()
        conn.close()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE magazines SET category = ? WHERE id = ?', (self._category, self.id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        from models.article import Article
        return [Article(article["id"], article["title"], article["author_id"], article["magazine_id"]) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        from models.author import Author
        return [Author(author["id"], author["name"]) for author in authors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [article["title"] for article in articles] if articles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        from models.author import Author
        return [Author(author["id"], author["name"]) for author in authors] if authors else None
