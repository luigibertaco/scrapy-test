import unittest
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from scrapy_theguardian.spiders.articles_spider import ArticlesSpider

class TestArticlesSpider(unittest.TestCase):

    def test_parse_page(self):
        articles_spider = ArticlesSpider()
        res = HtmlResponse(url='', encoding='utf-8', body='<html><body><a href="http://test1.com" data-link-name="article">Test1</a>\
        <a href="http://test2.com" data-link-name="ads">Test2 ads</a>\
        <a href="http://test3.com" data-link-name="article">Test3</a>\
        <a data-page="2" rel="next" href="https://test.com/?page=2" data-link-name="Pagination view next"></a></body></html>')
        ret = [x for x in articles_spider.parse(res)]
        self.assertEqual(ret.__str__(), '[<GET http://test1.com>, <GET http://test3.com>, <GET https://test.com/?page=2>]')
    
    def test_parse_last_page(self):
        articles_spider = ArticlesSpider()
        res = HtmlResponse(url='', encoding='utf-8', body='<html><body><a href="http://test1.com" data-link-name="article">Test1</a>\
        <a href="http://test2.com" data-link-name="ads">Test2 ads</a>\
        <a href="http://test3.com" data-link-name="article">Test3</a>\
        <a data-page="6" rel="next" href="https://test.com/?page=2" data-link-name="Pagination view next"></a></body></html>')
        ret = [x for x in articles_spider.parse(res)]
        self.assertEqual(ret.__str__(), '[<GET http://test1.com>, <GET http://test3.com>]')

    def test_parse_article(self):
        articles_spider = ArticlesSpider()
        url = 'http://testurl.com'
        res = HtmlResponse(url=url, encoding='utf-8', body='<html><body><header><meta name="keywords" content="a,b,c"></header>\
            <h1 class="content__headline content__headline--no-margin-bottom" itemprop="headline">\
            Title Parsed\
            </h1><span itemprop="author"> \
            <a><span itemprop="name">Author Name</span></a></span>\
            <meta itemprop="description" content="description details">\
            <div itemprop="articleBody"><p>body 1</p><p>body 2</p></div></body></html>')
        ret = [x for x in articles_spider.parse_article_content(res)]
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0], {
            'headline': 'Title Parsed',
            'description': 'description details',
            'body': 'body 1\nbody 2',
            'url': url,
            'author': 'Author Name',
            'keywords': ['a','b','c']
        })

    def test_parse_article_no_description(self):
        articles_spider = ArticlesSpider()
        url = 'http://testurl.com'
        res = HtmlResponse(url=url, encoding='utf-8', body='<html><body>\
            <h1 class="content__headline content__headline--no-margin-bottom" itemprop="headline">\
            Title Parsed\
            </h1><span itemprop="author"> \
            <a><span itemprop="name">Author Name</span></a></span>\
            <div itemprop="articleBody"><p>body 1</p><p>body 2</p></div></body></html>')
        ret = [x for x in articles_spider.parse_article_content(res)]
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0], {
            'headline': 'Title Parsed',
            'description': '',
            'body': 'body 1\nbody 2',
            'url': url,
            'author': 'Author Name',
            'keywords' : ['']
        })
    
    def test_parse_article_body(self):
        articles_spider = ArticlesSpider()
        selector = Selector(text='<html><body><p>first</p><p>2-<a href="#">Second</a>-2</p><p>3rd</p></body></html>').css("p")
        self.assertEqual(articles_spider.parse_article_body(selector), 'first\n2-Second-2\n3rd')

if __name__ == '__main__':
    unittest.main()