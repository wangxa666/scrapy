# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from readbook.items import ReadbookItem

class ReadRedisSpider(RedisCrawlSpider):
    name = 'read_redis'
    allowed_domains = ['www.dushu.com']

    redis_key = 'read:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'/book/1107_\d+.html'),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        img_list = response.xpath('//div[@class="bookslist"]//img')
        for img in img_list:
            src = img.xpath('./@data-original').extract_first()
            name = img.xpath('./@alt').extract_first()
            book = ReadbookItem(src=src, name=name)
            yield book
