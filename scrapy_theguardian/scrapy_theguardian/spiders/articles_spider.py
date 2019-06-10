import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self):
        url = 'https://www.theguardian.com/articles'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass