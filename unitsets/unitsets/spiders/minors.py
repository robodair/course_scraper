# -*- coding: utf-8 -*-
import scrapy


class MinorsSpider(scrapy.Spider):
    name = 'minors'
    allowed_domains = ['canberra.edu.au']
    start_urls = ['https://search.canberra.edu.au/s/search.html?collection=courses&from-advanced=true&facetScope=f.Year%257CO%3D2019&scope=&query=&query_and=&query_phrase=&query_not=&meta_t=minor&meta_a=&meta_s=&meta_f_sand=&meta_d1year=&meta_d1month=&meta_d1day=&meta_d2year=&meta_d2month=&meta_d2day=&sort=&num_ranks=1000&origin=&maxdist=&scope=&meta_v=']

    def parse(self, response):
        for list_item in response.css('#search-results li[data-fb-result]'):
            title = list_item.css('h4 a::text').extract_first().strip()
            link = list_item.css('a::attr(title)').extract_first()
            yield response.follow(link, self.parse_set)

    def parse_set(self, response):
        title = response.css('main .center-col h1::text').extract_first().strip()
        requirements = response.css(".course__requirements ul li span a::text").extract()
        yield {
            'title': title,
            'requirements': requirements
        }
