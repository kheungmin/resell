# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LuckyDrawItem(scrapy.Item):
    code = scrapy.Field()
    name_en = scrapy.Field()
    release_date = scrapy.Field()
    price = scrapy.Field()
    img_url = scrapy.Field()
    # img = scrapy.Field()

