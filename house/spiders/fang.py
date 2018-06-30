# -*- coding: utf-8 -*-
import scrapy
import re


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['wuhan.fang.com']
    start_urls = ['http://zu.wuhan.fang.com/']

    def parse(self, response):
        dl_list = response.xpath("//div[@class='houseList']/dl")
        for dl in dl_list:
            item = {}
            item["title"]=dl.xpath(".//dd/p[1]/a/text()").extract_first()
            item["house_style"]=dl.xpath(".//dd/p[2]/text()").extract_first()
            item["local"]=dl.xpath(".//p[@class='gray6 mt20']/a/span/text()").extract_first()
            item["distance"]=dl.xpath(".//dd[@class='info rel']/p[3]/a/span/text()").extract_first()
            item["advantage"]=dl.xpath(".//dd[@class='info rel']/p[5]/span/text()").extract_first()
            item["href"] = dl.xpath(".//dd[@class='info rel']/p[1]/a/@href").extract_first()
            if item["href"] is not None:
                item["href"] = "http://zu.wuhan.fang.com/" + item["href"]
            item["img_href"] = dl.xpath(".//dt/a/img/@src").extract_first()
            if item["img_href"] is None:
                item["img_href"]=re.findall(r"imgiserror(this,(.*?))",response.body)
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta ={"item":item}
            )
            next_url = response.xpath("//div[@class='fanye']/a[text()='下一页']/@href")
            if next_url is not None:
                next_url = "http://zu.wuhan.fang.com" + next_url
                yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                    meta={"item":item}
        )

    def parse_detail(self,response):
        item = response.meta["item"]
        item["price"]=response.xpath("//div[@class='trl-item sty1']/i/text()")
        print(item)