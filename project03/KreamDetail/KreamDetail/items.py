# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KreamdetailItem(scrapy.Item):
    brand = scrapy.Field()
    prod_name = scrapy.Field()
    prod_kr_name = scrapy.Field()
    rescent_price = scrapy.Field()
    model_no = scrapy.Field()
    release_date = scrapy.Field()
    colors = scrapy.Field()
    release_price = scrapy.Field()
    instant_buy_price = scrapy.Field()
    instant_sell_price = scrapy.Field()
    img_url = scrapy.Field()