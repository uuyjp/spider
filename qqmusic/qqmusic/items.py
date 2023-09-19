# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QqmusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vid = scrapy.Field()  # ID
    name = scrapy.Field()  # 标题
    url = scrapy.Field()  # 链接
    content = scrapy.Field()  # 二进制数据
