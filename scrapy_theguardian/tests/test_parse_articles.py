import unittest
from scrapy_theguardian.spiders.articles_spider import ArticlesSpider

class TestArticlesSpider(unittest.TestCase):

    def test_pares_page(self):
        articles_spider = ArticlesSpider()
        self.assertEqual(articles_spider.parse(None), None)

if __name__ == '__main__':
    unittest.main()