import sqlite3
from database.connection import get_db_connection


class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None and name and category:
            self._create_magazine_in_db(name, category)
        else:
            self._id = id
            self._name = name
            self._category = category

    def _create_magazine_in_db(self, name, category):
        """
        Creates a new magazine in the database and sets its ID.
        """
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError(
                "Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) <= 0:
            raise ValueError("Category must be a non-empty string.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()
        self._name = name
        self._category = category

    def __str__(self):
        return f"Magazine(id={self.id}, name='{self.name}', category='{self.category}')"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError(
                "Name must be a string between 2 and 16 characters.")
        self._name = value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE magazines SET name = ? WHERE id = ?", (self._name, self.id))
        conn.commit()
        conn.close()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE magazines SET category = ? WHERE id = ?", (self._category, self.id))
        conn.commit()
        conn.close()
