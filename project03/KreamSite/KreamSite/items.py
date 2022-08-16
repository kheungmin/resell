# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KreamsiteItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    kr_name = scrapy.Field()
    price = scrapy.Field()
    like = scrapy.Field()
    post = scrapy.Field()
    all_trade = scrapy.Field()
    link = scrapy.Field()
    
    