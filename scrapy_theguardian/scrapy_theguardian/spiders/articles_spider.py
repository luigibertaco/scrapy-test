import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self):
        url = 'https://www.theguardian.com/articles'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article_link in response.css('a[data-link-name="article"]::attr(href)').getall():
            yield scrapy.Request(url=article_link, callback=self.parse_article_content)
    
    def parse_article_body(self, selector):
        return '\n'.join(["".join(x.css("::text").getall()).rstrip() for x in selector])

    def parse_article_content(self, response):
        yield {
            'headline': response.css('h1[itemprop="headline"]::text').get().rstrip(),
            'description': response.css('meta[itemprop="description"]::attr(content)').get().rstrip(),
            'body': self.parse_article_body(response.css('div[itemprop="articleBody"] > p')),
            'url': response.url
        }