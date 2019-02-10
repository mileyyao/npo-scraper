from scrapy import signals
from scrapy import spiders
from scrapy import linkextractors
from urllib import parse

import scrapy
import utils
import json

out_file = 'output.json'
log_file = 'log.txt'

data = []

# clear out files
with open(out_file, 'w') as a, open(log_file, 'w') as b:
    pass


class OrgCrawler(scrapy.Spider):

    name = 'orgcrawler'

    # custom_settings = {
    #     'DEPTH_LIMIT': 1,
    # }

    # called when the spider is closed, will be used for reporting purposes
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OrgCrawler, cls).from_crawler(crawler, *args, **kwargs)

        # register closed method
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    # get urls, generate request objects to crawl
    # will call parse() tp crawl
    def start_requests(self):
        urls = utils.get_urls(filename='partner_urls.txt')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

    # called when spider is closed
    def spider_closed(self):
        with open(out_file, 'w') as f:
            f.write(json.dumps(data, indent=4))

    # crawling logic
    def parse_url(self, response):

        # node object will contain base site and all link neighbors
        node = {
            'base': response.url,
            'partner_links': []
        }

        # anything on homepage that matches <a> tags
        for link in response.xpath('//a'):

            # get the link name, get the link url
            # link_name = link.xpath('text()').get()
            link_url = link.xpath('@href').get()

            # get to see if link matches keywords
            if utils.check_kw(link_url, self.logger):
                node['partner_links'].append(link_url)
                yield scrapy.Request(response.urljoin(link_url), callback=self.parse_url)
        # add to data
        data.append(node)