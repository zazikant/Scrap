import scrapy
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

class QuotesScrollSpider(scrapy.Spider):
    name = 'scroll'
    allowed_domains = ['protiger.com']    
        
    def start_requests(self):
        
          url="https://www.proptiger.com/mumbai/all-builders?page={}"
          
          for i in range(1,5):
                    
                yield scrapy.Request(
                     
                    url.format(i),       
    
                    meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".js-disclaimer>.icon-new-close"),
                    PageMethod("click",".js-disclaimer>.icon-new-close"),
                    PageMethod("evaluate",("window.scrollTo(0,document.body.scrollHeight"))
                ],
                "playwright_include_page": True
            },
            errback=self.close_page
        )

    async def parse(self, response):
           
        for q in response.css('.b-card'):
            yield {
                'builders': q.css('.builder-exp-wrap>.builder-details-wrap ::text').getall(),               
            }

    async def close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()