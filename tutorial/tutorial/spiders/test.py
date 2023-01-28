import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['x']
    start_urls = ['http://google.com/']

    def parse(self, response):
        pass

