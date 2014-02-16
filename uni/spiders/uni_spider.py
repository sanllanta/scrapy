from scrapy.spider import Spider,BaseSpider
from scrapy.selector import Selector
from uni.items import UniItem
from uni.items import DependencyItem
from scrapy.http    import Request
from urlparse import urlparse

class UniSpider(BaseSpider):
    name = "uni"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = [
        "http://uniandes.edu.co"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//body/div[@id="container"]/div[@id="header"]/div[@id="principal"]/div[@id="menupage"]/div[@id="facultad"]')
        sites = sites.xpath('.//li')
        items = []

        for site in sites:

            dependency = site.xpath('./a/text()').extract()
            if len(dependency) > 0:
                #items.append(item)
                print dependency
                link = site.xpath('normalize-space(./a/@href)').extract()[0]
                print link

                #Es un link a una dependencia
                if 'uniandes.edu.co' in link:
                    request=Request(str(link), callback=self.parse_dependency)
                    request.meta['dependency']= dependency[0]
                    request.meta['url']= link
                    yield request


    def parse_dependency(self, response):
        dependency = DependencyItem()
        dependency['name'] =  response.meta['dependency']
        dependency['main_url'] =  response.meta['url']
        dependency['teacher_urls'] = []

        url = urlparse(response.meta['url'])
        domain = url.hostname.split('.')[0]
        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
       
        print '--'+dependency['name']+'--'

        for link in links:
            if (link.startswith('/') or (domain in link)) and (('planta' in link) or ('profesores' in link)):
                print '\t-'+link
                dependency['teacher_urls'].append(link)
        return dependency