# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# 데이터를 저장하는 형태 작성 (방법)
import scrapy


class ProjectNameItem(scrapy.Item):
    article_title = scrapy.Field()
    article_time=scrapy.Field()
    article_text= scrapy.Field()
