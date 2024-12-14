import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine


class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "Betty")
        self.assertEqual(author.name, "Betty")

    def test_article_creation(self):
        author = Author(1, "Betty")
        magazine = Magazine(1, "Vogue", "Technology")

        article = Article(title="Vogue", author=author, magazine=magazine)

        self.assertEqual(article.title, "Vogue")
        self.assertEqual(article.author.name, "Betty")
        self.assertEqual(article.magazine.name, "Vogue")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Vogue", "Technology")
        self.assertEqual(magazine.name, "Vogue")


if __name__ == "__main__":
    unittest.main()
