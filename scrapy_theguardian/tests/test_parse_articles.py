import unittest
from scrapy.http import HtmlResponse
from scrapy_theguardian.spiders.articles_spider import ArticlesSpider

class TestArticlesSpider(unittest.TestCase):

    def test_parse_page(self):
        articles_spider = ArticlesSpider()
        res = HtmlResponse(url='', encoding='utf-8', body='<html><body><a href="http://test1.com" data-link-name="article">Test1</a>\
        <a href="http://test2.com" data-link-name="ads">Test2 ads</a>\
        <a href="http://test3.com" data-link-name="article">Test3</a></body></html>')
        ret = [x for x in articles_spider.parse(res)]
        self.assertEqual(ret.__str__(), '[<GET http://test1.com>, <GET http://test3.com>]')

    def test_parse_article(self):
        articles_spider = ArticlesSpider()
        res = HtmlResponse(url='', encoding='utf-8', body='<html><body><h1 class="content__headline content__headline--no-margin-bottom" itemprop="headline">\
Title Parsed\
</h1></body></html>')
        ret = [x for x in articles_spider.parse_article_content(res)]
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0], {
            'headline': 'Title Parsed',
        })

if __name__ == '__main__':
    unittest.main()