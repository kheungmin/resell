# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstapostItem(scrapy.Item):
    model_no = scrapy.Field()
    img_url = scrapy.Field()
