class Article:
    all_articles = []  # Class-level attribute to track all articles

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of the Author class.")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        self.author = author
        self.magazine = magazine
        self.title = title

        Article.all_articles.append(self)

    @staticmethod
    def get_all_articles():
        return Article.all_articles


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self.name = name

    def articles(self):
        return [article for article in Article.all_articles if article.author == self]

    def magazines(self):
        magazines = {article.magazine for article in self.articles()}
        return list(magazines) if magazines else None

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str):
            raise ValueError("Title must be a string.")
        return Article(self, magazine, title)

    def topic_areas(self):
        categories = {magazine.category for magazine in self.magazines()} if self.magazines() else None
        return list(categories) if categories else None


class Magazine:
    all_magazines = []  # Class-level attribute to track all magazine instances

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        
        self.name = name
        self.category = category
        Magazine.all_magazines.append(self)

    def articles(self):
        articles = [article for article in Article.all_articles if article.magazine == self]
        return articles if articles else None

    def contributors(self):
        authors = {article.author for article in self.articles()} if self.articles() else None
        return list(authors) if authors else None

    def article_titles(self):
        titles = [article.title for article in self.articles()] if self.articles() else None
        return titles

    def contributing_authors(self):
        authors = self.contributors()
        if not authors:
            return None
        frequent_authors = [author for author in authors if sum(1 for article in author.articles() if article.magazine == self) > 2]
        return frequent_authors if frequent_authors else None

    @classmethod
    def top_publisher(cls):
        if not Article.get_all_articles():
            return None
        magazine_article_counts = {magazine: len(magazine.articles()) for magazine in cls.all_magazines}
        return max(magazine_article_counts, key=magazine_article_counts.get, default=None)
