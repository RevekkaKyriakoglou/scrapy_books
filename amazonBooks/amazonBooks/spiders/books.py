# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.amazon.fr']
    start_urls = ['https://www.amazon.fr/b/?node=302011']

    def parse(self, response):
        for product in response.xpath("//div[@id='mainResults']/ul/li"):
            title = product.xpath(".//div[@class='a-row a-spacing-small']/div[1]/a/@title").get()
            link = product.xpath(".//div[@class='a-row a-spacing-small']/div[1]/a/@href").get()
            date = product.xpath(".//div[@class='a-row a-spacing-small']/div[1]/span[@class='a-size-small a-color-secondary']/text()").get()
            yield{
                'book_title' : title,
                'href' : link,
                'date' : date 
            }

        #next_page = response.xpath("//a[@class='pagnNext']").get()
        #it is relative url and in order to do it manualy absolute, we do the following:
        next_page = response.xpath("//a[@id='pagnNextLink']/@href").extract_first()
        
        if next_page:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_url)
        
    def parse_url(self,response):
        for product in response.xpath("//div[@class='sg-col-inner']/span[@class='rush-component s-latency-cf-section']/div[@class='s-result-list s-search-results sg-row']/div[@class='sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28']"):
            title = product.xpath(".//a[@class='a-link-normal a-text-normal']/span/text()").get()
            link = product.xpath(".//a[@class='a-link-normal a-text-normal']/@href").get()
            date = product.xpath(".//span[@class='a-size-base a-color-secondary a-text-normal']/text()").get()
            yield{
                'book_title' : title,
                'href' : link,
                'date' : date 
            }
        next_page = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a/@href").extract_first()
        
        if next_page:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_url)
          


       