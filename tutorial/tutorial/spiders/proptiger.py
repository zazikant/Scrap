import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy_playwright
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

class ProptigerSpider(CrawlSpider):
    name = 'proptiger'
    allowed_domains = ['proptiger.com']
    
    
    def start_requests(self):
    
        for i in range(1,4):
        
            url = f"proptiger.com/mumbai/all-builders?page={i}"
            
            meta={
                
                'playwright': True,
                'playwright_page_methods': [
                    
                    PageMethod("wait_for_selector", ".project-card-main-wrapper:nth-child(15)")
                ],
                "playwright_include_page": True              
            },
            
            errback = self.close_page            
        
            yield scrapy.Request(url, callback=self.parse) 
        
    book_details = LinkExtractor(restrict_css=''),
        
    next_details = LinkExtractor(restrict_css='.custom-pagi  a'),
        
    rule_book_details  = Rule(book_details, callback='parse_item', follow=False),
        
    rule_next = Rule(next_details, callback='parse_item', follow=True),
        
    rules = (rule_book_details, rule_next)
    
    async def parse_item(self, response):
        
        page = response.meta['playwright_page']
        
        for i in range(2,11):
            
            show_count = 15*i
            
            await page.evaluate("window.scrollBy(0,document.body.scrollHeight)")
            
            await page.wait_for_selector(f".project-card-main-wrapper:nth-child{show_count}")
        
        html = await page.content()
        
        await page.close()
        
        s = Selector(text=html)          
    
        for i in s.css('html'):   #toggle element is not given here as there are no duplicates to below yields in entire html
            
            yield{
                
                'Dev_name': i.css('.blacklayer ~.heading::text').get(),
                'Total Projects': i.css('.three-points :nth-child(2) span::text').get(),
                'Ongoing Projects': i.css('.three-points :nth-child(3) span::text').get(),
                'breadcrumb': i.css('.js-breadcrumb-seo >div:first-child> span:last-child a span::text').get(),
                'projects': i.css('.project-card-main-wrapper >div:nth-child(3)>div>div>a>span::text').getall(),
                'location': i.css('.project-card-main-wrapper >div:nth-child(3)>div>div:nth-child(2)>div>span::text').getall(),
                'City': i.css('.proj-address .loc + span').getall()                                

            }

        async def close_page(self, failure):
            
            page = failure.request.meta['playwright_page']
            await page.close()