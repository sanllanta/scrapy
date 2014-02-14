from scrapy.spider import Spider
from scrapy.selector import Selector
from uni.items import UniItem

class UniSpider(Spider):
    name = "uni"
    allowed_domains = ["www.uniandes.edu.co"]
    start_urls = [
        "http://www.uniandes.edu.co"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//body/div[@id="container"]/div[@id="header"]/div[@id="principal"]/div[@id="menupage"]/div[@id="facultad"]')
        
        sites = sites.xpath('.//li')
        items = []

        for site in sites:
            item = UniItem()
            item['dependency'] = site.xpath('./a/text()').extract()
            print site.xpath('./a/text()').extract()
            items.append(item)
            link = site.xpath('./a/@href').extract()
            print link
        return items