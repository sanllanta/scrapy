# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UniItem(Item):
    name = Field()
    dependency = Field()
    email = Field()
    extension = Field()
    website = Field()

class DependencyItem(Item):
    name = Field()
    teacher_urls = Field()
    main_url = Field()