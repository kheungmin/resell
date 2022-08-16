# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ProjectTestItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
class ProjectTestItem(scrapy.Item):
    news_title = scrapy.Field()
    news_time = scrapy.Field()
    news_content = scrapy.Field()