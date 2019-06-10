import scrapy

MAX_PAGE_REQUESTS = 5

class ArticlesSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self):
        url = 'https://www.theguardian.com/articles'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article_link in response.css('a[data-link-name="article"]::attr(href)').getall():
            yield scrapy.Request(url=article_link, callback=self.parse_article_content)
        next_page_number = int(response.css('a[data-link-name="Pagination view next"]::attr(data-page)').get())
        print(next_page_number)
        if next_page_number <= MAX_PAGE_REQUESTS:
            next_page_url = response.css('a[data-link-name="Pagination view next"]::attr(href)').get()
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    
    def parse_article_body(self, selector):
        return '\n'.join(["".join(x.css("::text").getall()).strip() for x in selector])

    def parse_article_content(self, response):
        yield {
            'headline': (response.css('h1[itemprop="headline"]::text').get() or '').strip(),
            'description': (response.css('meta[itemprop="description"]::attr(content)').get() or '').strip(),
            'body': self.parse_article_body(response.css('div[itemprop="articleBody"] > p')),
            'url': response.url,
            'author': (response.css('span[itemprop="author"] span[itemprop="name"]::text').get() or '').strip(),
            'keywords': (response.css('meta[name="keywords"]::attr(content)').get() or '').split(","),
        }